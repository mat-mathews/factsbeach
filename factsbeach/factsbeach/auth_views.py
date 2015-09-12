import os
import sys
import redis
import random
import requests
import datetime
import traceback
import ConfigParser
import logging
import json
from collections import defaultdict
from hashlib import sha512
from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import *
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
)
from mako.template import Template
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.exc import *

from pyaella import *
from pyaella import dinj
from pyaella.server.api import *
from pyaella.orm.xsqlalchemy import SQLAlchemySessionFactory
from pyaella.orm.auth import get_user, forget_user
from pyaella.geo import GPSPoint, GeoHashGrid
from pyaella.metacode import tmpl as pyaella_templates
from pyaella.server.processes import Emailer
from pyaella.codify import *
from pyaella.tasks import Task

import factsbeach
from factsbeach import *
from factsbeach.models import *


ASSETS_DIR = os.path.dirname(os.path.abspath(factsbeach.assets.__file__))


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
fh = logging.FileHandler(__name__+'.log')
fh.setLevel(logging.DEBUG)
frmttr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmttr)
log.addHandler(fh)


def get_session():
    return SQLAlchemySessionFactory().Session


# TODO: memoize
def get_app_config():
    return dinj.AppConfig()


def get_dinj_config(app_config):
    return dinj.DinjLexicon(parsable=app_config.FullConfigPath)


@view_config(
    name='signup',
    request_method='GET',
    context='factsbeach:contexts.AppRoot',
    renderer='signup.mako')
def signup_new_user(request):
    try:
        
        args = list(request.subpath)
        kwds = _process_subpath(args)
        
        auth_usrid = authenticated_userid(request)
        session = get_session()

        return dict(
            app_name=kwds['app'] if 'app' in kwds else 'Erwin',
            email_address=kwds['email'] if 'email' in kwds else None,
            logged_in=auth_usrid
        )

    except HTTPFound: raise
    except EntityNotFound:
        raise HTTPNotFound(explanation='Requested Entity does not exist')
    except:
        log.exception(traceback.format_exc())
        raise HTTPBadRequest(explanation='Invalid query parameters')
    finally:
        try:
            session.close()
        except:
            pass


@view_config(
    name='signup',
    request_method='POST',
    context='factsbeach:contexts.AppRoot',
    renderer='json')
def signup_new_user_post(request):
    """ """
    try:
        print 'signup_new_user_post called', request
        args = list(request.subpath)
        kwds = _process_subpath(
            request.subpath, formUrlEncodedParams=request.POST)

        ac = get_app_config()
        dconfig = get_dinj_config(ac)
        session = get_session()
        user = None
        email_address = kwds['email_address'].lower()

        user = (session.query(~User)
                    .filter((~User).email_address==kwds['email_address'].lower())
                    ).first()
        if user:
            user = User(entity=user)

            if user.is_active:
                # this user already active
                raise HTTPConflict
                
            # supporting re-up users?
            for k,v in kwds.items():
                setattr(user, k, v)
        else:
            user = User(**kwds)

        user.access_token = \
            sha512(
                str(user.id) + str(user.initial_entry_date) + default_hashkey
            ).hexdigest()
        user.password = sha512(user.password + default_hashkey).hexdigest()
        user.auth_code = generate_auth_code(8, 1)[0]
        user.device_tokens = []
        user.is_active = True

        user.save(session)

        """
            1 == su
            2 == admin
            3 == editor
            4 == user
        """
        grp_ids = set()
        grp_lut = LutValues(model=Group)
        utl_lut = LutValues(model=UserTypeLookup)

        grp_ids.add(grp_lut.get_id('su'))

        # add to correct group (permission role)
        grp_ids = list(grp_ids)
        grp_ids.sort()
        # lowest is best
        UserXGroup(
            user_id=user.id, 
            group_id=grp_ids[0]
            ).save(session=session)

        # add user types
        UserXUserTypeLookup(
            user_id=user.id, 
            user_type_id=utl_lut.get_id('super_user')
            ).save(session=session)

        APP = ~Application
        factsbeach_app = (session.query(APP)
                    .filter(APP.name=='factsbeach-summer-meakan')
                    ).first()
        if factsbeach_app:
            UserXApplication(
                user_id=user.id,
                enabled=True,
                application_id=factsbeach_app.id
                ).save(session=session)
        else:
            raise HTTPBadRequest("Requested application does not exist")

        result = make_result_repr(
            User,
            [user],
            logged_in=user.email_address if user else None,
            create_came_from=kwds['create_came_from'] if 'create_came_from' in kwds else None
        )

        return result
        

    except HTTPGone: raise
    except HTTPFound: raise
    except HTTPUnauthorized: raise
    except HTTPConflict: raise
    except PyaellaHTTPException: raise
    except EntityNotFound:
        raise HTTPNotFound(explanation='Requested Entity does not exist')
    except:
        print traceback.format_exc()
        log.exception(traceback.format_exc())
        raise HTTPBadRequest(explanation='Invalid query parameters?')
    finally:
        try:
            session.close()
        except:
            pass


@view_config(
    name='login',
    request_method='GET',
    context='factsbeach:contexts.AppRoot',
    renderer='login.mako')
def login_get(request):
    args = list(request.subpath)
    kwds = _process_subpath(args)
    return {
        'url': '/login',
        'came_from': '/login',
        'login': kwds['email_address'] if 'email_address' in kwds else '',
        'password': '',
        'message': '',
        'logged_in': authenticated_userid(request)
    }


@view_config(
    name='login',
    request_method='POST',
    context='factsbeach:contexts.AppRoot',
    renderer='json')
@forbidden_view_config(renderer='login.mako')
def login_post(request):
    """ """
    print 'login_post', request
    login_url = request.resource_url(request.context, 'login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/u/account'
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    user = None
    status = 'Err'
    if 'form.submitted' in request.params:
        login = request.params['login']
        print request.params['password']
        password = sha512(request.params['password'] + default_hashkey).hexdigest()
        print 'PASSWORD ENCRYPTED', password
        # forget_user(login)
        user = get_user(login)
        print 'HERE IS THE USER', user
        if user:
            print 'USER PASSWORD', user.password
            if str(user.password) == str(password):

                # set headers
                headers = remember(request, login)
                request.response.headerlist.extend(headers)
            
                status='Ok'
                message='Login succeeded'
                
                # return HTML only if requested
                if 'resp' in request.params and request.params['resp'] == 'html':
                    redirect = came_from if came_from != '/login' else '/login'
                    resp = HTTPFound(location=redirect, headers=headers)
                    resp.headers['LOGIN-SUCCESS'] = 'TRUE'
                    raise resp
            else:
                message = 'Failed login'
                request.response.headers['LOGIN-SUCCESS'] = "FALSE"
        else:
            message = 'Failed login'
            request.response.headers['LOGIN-SUCCESS'] = "FALSE"

    res = dict(
        status=status,
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login,
        password=password,
        logged_in=login if status=='Ok' else None
    )
    return res


@view_config(
    context='factsbeach:contexts.AppRoot',
    name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(
        location='/login', headers=headers)


@view_config(
    name='forgotten-password',
    request_method="GET",
    context='factsbeach:contexts.AppRoot',
    renderer="forgotten.password.mako")
def forgotten_password(request):
    try:
        args = list(request.subpath)
        kwds = _process_subpath(args, formUrlEncodedParams=request.POST)
        dconfig = get_dinj_config(get_app_config())

        return dict(
            url='/password-reset'
            )

    except HTTPUnauthorized: raise
    except EntityNotFound:
        raise HTTPNotFound(explanation='Requested Entity does not exist')
    except:
        log.exception(traceback.format_exc())
        raise HTTPBadRequest(explanation='Invalid query parameters')
    finally:
        try:
            session.close()
        except:
            pass


@view_config(
    name='password-reset',
    request_method="GET",
    context='factsbeach:contexts.AppRoot',
    renderer="password.reset.result.mako")
def password_reset_get(request):
    args = list(request.subpath)
    kwds = _process_subpath(args)           
    return dict(
        email_address=kwds['email_address']
    )


@view_config(
    name='password-reset',
    request_method="POST",
    context='factsbeach:contexts.AppRoot',
    renderer="password.reset.result.mako")
def password_reset(request):
    try:
        args = list(request.subpath)
        kwds = _process_subpath(args, formUrlEncodedParams=request.POST)
        dconfig = get_dinj_config(get_app_config())
        user = get_current_user(kwds['email_address'])
        if user:
            session = get_session()
            user = session.merge(user)

            tmp_passwd = 'X' + sha512(str(datetime.datetime.now()) + default_hashkey).hexdigest()[:8].lower() + 'x9'
            user.auth_code = generate_auth_code(8, 1)[0]
            # user.is_active = False
            user.password = sha512(tmp_passwd + default_hashkey).hexdigest()
            
            session.add(user)
            session.commit()

            site_addr = get_site_addr()

            email_tmpl = os.path.join(dconfig.Web.TemplateDir, 'crm', 'email.user.reset.password.mako')

            tmpl_vars = {
                'site_id': 'factsbeach',
                'site_hostname': site_addr,
                'site_display_name': 'Mividio',
                'email_address': kwds['email_address'],
                'auth_code': user.auth_code,
                'tmp_passwd': tmp_passwd
            }

            message_body = Template(filename=email_tmpl).render(**tmpl_vars)

            smtp_usr = dconfig.Resources.SMTP.User
            smtp_psswd = os.environ['MIVIDIO_SMTP_PASSWORD']
            smtp_srvr = dconfig.Resources.SMTP.Server

            emailer = Emailer(smtp_usr, smtp_psswd, smtp_srvr)
            email_res = emailer.send_html_email({
                'to': kwds['email_address'],
                'from': smtp_usr,
                'subject': 'Password reset',
                'message_body': message_body},
                attached_logo=os.path.join(ASSETS_DIR,"factsbeach_house_bug.png"))

            print 'Sent password reset request', kwds['email_address']

            return dict(
                email_address=kwds['email_address']
                )

        else:
            #raise HTTPFound(location="/dev/login")
            raise HTTPUnauthorized(explanation="No account found for email")
            
    except HTTPFound: raise
    except HTTPUnauthorized: raise
    except EntityNotFound:
        raise HTTPNotFound(explanation='Requested Entity does not exist')
    except:
        print traceback.format_exc()
        log.exception(traceback.format_exc())
        raise HTTPBadRequest(explanation='Invalid query parameters')
    finally:
        try:
            session.close()
        except:
            pass


@view_config(
    name='password-reset-verify',
    request_method="GET",
    context='factsbeach:contexts.AppRoot',
    renderer="json")
def password_reset_verify(request):
    try:
        headers = forget(request)
        args = list(request.subpath)
        print 'password_reset_verify args', args
        dconfig = get_dinj_config(get_app_config())
        if args[0] in [None, '']:
            raise Exception('No auth_code provited')
        session = get_session()
        U = ~User
        users = (session.query(U).filter(U.auth_code==args[0])).all()
        if len(users) > 1:
            raise IntegrityError()
        elif users and not users[0].is_active:
            user = users[0]
            user.is_active = True
            user.auth_code = None
            session.add(user)
            session.commit()
            raise HTTPFound(location="/login", headers=headers)
        else:
            raise HTTPGone()

    except HTTPGone: raise
    except HTTPFound: raise
    except HTTPUnauthorized: raise
    except EntityNotFound:
        raise HTTPNotFound(explanation='Requested Entity does not exist')
    except:
        log.exception(traceback.format_exc())
        raise HTTPBadRequest(explanation='Invalid query parameters')
    finally:
        try:
            session.close()
        except:
            pass


@view_config(
    name='disable',
    request_method='POST',
    context='factsbeach:contexts.Users',
    renderer='json',
    permission='user')
def disable_user(request):
    try:
        args = list(request.subpath)
        kwds = _process_subpath(args)
        auth_usrid = authenticated_userid(request)
        user, user_type_names, user_type_lookup = (
            get_current_rbac_user(auth_usrid,
                accept_user_type_names=[
                    'super_user',
                    'user'
                ]
            )
        )
        status = 'Err'
        if user and user.is_active:
            with SQLAlchemySessionFactory() as session:

                r = requests.put("http://localhost:9999/signup", data={
                    'id':user.id,
                    'is_active':False
                })

                if r.status_code == 200:
                    status = 'Ok'
                else:
                    if r.status_code == 409:
                        #user already exists
                        raise HTTPConflict

                    # raise unknown exceptions
                    raise Exception

        return dict(
            status=status,
            logged_in=auth_usrid
        )

    except HTTPFound: raise
    except EntityNotFound:
        raise HTTPNotFound(explanation='Requested Entity does not exist')
    except:
        log.exception(traceback.format_exc())
        raise HTTPBadRequest(explanation='Invalid query parameters')
    finally:
        try:
            session.close()
        except:
            pass


@view_config(
    name='edit-user',
    request_method='GET',
    context='factsbeach:contexts.Admin',
    renderer='admin.edit.user.mako',
    permission='su')
def admin_edit_user_get(request):
    """ """
    try:
        print 'admin_edit_user_get', request

        args = list(request.subpath)
        kwds = _process_subpath(
            request.subpath, formUrlEncodedParams=request.POST)
        ac = get_app_config()
        dconfig = get_dinj_config(ac)
        auth_usrid = authenticated_userid(request)
        user, user_type_names, user_type_lookup = (
            get_current_rbac_user(auth_usrid,
                accept_user_type_names=[
                    'super_user'
                ]
            )
        )
        print 'admin_edit_user_get', user, user_type_names
        if user and user.is_active:
            with SQLAlchemySessionFactory() as session:
                
                user_to_edit = None
                print 'admin_edit_user_get kwds', kwds

                user_to_edit = (session.query(~User)
                            .filter((~User).email_address==kwds['email_address'])
                            ).first()
                
                if user_to_edit:

                    print 'user to edit', user_to_edit

                    utl_lut = LutValues(model=UserTypeLookup)

                    user_to_edit = User(entity=user_to_edit)

                    user_to_edit_utn = [utl_lut.get_name(ut.user_type_id) for ut in user_to_edit.user_types]

                    print 'user_to_edit_utn', user_to_edit_utn

                    res = dict(
                        user_to_edit=user_to_edit,
                        user_to_edit_utn=user_to_edit_utn,
                        user=user,
                        user_type_names=user_type_names,
                        user_type_lookup=user_type_lookup,
                        logged_in=auth_usrid
                        )

                    print 'edit_user res', res
                    return res

        raise HTTPUnauthorized

    except HTTPGone: raise
    except HTTPFound: raise
    except HTTPUnauthorized: raise
    except HTTPConflict: raise
    except PyaellaHTTPException: raise
    except EntityNotFound:
        raise HTTPNotFound(explanation='Requested Entity does not exist')
    except:
        print traceback.format_exc()
        log.exception(traceback.format_exc())
        raise HTTPBadRequest(explanation='Invalid query parameters?')
    finally:
        try:
            session.close()
        except:
            pass


@view_config(
    name='edit-user',
    request_method='POST',
    context='factsbeach:contexts.Admin',
    renderer='admin.edit.user.mako',
    permission='su')
def admin_edit_user_post(request):
    """ """
    try:
        args = list(request.subpath)
        kwds = _process_subpath(
            request.subpath, formUrlEncodedParams=request.POST)
        ac = get_app_config()
        dconfig = get_dinj_config(ac)
        auth_usrid = authenticated_userid(request)
        user, user_type_names, user_type_lookup = (
            get_current_rbac_user(auth_usrid,
                accept_user_type_names=[
                    'super_user'
                ]
            )
        )
        if user and user.is_active:
            with SQLAlchemySessionFactory() as session:
                
                user_to_edit = None

                user_to_edit = (session.query(~User)
                            .filter((~User).email_address==kwds['email_address'])
                            ).first()

                if user_to_edit:

                    utl_lut = LutValues(model=UserTypeLookup)

                    user_to_edit = User(entity=user_to_edit)

                    try:
                        UxUT = ~UserXUserTypeLookup
                        rows = session.query(UxUT).filter(UxUT.user_id==user_to_edit.id).delete()
                        session.commit()
                    except:
                        try:
                            session.rollback()
                        except:
                            pass

                    grp_ids = set()
                    grp_lut = LutValues(model=Group)
                    utl_lut = LutValues(model=UserTypeLookup)

                    grp_ids.add(grp_lut.get_id('user'))

                    try:
                        if 'is_super_user' in kwds and kwds['is_super_user'] == 'true':
                            try:
                                UserXUserTypeLookup(
                                    user_id=user_to_edit.id, 
                                    user_type_id=utl_lut.get_id('super_user')
                                    ).save(session=session)
                            except IntegrityError:
                                try:
                                    (session.query(UxUT)
                                        .filter(UxUT.user_id==user_to_edit.id)
                                        .filter(UxUT.user_type_id==utl_lut.get_id('super_user'))
                                        .update({'last_opr':'INSERT'}))
                                    session.commit()
                                except:
                                    session.rollback()
                            grp_ids.add(grp_lut.get_id('su'))
                    except:pass

                    try:
                        if 'is_sys_admin' in kwds and kwds['is_sys_admin'] == 'true':
                            try:
                                UserXUserTypeLookup(
                                    user_id=user_to_edit.id, 
                                    user_type_id=utl_lut.get_id('sys_admin')
                                    ).save(session=session)
                            except IntegrityError:
                                try:
                                    (session.query(UxUT)
                                        .filter(UxUT.user_id==user_to_edit.id)
                                        .filter(UxUT.user_type_id==utl_lut.get_id('sys_admin'))
                                        .update({'last_opr':'INSERT'}))
                                    session.commit()
                                except:
                                    session.rollback()
                            grp_ids.add(grp_lut.get_id('admin'))
                    except:pass

                    try:
                        if 'is_internal_dev' in kwds and kwds['is_internal_dev'] == 'true':
                            try:
                                UserXUserTypeLookup(
                                    user_id=user_to_edit.id, 
                                    user_type_id=utl_lut.get_id('internal_dev')
                                    ).save(session=session)
                            except IntegrityError:
                                try:
                                    (session.query(UxUT)
                                        .filter(UxUT.user_id==user_to_edit.id)
                                        .filter(UxUT.user_type_id==utl_lut.get_id('internal_dev'))
                                        .update({'last_opr':'INSERT'}))
                                    session.commit()
                                except:
                                    session.rollback()
                            grp_ids.add(grp_lut.get_id('admin'))
                    except:pass

                    try:
                        if 'is_external_dev' in kwds and kwds['is_external_dev'] == 'true':
                            try:
                                UserXUserTypeLookup(
                                    user_id=user_to_edit.id, 
                                    user_type_id=utl_lut.get_id('external_dev')
                                    ).save(session=session)
                            except IntegrityError:
                                try:
                                    (session.query(UxUT)
                                        .filter(UxUT.user_id==user_to_edit.id)
                                        .filter(UxUT.user_type_id==utl_lut.get_id('external_dev'))
                                        .update({'last_opr':'INSERT'}))
                                    session.commit()
                                except:
                                    session.rollback()
                            grp_ids.add(grp_lut.get_id('editor'))
                    except:pass

                    try:
                        if 'is_tester' in kwds and kwds['is_tester'] == 'true':
                            try:
                                UserXUserTypeLookup(
                                    user_id=user_to_edit.id, 
                                    user_type_id=utl_lut.get_id('tester')
                                    ).save(session=session)
                            except IntegrityError:
                                try:
                                    (session.query(UxUT)
                                        .filter(UxUT.user_id==user_to_edit.id)
                                        .filter(UxUT.user_type_id==utl_lut.get_id('tester'))
                                        .update({'last_opr':'INSERT'}))
                                    session.commit()
                                except:
                                    session.rollback()
                            grp_ids.add(grp_lut.get_id('editor'))
                    except:pass

                    try:
                        if 'is_user' in kwds and kwds['is_user'] == 'true':
                            try:
                                UserXUserTypeLookup(
                                    user_id=user_to_edit.id, 
                                    user_type_id=utl_lut.get_id('user')
                                    ).save(session=session)
                            except IntegrityError:
                                try:
                                    (session.query(UxUT)
                                        .filter(UxUT.user_id==user_to_edit.id)
                                        .filter(UxUT.user_type_id==utl_lut.get_id('user'))
                                        .update({'last_opr':'INSERT'}))
                                    session.commit()
                                except:
                                    session.rollback()
                            grp_ids.add(grp_lut.get_id('user'))
                    except:pass


                    grp_ids = list(grp_ids)
                    grp_ids.sort()

                    
                    try:
                        UxG = ~UserXGroup
                        rows = session.query(UxG).filter(UxG.user_id==user_to_edit.id).delete()
                        session.commit()
                    except:
                        print traceback.format_exc()
                        try:
                            session.rollback()
                        except:pass

                    # lowest is best
                    UserXGroup(user_id=user_to_edit.id, group_id=grp_ids[0]).save(session=session)

                    user_to_edit_utn = [utl_lut.get_name(ut.user_type_id) for ut in user_to_edit.user_types]

                    user = get_user(kwds['email_address'], force_refresh=True)

                    print 'forced refreshed', user

                    user = User(entity=user)

                    return dict(
                        user_to_edit=user_to_edit,
                        user_to_edit_utn=user_to_edit_utn,
                        user=user,
                        user_type_names=user_type_names,
                        user_type_lookup=user_type_lookup,
                        logged_in=auth_usrid
                        )

        raise HTTPUnauthorized

    except HTTPGone: raise
    except HTTPFound: raise
    except HTTPUnauthorized: raise
    except HTTPConflict: raise
    except PyaellaHTTPException: raise
    except EntityNotFound:
        raise HTTPNotFound(explanation='Requested Entity does not exist')
    except:
        print traceback.format_exc()
        log.exception(traceback.format_exc())
        raise HTTPBadRequest(explanation='Invalid query parameters?')
    finally:
        try:
            session.close()
        except:
            pass





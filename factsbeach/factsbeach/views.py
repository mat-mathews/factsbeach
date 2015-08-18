import os
import sys
import redis
import logging
import datetime
import traceback
import ConfigParser
from hashlib import sha512
from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import *
from pyramid.security import (remember, forget, authenticated_userid)
from mako.template import Template
#amazon s3 support
from boto.s3.connection import S3Connection, Location
from boto.s3.key import Key
# pyaella imports
from pyaella import *
from pyaella import dinj
from pyaella.server.api import *
from pyaella.orm.xsqlalchemy import SQLAlchemySessionFactory
from pyaella.orm.auth import get_user
from pyaella.geo import GPSPoint
from pyaella.metacode import tmpl as pyaella_templates
from pyaella.server.processes import Emailer


from factsbeach import *
from factsbeach.models import *


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
fh = logging.FileHandler(__name__+'.log')
fh.setLevel(logging.DEBUG)
frmttr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmttr)
log.addHandler(fh)


@view_config(
    name='',
    request_method='GET',
    renderer='default.mako')
def say_hello(request):
    auth_usrid = authenticated_userid(request)
    return dict(
        logged_in=auth_usrid
        )


@view_config(
    name='account',
    request_method='GET',
    context='factsbeach:contexts.Users',
    renderer='user.mako')
def user_account(request):
    try:
        args = list(request.subpath)
        kwds = _process_subpath(args)
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
                
                DUER = ~DefinedUserEventReport
                duers = session.query(DUER).all()

                GLTLU, GPETLU = ~GameLocationTypeLookup, ~GamePlayEventTypeLookup

                game_locations = session.query(GLTLU).order_by(GLTLU.name).all()

                game_play_events = session.query(GPETLU).order_by(GPETLU.name).all()

                return dict(
                    status='Ok',
                    defined_ue_reports=[DefinedUserEventReport(entity=d) for d in duers],
                    game_locations=game_locations,
                    game_play_events=game_play_events,
                    logged_in=auth_usrid
                    )

        raise HTTPUnauthorized

    except HTTPAccepted: raise
    except HTTPGone: raise
    except HTTPFound: raise
    except HTTPUnauthorized: raise
    except HTTPConflict: raise
    except:
        print traceback.format_exc()
        log.exception(traceback.format_exc())
        raise HTTPBadRequest(explanation='Invalid query parameters?')
    finally:
        try:
            session.close()
        except:
            pass


















import os
import sys
import datetime
import traceback
import logging
import ConfigParser
from hashlib import sha512
from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import *
from pyramid.security import (remember, forget, authenticated_userid)
from mako.template import Template
from sqlalchemy import *
from sqlalchemy.orm import *
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


def get_count(q):
	""" BROKEN """
	count_q = q.statement.with_only_columns([func.count()]).order_by(None)
	count = q.session.execute(count_q).scalar()
	return count


def get_ue_event_attrs(session, **kwds):

	UE = ~UserEvent
	ue_cats = (session.query(UE.event_category)
			.filter(UE.session_key==kwds['session_key'])
			.filter(UE.event_category != None)
			.distinct()
			).all()
	ue_mets = (session.query(UE.event_metric)
			.filter(UE.session_key==kwds['session_key'])
			.filter(UE.event_metric != None)
			.distinct()
			).all()
	ue_vals = (session.query(UE.event_value)
			.filter(UE.session_key==kwds['session_key'])
			.filter(UE.event_value != None)
			.distinct()
			).all()

	return ue_cats, ue_mets, ue_vals



@view_config(
	name='base-report',
	request_method='GET',
	context='factsbeach:contexts.Reports',
	renderer='base.report.mako')
def base_report(request):
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

				UE = ~UserEvent
				DUER = ~DefinedUserEventReport
				duer = (session.query(DUER)
							.filter(DUER.id==kwds['id'])
							).first()
				kwds['session_key'] = duer.session_key
				ue_cats, ue_mets, ue_vals = get_ue_event_attrs(session, **kwds)

				session_keys = session.query(UE.session_key).distinct().all()

				return dict(
					status='Ok',
					duer=duer,
					session_keys=session_keys,
					ue_cats=[c[0] for c in ue_cats],
					ue_mets=[m[0] for m in ue_mets],
					ue_vals=[v[0] for v in ue_vals]
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


@view_config(
	name='base',
	request_method='GET',
	context='factsbeach:contexts.Reports',
	renderer='json')
def get_base_user_event_report_data(request):
	print 'get_base_user_event_report_data called', request
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
				
				UE = ~UserEvent
				q = session.query(UE)

				if 'session_key' in kwds and kwds['session_key'] not in [None, "", "None"]:

					q = q.filter(UE.session_key==kwds['session_key'])
					if 'event_category' in kwds and kwds['event_category'] not in [None, "", "None"]:
						q = q.filter(UE.event_category==kwds['event_category'])
						q = q.filter(UE.event_metric==kwds['event_metric'])
						q = q.filter(UE.event_value==kwds['event_value'])
				else:
					if 'event_category' in kwds and kwds['event_category'] not in [None, "", "None"]:
						q = q.filter(UE.event_category==kwds['event_category'])
						q = q.filter(UE.event_metric==kwds['event_metric'])
						q = q.filter(UE.event_value==kwds['event_value'])
						if 'session_key' in kwds and kwds['session_key'] not in [None, "", "None"]:
							q = q.filter(UE.session_key==kwds['session_key'])
					else:
						raise HTTPBadRequest("Reports require Session Keys or Event Criteria")

				print 'QUERY', q


				if 'limit' in kwds:
					q = q.limit(kwds['limit'])

				if 'offset' in kwds:
					q = q.offset(kwds['offset'])

				rp = q.all()

				head_health = []
				for ue in rp:
					if ue.head_health:
						head_health.append([float(ue.in_game_timestamp), float(ue.head_health)])

				torso_health = []
				for ue in rp:
					if ue.torso_health:
						torso_health.append([float(ue.in_game_timestamp), float(ue.torso_health)])

				right_arm_health = []
				for ue in rp:
					if ue.right_arm_health:
						right_arm_health.append([float(ue.in_game_timestamp), float(ue.right_arm_health)])

				left_arm_health = []
				for ue in rp:
					if ue.left_arm_health:
						left_arm_health.append([float(ue.in_game_timestamp), float(ue.left_arm_health)])

				right_leg_health = []
				for ue in rp:
					if ue.right_leg_health:
						right_leg_health.append([float(ue.in_game_timestamp), float(ue.right_leg_health)])

				left_leg_health = []
				for ue in rp:
					if ue.left_leg_health:
						left_leg_health.append([float(ue.in_game_timestamp), float(ue.left_leg_health)])

				total_health = []
				for ue in rp:
					if ue.total_health:
						total_health.append([float(ue.in_game_timestamp), float(ue.total_health)])

				mental_health = []
				for ue in rp:
					if ue.mental_health:
						mental_health.append([float(ue.in_game_timestamp), float(ue.mental_health)])

				stamina = []
				for ue in rp:
					if ue.stamina:
						stamina.append([float(ue.in_game_timestamp), float(ue.stamina)])

				oxygen = []
				for ue in rp:
					if ue.oxygen:
						oxygen.append([float(ue.in_game_timestamp), float(ue.oxygen)])

				food = []
				for ue in rp:
					if ue.food:
						food.append([float(ue.in_game_timestamp), float(ue.food)])

				water = []
				for ue in rp:
					if ue.water:
						water.append([float(ue.in_game_timestamp), float(ue.water)])

				temperature = []
				for ue in rp:
					if ue.temperature:
						temperature.append([float(ue.in_game_timestamp), float(ue.temperature)])

				os_name = None
				for ue in rp:
					if ue.os_name != None:
						os_name = ue.os_name
						break
						
				cpu_name = None
				for ue in rp:
					if ue.cpu_name:
						cpu_name = ue.cpu_name
						break

				gpu_name = None
				for ue in rp:
					if ue.gpu_name:
						gpu_name = ue.gpu_name
						break

				gmem_size = 0
				for ue in rp:
					if ue.gmem_size:
						gmem_size = ue.gmem_size
						break

				smem_size = 0
				for ue in rp:
					if ue.smem_size:
						smem_size = ue.smem_size
						break

				frame_rate = []
				for ue in rp:
					if ue.frame_rate:
						frame_rate.append([float(ue.in_game_timestamp), float(ue.frame_rate)])

				resolution = []
				for ue in rp:
					if ue.resolution:
						resolution.append([float(ue.in_game_timestamp), ue.resolution])



				count = len(rp)

				return dict(
					status='Ok',
					count=count,
					head_health=head_health,
					torso_health=torso_health,
					right_arm_health=right_arm_health,
					left_arm_health=left_arm_health,
					right_leg_health=right_leg_health,
					left_leg_health=left_leg_health,
					total_health=total_health,
					mental_health=mental_health,
					stamina=stamina,
					oxygen=oxygen,
					food=food,
					water=water,
					temperature=temperature,
					os_name=os_name,
					cpu_name=cpu_name,
					gpu_name=gpu_name,
					gmem_size=gmem_size,
					smem_size=smem_size,
					frame_rate=frame_rate,
					resolution=resolution,
					user_events=[UserEvent(entity=ue) for ue in rp]
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


@view_config(
	name='game-loc',
	request_method='GET',
	context='factsbeach:contexts.Reports',
	renderer='json')
def get_base_game_location_report_data(request):
	print 'get_base_game_location_report_data called'
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
				
				UE, GLLU = ~UserEvent, ~GameLocationTypeLookup
				q = (session.query(UE, GLLU)
						.filter(UE.event_category=="location")
						.filter(UE.game_location_type_id != None)
						.filter(GLLU.id==UE.game_location_type_id)
						.order_by(UE.in_game_timestamp)
						)

				if 'limit' in kwds:
					q = q.limit(kwds['limit'])

				if 'offset' in kwds:
					q = q.offset(kwds['offset'])

				rp = q.all()

				count = len(rp)

				game_locations = {}
				for row in rp:
					ue, gllut = row
					game_locations.setdefault(gllut.name, {}).setdefault('count', 0)
					game_locations[gllut.name]['points'] = (gllut.x_point, gllut.y_point)
					game_locations[gllut.name]['count'] += 1

				return dict(
					status='Ok',
					count=count,
					game_locations=game_locations
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



@view_config(
	name='session-categories',
	request_method='GET',
	context='factsbeach:contexts.Reports',
	renderer='json')
def get_base_session_categories_data(request):
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
				
				ue_cats, ue_mets, ue_vals = get_ue_event_attrs(session, **kwds)

				return dict(
					status='Ok',
					ue_cats=ue_cats,
					ue_mets=ue_mets,
					ue_vals=ue_vals
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



@view_config(
	name='compare',
	request_method='GET',
	context='factsbeach:contexts.Reports',
	renderer='json')
def get_base_session_compare_data(request):
	print 'get_base_session_compare_data called', request
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
				
				UE = ~UserEvent
				q = (session.query(UE)
						.filter(UE.event_category==kwds['event_category'])
						.filter(UE.event_metric==kwds['event_metric'])
						.filter(UE.event_value==kwds['event_value'])
						)
				if 'session_key' in kwds and kwds['session_key'] != None:
					q = q.filter(UE.session_key == kwds['session_key'])

				q = q.order_by(UE.in_game_timestamp)

				rp = q.all()

				print 'get_base_session_compare_data rp', rp

				vals = []
				for ue in rp:
					vals.append([float(ue.in_game_timestamp), 1])


				print 'get_base_session_compare_data vals', vals

				return dict(
					status='Ok',
					cat_name=kwds['event_category'],
					met_name=kwds['event_metric'],
					val_name=kwds['event_value'],
					event_values=vals,
					user_events=[UserEvent(entity=ue) for ue in rp]
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









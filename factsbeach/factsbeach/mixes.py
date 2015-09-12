import os
import sys
import redis
import urlparse
import jsonpickle
import traceback
from hashlib import sha512

import pyaella
from pyaella import *
from pyaella.server.api import *
from pyaella.tasks import *
from pyaella.orm.xsqlalchemy import SQLAlchemySessionFactory
from pyaella.codify import IdCoder, generate_auth_code
from pyaella import dinj

from factsbeach import *


_MODELS = None

_redis = None


def get_app_config():
    return dinj.AppConfig()


def get_dinj_config(app_config):
    return dinj.DinjLexicon(parsable=app_config.FullConfigPath)


def _get_redis_server(dinj_config):
	global _redis
	if not _redis:
		if('RedisServer' in dinj_config.Resources):
			if dinj_config.Resources.RedisServer not in [None, '']:
					_redis = redis.Redis(dinj_config.Resources.RedisServer)
			else:
				raise Exception('No Redis server specified in ENV or Config')
	return _redis


@memoize
def _get_model(name):
	global _MODELS
	if not _MODELS:
		_MODELS = SQLAlchemySessionFactory().ModelsModule
	return _MODELS.__dict__[name]


@memoize_exp(expiration=30)
def LUT_FACTORY(model):
	return LutValues(model=model)


class UserEventMix(Mix):

	def post_pre_hook(self, **kwds):
		if 'event_category' in kwds and kwds['event_category'] == 'location':
			gl_lut = LUT_FACTORY(model=_get_model('GameLocationTypeLookup'))
			if kwds['event_metric'] in gl_lut.get_all_names():
				setattr(self, 'game_location_type_id', gl_lut(kwds['event_metric']))

	def post_final_hook(self, session, **kwds):
		pass

	def put_pre_hook(self, session, **kwds):
		return self, kwds


class GameLocationTypeLookupMix(Mix):

	def post_pre_hook(self, **kwds):
		pass

	def post_final_hook(self, session, **kwds):
		try:
			ac = get_app_config()
			dconfig = get_dinj_config(ac)
			
			task = Task(
				target='UpdateDatabase',
				model='GameLocationTypeLookup',
				action='UPDATE',
				game_location_name=self.name
				)

			r_srv = _get_redis_server(dconfig)

			if r_srv:
				data = op.json ** task
				rpush_res = r_srv.rpush(
					REDIS_CHANNEL_TO_HEVN_IN, data)

		except:
			traceback.format_exc()

	def pre_delete(self, session, **kwds):
		print 'pre_delete called', kwds, self.id
		try:
			ac = get_app_config()
			dconfig = get_dinj_config(ac)
			
			gllut = LUT_FACTORY(model=_get_model('GameLocationTypeLookup'))

			UE = ~(_get_model('UserEvent'))
			res = session.query(UE).filter(UE.game_location_type_id==self.id).update(
				{ UE.game_location_type_id: 1}, synchronize_session=False
			)
			session.commit()

		except:
			print traceback.format_exc()

	def finalize_delete(self, session, **kwds):
		pass


class GamePlayEventTypeLookupMix(Mix):

	def post_pre_hook(self, **kwds):
		pass

	def post_final_hook(self, session, **kwds):
		try:
			ac = get_app_config()
			dconfig = get_dinj_config(ac)
			
			task = Task(
				target='UpdateDatabase',
				model='GamePlayEventTypeLookup',
				action='UPDATE',
				game_play_event_name=self.name
				)

			r_srv = _get_redis_server(dconfig)

			if r_srv:
				data = op.json ** task
				rpush_res = r_srv.rpush(
					REDIS_CHANNEL_TO_HEVN_IN, data)

		except:
			traceback.format_exc()



























import os
import sys
import time
import shutil
import redis
import traceback
import datetime
import multiprocessing
import threading
import PIL as pil
from boto.s3.key import Key
from boto.s3.connection import S3Connection, Location

from pyaella import *
from pyaella import dinj
from pyaella.server.api import *
from pyaella.server.processes import UploadProcess
from pyaella.tasks import *
from pyaella.orm.xsqlalchemy import SQLAlchemySessionFactory

from factsbeach import *
from factsbeach.models import *

#  Boto tutorial here http://docs.pythonboto.org/en/latest/s3_tut.html

__procs__ = [
    'FactsBeachUpdateThread'
]


# def get_app_config():
#     return dinj.AppConfig()


# def get_dinj_config(app_config):
#     return dinj.DinjLexicon(parsable=app_config.FullConfigPath)


@memoize_exp(expiration=300)
def LUT_FCTRY(model):
    return LutValues(model=model)


class FactsBeachUpdateThread(threading.Thread):
    """ """
    AsyncFamily = 'Threading'

    def setup(self):
        self._app_config = dinj.AppConfig()
        self._dinj_config = dinj.DinjLexicon(parsable=self._app_config.FullConfigPath)

        self._dispatch = {
            'UpdateDatabase':self.on_update_database,
        }

        self._r_srv = None

        if('RedisServer' in self._dinj_config.Resources):
            self._r_srv = redis.Redis(self._dinj_config.Resources.RedisServer, socket_timeout=15)

        self._lock = threading.RLock()
        self._go = threading.Event()

    def on_new(self, task):
        return self._dispatch[task.Target](task)

    def on_update_database(self, task):
        print 'on_update_database called', task
        try:
            with SQLAlchemySessionFactory() as session:
                UE = ~UserEvent
                gllut = LUT_FCTRY(model=GameLocationTypeLookup)

                try:
                    if task.action == 'UPDATE' and task.model == 'GameLocationTypeLookup':

                        try:
                            gltid = gllut(task.game_location_name)
                            if gltid:
                                session.query(UE).filter(UE.event_metric==task.game_location_name).update(
                                    { 'game_location_type_id': gltid}, synchronize_session='fetch'
                                )
                                session.commit()
                        except:
                            pass

                    if task.action == 'DELETE' and task.model == 'GameLocationTypeLookup':

                        try:
                            gltid = gllut(task.game_location_name)
                            session.query(UE).filter(UE.game_location_type_id==task.game_location_type_id).update(
                                { 'game_location_type_id': 1}, synchronize_session='fetch'
                            )
                            session.commit()
                        except:
                            pass

                except:
                    print traceback.format_exc()


        except:
            print traceback.format_exc()
        finally:
            try:
                session.close()
            except:
                pass

    
    def run(self):
        self.setup()
        sleep_x = 1
        to_close = set()
        while not self._go.is_set():
            if self._r_srv:

                item = self._r_srv.rpoplpush(
                    REDIS_CHANNEL_TO_HEVN_IN, 
                    REDIS_CHANNEL_TO_HEVN_OUT
                )

                if item:
                    with self._lock:
                        try:
                            self.on_new(Task ** item)
                        except:
                            print traceback.format_exc()

                time.sleep(sleep_x) # be nice to the machines




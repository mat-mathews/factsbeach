import os, sys
import ConfigParser
from pyaella import dinj
from pyaella import memoize, memoize_exp


__all__ = [
    'get_app_config',
    'get_dinj_config',
    'get_site_addr',
    'default_hashkey',
    'REDIS_CHANNEL_TO_HEVN_IN',
    'REDIS_CHANNEL_TO_HEVN_OUT'

]


_HOST, _PORT = None, None


REDIS_CHANNEL_TO_HEVN_IN = 'REDIS_CHANNEL_TO_HEVN_IN'
REDIS_CHANNEL_TO_HEVN_OUT = 'REDIS_CHANNEL_TO_HEVN_OUT'


try:
    if len(sys.argv) > 0:
        # Read host and port from 
        __cfg = ConfigParser.ConfigParser()
        __cfg.read(sys.argv[1])
        _HOST = __cfg.get('server:main', 'host')
        _PORT = __cfg.get('server:main', 'port')
except:
    pass


def get_app_config():
    return dinj.AppConfig()


def get_dinj_config(app_config):
    return dinj.DinjLexicon(parsable=app_config.FullConfigPath)


@memoize
def get_site_addr():
        sn = get_dinj_config(get_app_config()).Web.SiteName
        if _PORT != None:
            if _PORT not in [80, '80', ""]:
                sn += ':%s'%_PORT
        return sn #+ ':%s'%_PORT if _PORT not in [80, '80', ''] else ''


default_hashkey = (
    '0f6241880e5f26c13d02caf73f4f4cff'
    '9ce292499db4f2cbf7b348c1f5b6e0f5'
    '9e3a52334ddbf536b7ac89949a6c0ed6'
    'ee5bd4718aa0a74b330a9a55b4bc97a2'
)
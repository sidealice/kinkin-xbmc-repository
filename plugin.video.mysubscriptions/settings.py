'''

@author: Batch
'''
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os
from common import create_directory, create_file

ADDON = xbmcaddon.Addon(id='plugin.video.mysubscriptions')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.mysubscriptions'), '')

def addon():
    return ADDON

def data_path():
    return DATA_PATH

def subscription_file():
    return create_file(DATA_PATH, "subscription.list")
	
def subs_imdb_file():
    return create_file(DATA_PATH, "subs_imdb.list")
	
def tv_directory():
    if ADDON.getSetting('tv_directory').startswith('special'):
        return create_directory(DATA_PATH, "TV_SUBSCRIPTIONS")
    else:
        return ADDON.getSetting('tv_directory')
	
def show_unaired():
    if ADDON.getSetting('show_unaired') == "true":
        return True
    else:
        return False
		
def subscription_update():
    if ADDON.getSetting('subscription_update') == "true":
        return True
    else:
        return False

def dummy_path():
    return os.path.join(ADDON.getAddonInfo('path'), 'dummy.wma')

def service_sleep_time():
    return 10

def subscription_timer():
    return int(ADDON.getSetting('subscription_timer'))
		
create_directory(DATA_PATH, "")

	

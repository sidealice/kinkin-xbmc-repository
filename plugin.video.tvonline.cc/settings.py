import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON = xbmcaddon.Addon(id='plugin.video.tvonline.cc')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.tvonline.cc'), '')
TVO_PATH = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', ''))

def addon():
    return ADDON
	
def tvo_user():
    return ADDON.getSetting('tvo_user') 

def tvo_pass():
    return ADDON.getSetting('tvo_pass') 
	
def tvo_email():
    return ADDON.getSetting('tvo_email')
	
def enable_subscriptions():
    if ADDON.getSetting('enable_subscriptions') == "true":
        return True
    else:
        return False
		
def enable_meta():
    if ADDON.getSetting('enable_meta') == "true":
        return True
    else:
        return False
	
def tv_directory():
    if ADDON.getSetting('tv_directory').startswith('special'):
        return create_directory(DATA_PATH, "tvshows")
    else:
        return ADDON.getSetting('tv_directory')
		
def cache_path():
    return create_directory(DATA_PATH, "cache")
	
def favourites_file():
    return create_file(DATA_PATH, "favourites.list")
	
def subscription_file():
    return create_file(DATA_PATH, "subscriptions.list")

	
def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path
	
create_directory(DATA_PATH, "")

		

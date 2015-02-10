import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON = xbmcaddon.Addon(id='plugin.video.flixanity')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.flixanity'), '')
TVO_PATH = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', ''))



def addon():
    return ADDON
	
def base_url():
    quality = ADDON.getSetting('base_url')
    if quality == '0':
        return 'http://www.flixanity.com/'
    else:
        return 'http://www.cartoonhd.is/'
	
def enable_meta():
    if ADDON.getSetting('enable_meta') == "true":
        return True
    else:
        return False
	
def ms_account():
    if ADDON.getSetting('ms_account') == "true":
        return True
    else:
        return False
	
def ms_user():
    return ADDON.getSetting('ms_user') 

def ms_pass():
    return ADDON.getSetting('ms_pass') 
	
def cache_path():
    return create_directory(DATA_PATH, "cache")

	
def enable_subscriptions():
    if ADDON.getSetting('enable_subscriptions') == "true":
        return True
    else:
        return False
		
def autoplay():
    if ADDON.getSetting('autoplay') == "true":
        return True
    else:
        return False
		
def restrict_trailer():
    if ADDON.getSetting('restrict_trailer') == "true":
        return True
    else:
        return False
		
def trailer_quality():
    quality = ADDON.getSetting('trailer_quality')
    if quality == '0':
        return '480p'
    elif quality == '1':
        return '720p'
    else:
        return '1080p'
		
def trailer_one_click():
    if ADDON.getSetting('trailer_one_click') == "true":
        return True
    else:
        return False
	
def tv_directory():
    if ADDON.getSetting('tv_directory')=='set':
        return create_directory(DATA_PATH, "tvshows")
    else:
        return ADDON.getSetting('tv_directory')
	
def movie_directory():
    if ADDON.getSetting('movie_directory')=='set':
        return create_directory(DATA_PATH, "movies")
    else:
        return ADDON.getSetting('movie_directory')
	
def favourites_file():
    return create_file(DATA_PATH, "favourites.list")
	
def favourites_movies_file():
    return create_file(DATA_PATH, "favourites_movies.list")
	
def subscription_file():
    return create_file(DATA_PATH, "subscriptions.list")
		
def cookie_jar():
    return create_file(DATA_PATH, "cookiejar.lwp")
	
def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

create_directory(DATA_PATH)

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

		

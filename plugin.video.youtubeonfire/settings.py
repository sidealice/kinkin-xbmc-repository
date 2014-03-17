import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON = xbmcaddon.Addon(id='plugin.video.youtubeonfire')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.youtubeonfire'), '')

def addon():
    return ADDON

def enable_meta():
    if ADDON.getSetting('enable_meta') == "true":
        return True
    else:
        return False
		
def play_max():
    if ADDON.getSetting('play_max') == "true":
        return True
    else:
        return False
		
def default_sort():
    option = ADDON.getSetting('default_sort')
    if option == '0':
        return 'Score'
    elif option == '1':
        return 'addTime'
    elif option == '2':
        return 'ReleaseDate'
    elif option == '3':
        return 'TomatoFresh'
    else:
        return 'Score'
		
def default_language():
    option = ADDON.getSetting('default_language')
    if option == '0':
        return 'English'
    elif option == '1':
        return 'Korean'
    elif option == '2':
        return 'Chinese'
    elif option == '3':
        return 'Asia'
    if option == '4':
        return 'Thai'
    elif option == '5':
        return 'Malay'
    elif option == '6':
        return 'Indonesian'
    elif option == '7':
        return 'Filipino'
    if option == '8':
        return 'Arabic'
    elif option == '9':
        return 'Hindi'
    elif option == '10':
        return 'Spanish'
    elif option == '11':
        return 'Portuguese'
    if option == '12':
        return 'French'
    elif option == '13':
        return 'German'
    elif option == '14':
        return 'Russian'
    elif option == '15':
        return 'Italian'
    else:
        return 'English'
		
def default_subtitle():
    option = ADDON.getSetting('default_subtitle')
    if option == '0':
        return ''
    if option == '1':
        return 'English'
    elif option == '2':
        return 'Chinese'
    elif option == '3':
        return 'Malay'
    elif option == '4':
        return 'Spanish'
    if option == '5':
        return 'Arabic'
    elif option == '6':
        return 'Korean'
    elif option == '7':
        return 'Thai'
    else:
        return ''
	
def movie_directory():
    if ADDON.getSetting('movie_directory').startswith('special'):
        return create_directory(DATA_PATH, "movies")
    else:
        return ADDON.getSetting('movie_directory')
	
def favourites_file():
    return create_file(DATA_PATH, "favourites.list")
	
def favourites_music_file():
    return create_file(DATA_PATH, "favourites_music.list")
	
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

		

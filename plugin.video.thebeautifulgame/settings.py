import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON = xbmcaddon.Addon(id='plugin.video.thebeautifulgame')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.thebeautifulgame'), '')
WTSN_PATH = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.thebeautifulgame', ''))

def addon():
    return ADDON
	
def favourites_file():
    return create_file(DATA_PATH, "favourites.list")
		
def cookie_jar():
    return create_file(DATA_PATH, "cookiejar.lwp")
	
def force_sd():
    if ADDON.getSetting('force_sd') == "true":
        return True
    else:
        return False
		
def hide_scores():
    option = ADDON.getSetting('hide_scores')
    if option == '0':
        return 'ask'
    elif option == '1':
        return 'hide'
    elif option == '2':
        return 'show'
    else:
        return 'ask'
	
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
		

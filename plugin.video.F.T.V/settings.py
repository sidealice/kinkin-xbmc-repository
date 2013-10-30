import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON = xbmcaddon.Addon(id='plugin.video.F.T.V')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.F.T.V'), '')
ADDON_PATH = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', ''))

def addon():
    return ADDON

def session_id():
    return ADDON.getSetting('session_id')
	
def keep_session_flag():
    return ADDON.getSetting('keep_session_flag')

def filmon_account():
    if ADDON.getSetting('filmon_account') == 'true':
        return True
    else:
        return False
	
def filmon_user():
    return ADDON.getSetting('filmon_user') 

def filmon_pass():
    return ADDON.getSetting('filmon_pass') 

def filmon_quality():
    quality = ADDON.getSetting('filmon_quality')
    if quality == '0':
        return "480p"
    else:
        return "360p"
		
def auto_switch():
    if ADDON.getSetting('auto_switch') == 'true':
        return True
    else:
        return False

def download_path():
    return ADDON.getSetting('download_path')

def my_videos():
    if ADDON.getSetting('my_videos') == 'true':
        return True
    else:
        return False

def my_audio():
    if ADDON.getSetting('my_audio') == 'true':
        return True
    else:
        return False

def other_menu():
    if ADDON.getSetting('other_menu') == 'true':
        return True
    else:
        return False
	
def cookie_jar():
    return create_file(DATA_PATH, "cookiejar.lwp")
	
def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path
		

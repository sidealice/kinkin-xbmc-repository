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
		
def cookie_jar():
    return create_file(TVO_PATH, "cookiejar.lwp")
	
def create_file(dir_path, file_name=None):
    file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path
		

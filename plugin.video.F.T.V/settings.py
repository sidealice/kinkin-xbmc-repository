import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON = xbmcaddon.Addon(id='plugin.video.F.T.V')

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
        return "high"
    else:
        return "low"

def download_path():
    return ADDON.getSetting('download_path')	

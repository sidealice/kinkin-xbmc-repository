import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON = xbmcaddon.Addon(id='plugin.video.smoothschedule')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.smoothschedule'), '')

def timezone():
    timezone = ADDON.getSetting('timezone')
    if timezone == '0':
        return 'America/New York'
    elif timezone == '1':
        return 'America/Los Angeles'
    elif timezone == '2':
        return 'Europe/London'
    elif timezone == '3':
        return 'Europe/Amsterdam'
    else:
        return 'Asia/Hong Kong'
   

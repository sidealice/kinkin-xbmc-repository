#author : kinkin

import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON = xbmcaddon.Addon(id='plugin.video.adblocker')
AD_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.xbmc.ads'), '')

def addon():
    return ADDON
	
def ads_freq():
    freq = ADDON.getSetting('ads_freq')
    if freq == '0':
        return 1
    elif freq == '1':
        return 5
    elif freq == '2':
        return 15
    elif freq == '3':
        return 30
    elif freq == '4':
        return 60
    elif freq == '5':
        return 120
    elif freq == '6':
        return 360
    elif freq == '7':
        return 720
    else:
        return 1080
	
def ads():
    text = ADDON.getSetting('ads_settings_folder')
    if text == "":
        path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.xbmc.ads'), '')
    else:
        path = text
    return path
	
def ads_addon():
    text = ADDON.getSetting('ads_addon')
    if ADDON.getSetting('ads_addon') == "":
        path = xbmcaddon.Addon(id='script.module.xbmc.ads')
    else:
        path = xbmcaddon.Addon(id=text)
    return path
	
def string_1():
    return ADDON.getSetting('string_1')
	
def string_2():
    return ADDON.getSetting('string_1')
	
def string_3():
    return ADDON.getSetting('string_3')
	
def string_4():
    return ADDON.getSetting('string_4')
	
def string_5():
    return ADDON.getSetting('string_5')
	







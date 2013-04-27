'''
Created on 24 feb 2012

@author: Batch
'''
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON = xbmcaddon.Addon(id='plugin.video.XMLbackup')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.XMLbackup'), '')

def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def addon():
    return ADDON

def data_path():
    return DATA_PATH

def backup_path():
    if ADDON.getSetting('backup_custom_directory') == "true":
        return ADDON.getSetting('backup_path')
    else:
        return create_directory(DATA_PATH, "backups")


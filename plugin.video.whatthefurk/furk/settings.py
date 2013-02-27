'''
Created on 24 feb 2012

@author: Batch
'''
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os
import re
ADDON = xbmcaddon.Addon(id='plugin.video.EasyNews')


def addon():
    return ADDON

def MOVIE_FILESIZE():
    quality = ADDON.getSetting('moviefilesize')
    if quality == '0':
        return ''
    elif quality == '1':
        return '18'
    elif quality == '2':
        return '19'
    elif quality == '3':
        return '20'
    elif quality == '4':
        return '21'
    elif quality == '5':
        return '22'
    elif quality == '6':
        return '23'
    elif quality == '7':
        return '24'
    elif quality == '8':
        return '26'
    elif quality == '9':
        return '28'
    elif quality == '10':
        return '39'
    elif quality == '11':
        return '30'
        
        
def TV_FILESIZE():
    quality = ADDON.getSetting('tvfilesize')
    if quality == '0':
        return ''
    elif quality == '1':
        return '18'
    elif quality == '2':
        return '19'
    elif quality == '3':
        return '20'
    elif quality == '4':
        return '21'
    elif quality == '5':
        return '22'
    elif quality == '6':
        return '23'
    elif quality == '7':
        return '24'
    elif quality == '8':
        return '26'
    elif quality == '9':
        return '28'
    elif quality == '10':
        return '39'
    elif quality == '11':
        return '30'

def MOVIE_FILENAME():
    quality = ADDON.getSetting('moviefilename')
    if quality == '0':
        return ''
    elif quality == '1':   
        return 'AVI'
    elif quality == '2':
        return 'MKV'
    elif quality == '3':
        return 'MP4'
    elif quality == '4':
        return 'ISO'
    elif quality == '5':
        return 'DIVX'
    elif quality == '6':
        return 'MPG'
    elif quality == '7':
        return 'FLV'
    elif quality == '8':
        return 'WMV'
    elif quality == '9':
        return 'MOV'
    elif quality == '10':
        return 'ASF'
    elif quality == '11':
        return 'RM'

def TV_FILENAME():
    quality = ADDON.getSetting('tvfilename')
    if quality == '0':
        return ''
    elif quality == '1':   
        return 'AVI'
    elif quality == '2':
        return 'MKV'
    elif quality == '3':
        return 'MP4'
    elif quality == '4':
        return 'ISO'
    elif quality == '5':
        return 'DIVX'
    elif quality == '6':
        return 'MPG'
    elif quality == '7':
        return 'FLV'
    elif quality == '8':
        return 'WMV'
    elif quality == '9':
        return 'MOV'
    elif quality == '10':
        return 'ASF'
    elif quality == '11':
        return 'RM'
        
def BOOST():
    quality = ADDON.getSetting('boost')
    if quality == '0':
        return 'boost4-'
    elif quality == '1':   
        return 'boost1-'
    elif quality == '2':
        return 'boost5-'
    elif quality == '3':
        return ''

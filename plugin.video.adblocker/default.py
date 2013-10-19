'''
kinkin
'''

import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import settings, glob
import time,datetime
from datetime import date

ADDON = settings.addon()
ADS = settings.ads()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.adblocker', 'fanart.jpg'))
image = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.adblocker', 'icon.png'))
audiofile = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.adblocker', 'resources', 'adbusters.mp3'))
ADS_ADDON = settings.ads_addon()
GUISETTING = xbmc.translatePath(os.path.join('special://home/userdata', 'guisettings.xml'))

def WHOYOUGONNACALL():
    addDirFOLDER('Pre-load addons (blocks ad on first-run of addon)','url',2,image)
    addDir('Settings','url',1,image)
	
def preloadaddons():
    addons = os.listdir(addon_path)
    timesetting = str(datetime.datetime.now()).split('.')[0]
    for a in addons:
        xml_path = os.path.join(addon_path, a)
        for xml in glob.glob(os.path.join(xml_path, "addon.xml")):
            text = open(xml, 'r')
            r = text.read()
            text.close()
            try:
                id = strip_text(r, 'id="', '"')
                author = strip_text(r, 'provider-name="', '"')
                xmlid1 = "%s - %s - ad_time" % (author, id)
                xmlid2 = "%s - %s - ga_time" % (author, id)
                ADS_ADDON.setSetting(xmlid1, timesetting)
                ADS_ADDON.setSetting(xmlid2, timesetting)
            except:
                pass
    dialog = xbmcgui.Dialog()
    dialog.ok("Ad Blocker", "", "installed addons pre-loaded")
	
			
def strip_text(r, f, t, excluding=True):
    r = re.search("(?i)" + f + "([\S\s]+?)" + t, r).group(1)
    return r
	
def play_audio():
    xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER).play(audiofile)    

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
		
def addDirFOLDER(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Adbusters Mode: "+str(mode)


if mode==None or url==None or len(url)<1:
        play_audio()
        WHOYOUGONNACALL()
       
elif mode==1:
        ADDON.openSettings()
		
elif mode==2:
        preloadaddons()

		

        
		

xbmcplugin.endOfDirectory(int(sys.argv[1]))

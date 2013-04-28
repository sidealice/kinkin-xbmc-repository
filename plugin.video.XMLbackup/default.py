import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import settings
import shutil, glob

ADDON = settings.addon()
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.XMLbackup', 'fanart.jpg'))
restore_path = os.path.join(xbmc.translatePath('special://profile/addon_data'), '')
restorexbmc_path = os.path.join(xbmc.translatePath('special://profile'), '')
backup_path = settings.backup_path()

def CATEGORIES():
        addDir('Backup','url',1,'')
        addDir('Restore','url',2,'')
        addDir('Set backup path','url',3,'')

#########################  Backup and Restore	#################################################	
def backup_xml(url):
    for xml_file in glob.glob(os.path.join(restorexbmc_path, "*.xml")):
        shutil.copy(xml_file, backup_path)

    directories = os.listdir(restore_path)
    for d in directories:
        create_directory(backup_path, d)
        source = os.path.join(restore_path, d)
        destination = os.path.join(backup_path, d)
        for xml_file in glob.glob(os.path.join(source, "settings.xml")):
            shutil.copy(xml_file, destination)
        for xml_file in glob.glob(os.path.join(source, "*.list")):
            shutil.copy(xml_file, destination)
			
    dialog = xbmcgui.Dialog()
    dialog.ok("XML Backup", "All userdata/*.xml and addon 'settings.xml' files backed up")
    xbmc.executebuiltin('xbmc.activatewindow(0)')

				
def restore_xml(url):
    for xml_file in glob.glob(os.path.join(backup_path, "*.xml")):
        shutil.copy(xml_file, restorexbmc_path)

    directories = os.listdir(backup_path)
    for d in directories:
        source = os.path.join(backup_path, d)
        destination = os.path.join(restore_path, d)
        for xml_file in glob.glob(os.path.join(source, "settings.xml")):
            shutil.copy(xml_file, destination)
        for xml_file in glob.glob(os.path.join(source, "*.list")):
            shutil.copy(xml_file, destination)
			
    dialog = xbmcgui.Dialog()
    if dialog.yesno("XML Backup", "All userdata/*.xml and addon 'settings.xml' files restored", "Reboot to load restored gui settings settings", '', "Reboot Later", "Reboot Now"):
        if xbmc.getCondVisibility('system.platform.windows'):
            xbmc.executebuiltin('RestartApp')
        else:
            xbmc.executebuiltin('Reboot')
    else:
        xbmc.executebuiltin('xbmc.activatewindow(0)')
	
def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


#################################################################################################

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

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        backup_xml(url)
		
elif mode==2:
        print ""+url
        restore_xml(url)
		
elif mode==3:
        print ""+url
        ADDON.openSettings()
        
		

xbmcplugin.endOfDirectory(int(sys.argv[1]))

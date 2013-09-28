import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc
import shutil, glob
import os,fnmatch
import shutil

#ADDON = xbmcaddon.Addon(id='plugin.video.gachecker')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.XMLbackup', 'fanart.jpg'))
check_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
settings_path = os.path.join(xbmc.translatePath('special://home/userdata'), 'addon_data')
packages_path = os.path.join(xbmc.translatePath('special://home/addons'), 'packages')


                  												  
def CATEGORIES():
    list = []
    directories = os.listdir(check_path)
    for d in directories:
        if d != "plugin.video.gachecker":
            addonpath = os.path.join(check_path, d)
            for py_file in glob.glob(os.path.join(addonpath, "*.py")):
                text = read_from_file(py_file)
                if text.find('google-analytics') > 0 or text.find('GA(') > 0 or text.find('UA-') > 0:
                    cnt = text.count('GA(') + 1
                    #list.append(d)
                    addDir('[COLOR cyan]'+ d + '[/COLOR]' + " (GA tracking " + str(cnt) + " events)",d,2,'','list addons')
            directories = os.listdir(addonpath)
            for sd in directories:
                subd = os.path.join(check_path, d, sd)
                for py_file in glob.glob(os.path.join(subd, "*.py")):
                    text = read_from_file(py_file)
                    if text.find('google-analytics') > 0 or text.find('GA(') > 0 or text.find('UA-') > 0:
                        #list.append(d)
                        cnt = text.count('GA(') + 1
                        addDir('[COLOR cyan]'+ d + '[/COLOR]' + " (GA tracking " + str(cnt) + " events)",d,2,'','list addons')
                if os.path.isdir(subd):
                    directories = os.listdir(subd)
                    for sd2 in directories:
                        subd2 = os.path.join(check_path, d, sd, sd2)
                        for py_file in glob.glob(os.path.join(subd2, "*.py")):
                            text = read_from_file(py_file)
                            if text.find('google-analytics') > 0 or text.find('GA(') > 0 or text.find('UA-') > 0:
                                #list.append(d)
                                cnt = text.count('GA(') + 1
                                addDir('[COLOR cyan]'+ d + '[/COLOR]' + " (GA tracking " + str(cnt) + " events)",d,2,'','list addons')
                        if os.path.isdir(subd2):
                            directories = os.listdir(subd2)
                            for sd3 in directories:
                                subd3 = os.path.join(check_path, d, sd, sd2, sd3)
                                for py_file in glob.glob(os.path.join(subd3, "*.py")):
                                    text = read_from_file(py_file)
                                    if text.find('google-analytics') > 0 or text.find('GA(') > 0 or text.find('UA-') > 0:
                                        cnt = text.count('GA(') + 1
                                        #list.append(d)
                                        addDir('[COLOR cyan]'+ d + '[/COLOR]' + " (GA tracking " + str(cnt) + " events)",d,2,'','list addons')

        						
    #for l in list:
        #addDir(l,l,2,'','list addons')
    #if len(list) == 0:
        #addDir("No Google Analytics found","",1,'','list addons')


def remove_single(url):
    dialog = xbmcgui.Dialog()
    if dialog.yesno(url, "Do you want to remove this addon?"):
        urld = os.path.join(check_path, url)
        shutil.rmtree(urld)
		
        if dialog.yesno(url + "settings", "Do you want to remove this addon's settings?"):
            urld = os.path.join(settings_path, url)
            if os.path.exists(urld):
                shutil.rmtree(urld)
            else:
                dialog.ok(url + " settings", "", "No settings directories found")
		
        if dialog.yesno(url + "zip files", "Do you want to remove this addon's zip files?"):
            #urld = os.path.join(packages_path, url)
            for package in glob.glob(os.path.join(packages_path, url + "*")):
                os.remove(package)

        xbmc.executebuiltin("Container.Refresh")
	
def read_from_file(path, silent=False):
    try:
        f = open(path, 'r')
        r = f.read()
        f.close()
        return str(r)
    except:
        if not silent:
            print("Could not read from " + path)
        return None


   
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

       
def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

		

def addLink(name,url,iconimage,description):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok 
 
        
               
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
		
elif mode==2:
        print ""+url
        remove_single(url)
		
elif mode==3:
        print ""+url
        remove_all(url)
        

       
xbmcplugin.endOfDirectory(int(sys.argv[1]))

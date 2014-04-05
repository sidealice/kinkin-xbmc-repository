'''
kinkin
'''

import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import settings
import time,datetime
from datetime import date, timedelta
from threading import Timer
from helpers import clean_file_name
import json
import glob
import shutil
from threading import Thread
import cookielib
from t0mm0.common.net import Net
from helpers import clean_file_name
net = Net()


ADDON = settings.addon()
FAV = settings.favourites_file()
HIDE_PLUTO = settings.hide_pluto_vid()
cookie_jar = settings.cookie_jar()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.plutotv', 'fanart.jpg'))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.plutotv', 'icon.png'))
base_url = 'http://pluto.tv/'


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
	
def GET_URL(url):
    header_dict = {}
    header_dict['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    header_dict['Host'] = 'cdn-api.prod.pluto.tv'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Referer'] = base_url
    header_dict['Origin'] = base_url
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    net.set_cookies(cookie_jar)
    trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
    req = net.http_GET(url, headers=header_dict).content.translate(trans_table).rstrip()
    net.save_cookies(cookie_jar)
    return req
	
def CATEGORIES(name):
    addDir("All Channels", 'http://cdn-api.prod.pluto.tv/v1/channels.json',1,iconart, '','')
    addDir("Music", 'http://cdn-api.prod.pluto.tv/v1/channels.json',1,iconart, '','')
    addDir("News & Info", 'http://cdn-api.prod.pluto.tv/v1/channels.json',1,iconart, '','')
    addDir("Sports", 'http://cdn-api.prod.pluto.tv/v1/channels.json',1,iconart, '','')
    addDir("Entertainment", 'http://cdn-api.prod.pluto.tv/v1/channels.json',1,iconart, '','')
    addDir("Comedy", 'http://cdn-api.prod.pluto.tv/v1/channels.json',1,iconart, '','')	
    addDir("Lifestyle", 'http://cdn-api.prod.pluto.tv/v1/channels.json',1,iconart, '','')
    addDir("Tech", 'http://cdn-api.prod.pluto.tv/v1/channels.json',1,iconart, '','')
    addDir("Art & Culture", 'http://cdn-api.prod.pluto.tv/v1/channels.json',1,iconart, '','')
    addDir("Education", 'http://cdn-api.prod.pluto.tv/v1/channels.json',1,iconart, '','')
    addDir("Kids", 'http://cdn-api.prod.pluto.tv/v1/channels.json',1,iconart, '','')
    addDir("Favourite Videos", 'url',9,iconart, '','')

def all_channels(chname,url):
    link = GET_URL(url)
    match = re.compile('{"_id":"(.+?)","category":"(.+?)","description":"(.+?)","hash":"(.+?)","name":"(.+?)","number":(.+?)}').findall(link)
    for id,cat,plot,hash,name,number in match:
        if chname == "All Channels":
            title = "%s - %s: %s" % (cat,number,name)
            addDirPlayable(title,id,2,iconart,plot)
        elif chname == cat:
            title = "%s: %s" % (number,name)
            addDirPlayable(title,id,2,iconart,plot)
    setView('episodes', 'episodes-view')
	
def channel_schedule(name,url,iconimage):
    i = datetime.datetime.now()
    i2 = datetime.datetime.now() + timedelta(hours=8)
    t1 = i.strftime('%Y-%m-%dT%H:00:00')
    t2 = i2.strftime('%Y-%m-%dT%H:00:00')
    url1='http://cdn-api.prod.pluto.tv/v1/timelines/%s.000Z/%s.000Z/matrix.json' % (t1,t2)
    link = GET_URL(url1).replace('[', '<<').replace(']', '>>')
    ch_start = "%s%s" % ( url,'":<<')
    channel_info = regex_from_to(link,ch_start, ">>")
    id2 = regex_get_all(channel_info, '"_id":"', '}}')
    for i in id2:
        start=regex_from_to(regex_from_to(i,'start":"','"'),'T', ':00.000Z')
        stop=regex_from_to(regex_from_to(i,'stop":"','"'),'T', ':00.000Z')
        id='sched' + regex_from_to(i,'episode":{"_id":"','"')
        plot=regex_from_to(i,'description":"','"')
        name=regex_from_to(i,'name":"','"')
        title = "%s-%s  %s" % (start,stop,name)
        addDirPlayable(title,id,2,iconart,plot)
    setView('episodes', 'episodes-view')
        
def play_channel(name,url,iconimage,clear):
    if not 'sched' in url:
        i = datetime.datetime.now()
        i2 = datetime.datetime.now() + timedelta(hours=8)
        t1 = i.strftime('%Y-%m-%dT%H:00:00')
        t2 = i2.strftime('%Y-%m-%dT%H:00:00')
        url1='http://cdn-api.prod.pluto.tv/v1/timelines/%s.000Z/%s.000Z/matrix.json' % (t1,t2)
        link = GET_URL(url1).replace('[', '<<').replace(']', '>>')
        ch_start = "%s%s" % ( url,'":<<')
        channel_info = regex_from_to(link,ch_start, ">>")
        id = regex_from_to(channel_info, 'episode":{"_id":"', '"')
    else:
        id = url.replace('sched','')
    dp = xbmcgui.DialogProgress()
    dp.create("Pluto.TV",'Creating Your Channel')
    dp.update(0)
    playlist=[]
    url = 'http://cdn-api.prod.pluto.tv/v1/episodes/%s/clips.json' % id
    link = GET_URL(url)
    data = json.loads(link)
    nItem=len(data)
    pl = get_XBMCPlaylist(clear)
    for field in data:
        video_id = field['code']
        name = field['name']
        iconimage = 'https://i1.ytimg.com/vi/%s/hqdefault.jpg' % video_id
        url = str('plugin://plugin.video.youtube/?action=play_video&videoid=' +  video_id)
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo('video', {'Title':name})
        liz.setThumbnailImage(iconimage)
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        if HIDE_PLUTO==False or (HIDE_PLUTO==True and 'Pluto.TV' not in name and 'PlutoTV' not in name and name != 'Music 15 3'):
            playlist.append((url, liz))
            progress = len(playlist) / float(nItem) * 100               
            dp.update(int(progress), 'Adding to channel',name)
            if dp.iscanceled():
                return
    for blob,liz in playlist:
        try:
            if blob:
                pl.add(blob, liz)
        except:
            pass
    if clear or (not xbmc.Player().isPlayingVideo()):
        handle = str(sys.argv[1])    
        if handle != "-1":
            liz.setProperty("IsPlayable", "true")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        else:
            try:
                xbmc.Player().play(pl)
            except:
                pass
			
def browse_channel(name,url,iconimage,clear):
    if not 'sched' in url:
        i = datetime.datetime.now()
        i2 = datetime.datetime.now() + timedelta(hours=8)
        t1 = i.strftime('%Y-%m-%dT%H:00:00')
        t2 = i2.strftime('%Y-%m-%dT%H:00:00')
        url1='http://cdn-api.prod.pluto.tv/v1/timelines/%s.000Z/%s.000Z/matrix.json' % (t1,t2)
        link = GET_URL(url1).replace('[', '<<').replace(']', '>>')
        ch_start = "%s%s" % ( url,'":<<')
        channel_info = regex_from_to(link,ch_start, ">>")
        id = regex_from_to(channel_info, 'episode":{"_id":"', '"')
    else:
        id = url.replace('sched','')
    dp = xbmcgui.DialogProgress()
    dp.create("Pluto.TV",'Creating Your Channel')
    dp.update(0)
    playlist=[]
    url = 'http://cdn-api.prod.pluto.tv/v1/episodes/%s/clips.json' % id
    link = GET_URL(url)
    data = json.loads(link)
    nItem=len(data)
    pl = get_XBMCPlaylist(clear)
    for field in data:
        video_id = field['code']
        name = field['name']
        iconimage = 'https://i1.ytimg.com/vi/%s/hqdefault.jpg' % video_id 
        url = str('plugin://plugin.video.youtube/?action=play_video&videoid=' +  video_id)
        if HIDE_PLUTO==False or (HIDE_PLUTO==True and 'Pluto.TV' not in name and 'PlutoTV' not in name and name != 'Music 15 3'):
            addDirPlayable(name,url,5,iconimage,'')   
            liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
            liz.setInfo('video', {'Title':name})
            liz.setThumbnailImage(iconimage)
            liz.setProperty('fanart_image', fanart)
            liz.setProperty("IsPlayable","true")
            playlist.append((url, liz))

def play_video(name,url,iconimage,clear):
    if 'TEST' in iconimage:
        video_id = regex_from_to(url,'https://i1.ytimg.com/vi/','/hq')
        url=str('plugin://plugin.video.youtube/?action=play_video&videoid=' +  video_id)
        iconimage = url
    playlist=[]
    pl = get_XBMCPlaylist(clear)
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo('video', {'Title':name})
    liz.setThumbnailImage(iconimage)
    liz.setProperty('fanart_image', fanart)
    liz.setProperty("IsPlayable","true")
    playlist.append((url, liz))
    for blob,liz in playlist:
        try:
            if blob:
                pl.add(blob, liz)
        except:
            pass
    if clear or (not xbmc.Player().isPlayingVideo()):
        handle = str(sys.argv[1])    
        if handle != "-1":
            liz.setProperty("IsPlayable", "true")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        else:
            xbmc.Player().play(pl)

def get_XBMCPlaylist(clear):
    pl=xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    if clear:
        pl.clear()
    return pl	   

def search():
    keyboard = xbmc.Keyboard('', 'Search TV Show', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            search_show(query)
			

def favourites():
    if os.path.isfile(FAV):
        s = read_from_file(FAV)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                title = title.replace('->-', ' & ')
                url = list1[1]
                thumb = list1[1]
                video_id = regex_from_to(url,'https://i1.ytimg.com/vi/', '/hqdefault.jpg') 
                url = str('plugin://plugin.video.youtube/?action=play_video&videoid=' +  video_id)
                addDirPlayable(title,url,5,thumb,'fav')
				
	
def add_favourite(name, url, iconimage, dir, text):
    list_data = "%s<>%s<>%s" % (name,url,iconimage)
    add_to_list(list_data, dir)
    notification(name, "[COLOR lime]" + text + "[/COLOR]", '4000', url)
	
def remove_from_favourites(name, url, iconimage, dir, text):
    list_data = "%s<>%s<>%s" % (name,url,iconimage)
    remove_from_list(list_data, dir)
    notification(name, "[COLOR orange]" + text + "[/COLOR]", '4000', url)
		
def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path
	
def create_strm_file(name, url, mode, dir_path, iconimage, showname):
    try:
        strm_string = create_url(name, mode, url=url, iconimage=iconimage, showname=showname)
        filename = clean_file_name("%s.strm" % name)
        path = os.path.join(dir_path, filename)
        if not os.path.exists(path):
            stream_file = open(path, 'w')
            stream_file.write(strm_string)
            stream_file.close()
    except:
        xbmc.log("[TVonline] Error while creating strm file for : " + name)
		
def create_url(name, mode, url, iconimage, showname):
    name = urllib.quote(str(name))
    data = urllib.quote(str(url))
    iconimage = urllib.quote(str(iconimage))
    showname = urllib.quote(str(showname))
    mode = str(mode)
    url = sys.argv[0] + '?name=%s&url=%s&mode=%s&iconimage=%s&showname=%s' % (name, data, mode, iconimage, showname)
    return url
	
def get_subscriptions():
    try:
        if os.path.isfile(SUB):
            s = read_from_file(SUB)
            search_list = s.split('\n')
            for list in search_list:
                if list != '':
                    list1 = list.split('QQ')
                    title = list1[0]
                    url = list1[1]
                    thumb = list1[2]
                    create_tv_show_strm_files(title, url, list, "false")
    except:
        xbmc.log("[TVonline] Failed to fetch subscription")

def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r

def strip_text(r, f, t, excluding=True):
    r = re.search("(?i)" + f + "([\S\s]+?)" + t, r).group(1)
    return r


def find_list(query, search_file):
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        index = lines.index(query)
        return index
    except:
        return -1
		
def add_to_list(list, file):
    if find_list(list, file) >= 0:
        return

    if os.path.isfile(file):
        content = read_from_file(file)
    else:
        content = ""

    lines = content.split('\n')
    s = '%s\n' % list
    for line in lines:
        if len(line) > 0:
            s = s + line + '\n'
    write_to_file(file, s)
    xbmc.executebuiltin("Container.Refresh")
    
def remove_from_list(list, file):
    index = find_list(list, file)
    if index >= 0:
        content = read_from_file(file)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        write_to_file(file, s)
        xbmc.executebuiltin("Container.Refresh")
		
def write_to_file(path, content, append=False, silent=False):
    try:
        if append:
            f = open(path, 'a')
        else:
            f = open(path, 'w')
        f.write(content)
        f.close()
        return True
    except:
        if not silent:
            print("Could not write to " + path)
        return False

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

def wait_dl_only(time_to_wait, title):
    print 'Waiting ' + str(time_to_wait) + ' secs'    

    progress = xbmcgui.DialogProgress()
    progress.create(title)
    
    secs = 0
    percent = 0
    
    cancelled = False
    while secs < time_to_wait:
        secs = secs + 1
        percent = int((100 * secs) / time_to_wait)
        secs_left = str((time_to_wait - secs))
        remaining_display = ' waiting ' + secs_left + ' seconds for download to start...'
        progress.update(percent, remaining_display)
        xbmc.sleep(1000)
        if (progress.iscanceled()):
            cancelled = True
            break
    if cancelled == True:     
        print 'wait cancelled'
        return False
    else:
        print 'Done waiting'
        return True

		
def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
	
def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
   

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


def addDir(name,url,mode,iconimage,list,description):
        suffix = ""
        suffix2 = ""
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+str(iconimage)+"&list="+str(list)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name + suffix + suffix2, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description })
        liz.setProperty('fanart_image', fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirPlayable(name,url,mode,iconimage,showname):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&showname="+urllib.quote_plus(showname)
        ok=True
        contextMenuItems = []
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': showname })
        liz.setProperty('fanart_image', fanart )
        if not 'plugin' in url:
            contextMenuItems.append(("[COLOR lime]Channel Schedule[/COLOR]",'XBMC.Container.Update(%s?name=%s&url=%s&mode=7&iconimage=%s&showname=%s)'%(sys.argv[0],name, url, iconimage,showname)))
            contextMenuItems.append(("[COLOR lime]Queue Channel[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=3&iconimage=%s&showname=%s)'%(sys.argv[0],name, url, iconimage,showname)))
            contextMenuItems.append(("[COLOR lime]Browse Channel[/COLOR]",'XBMC.Container.Update(%s?name=%s&url=%s&mode=4&iconimage=%s&showname=%s)'%(sys.argv[0],name, url, iconimage,showname)))
        if 'plugin' in url:
            contextMenuItems.append(("[COLOR lime]Queue Video[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=6&iconimage=%s&showname=%s)'%(sys.argv[0],name, iconimage, "TEST",'video')))
            if showname != 'fav':
                contextMenuItems.append(("[COLOR lime]Save Video to Favourites[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=8&iconimage=%s&showname=%s)'%(sys.argv[0],name, iconimage, "TEST",'video')))
            if showname == 'fav':
                contextMenuItems.append(("[COLOR orange]Remove from Favourites[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=10&iconimage=%s&showname=%s)'%(sys.argv[0],name, iconimage, "TEST",'video')))        
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
		

params=get_params()

url=None
name=None
mode=None
iconimage=None



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
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        start=urllib.unquote_plus(params["start"])
except:
        pass
try:
        list=urllib.unquote_plus(params["list"])
except:
        pass
try:
        showname=str(params["showname"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass


if mode==None or url==None or len(url)<1:
        CATEGORIES(name)
		
elif mode==1:
        all_channels(name,url)
        
elif mode==2:
        play_channel(name,url,iconimage,True)
		
elif mode==3:
        play_channel(name,url,iconimage,False)
		
elif mode==4:
        browse_channel(name,url,iconimage,False)
		
elif mode==5:
        play_video(name, url, iconimage,True)
		
elif mode==6:
        play_video(name, url, iconimage,False)
		
elif mode==7:
        channel_schedule(name,url,iconimage)
		
elif mode==8:
        add_favourite(name, url, iconimage, FAV, "Added to Favourites")
		
elif mode == 9:
        favourites()
		
elif mode == 10:
        remove_from_favourites(name, url, iconimage, FAV, "Removed from Favourites")
		
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))



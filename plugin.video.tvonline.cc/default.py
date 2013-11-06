'''
kinkin
'''

import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import settings
import time,datetime
from datetime import date
from threading import Timer
from hashlib import md5
from helpers import clean_file_name
import json
import glob
from threading import Thread
import cookielib
from t0mm0.common.net import Net
from helpers import clean_file_name
net = Net()


ADDON = settings.addon()
TVO_USER = settings.tvo_user()
TVO_PASSWORD = settings.tvo_pass()
cookie_jar = settings.cookie_jar()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'Fanart2.jpg'))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'icon.png'))
base_url = 'http://www.tvonline.cc/'


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
def POST_URL(url, form_data):
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    header_dict['Host'] = 'www.tvonline.cc'
    header_dict['Referer'] = 'http://www.tvonline.cc/'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    net.set_cookies(cookie_jar)
    req = net.http_POST(url, form_data=form_data, headers=header_dict).content.encode("utf-8").rstrip()
    return req

def startup():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Setup account", "This addon requires a tvonline.cc account.", "What do you want to do?", '', "Use existing account", "Create new account"):
        register()
    else:
        keyboard = xbmc.Keyboard('', 'Username', False)
        keyboard.doModal()
        username = None
        if keyboard.isConfirmed() and len(keyboard.getText()) > 1:
            username = keyboard.getText()
            password = None
            keyboard = xbmc.Keyboard('', 'Password')
            keyboard.doModal()
            if keyboard.isConfirmed() and len(keyboard.getText()) > 1:
                password = keyboard.getText()
                ADDON.setSetting('tvo_user', value=username)
                ADDON.setSetting('tvo_pass', value=password)
                time.sleep(1)
                xbmc.executebuiltin("XBMC.Container.Update(plugin://plugin.video.tvonline.cc)")
            else:
                return
        else:
            return
        
def register():    
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'www.tvonline.cc'
    header_dict['Referer'] = 'http://www.tvonline.cc/'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
    header_dict['Connection'] = 'keep-alive'#
    #### Get token ###
    net.set_cookies(cookie_jar)
    url = 'http://www.tvonline.cc/reg.php'
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)

    tokenparam = re.compile('value="POST"><input type="hidden" name="(.+?)" value="(.+?)" id').findall(link)
    tokenfields = re.compile('name="(.+?)" value="(.+?)" id="(.+?)"></div></form>').findall(link)
    for a, b, c in tokenfields:
        field = a
        fieldvalue = b
    for a, b in tokenparam:
        param1 = a
        param1value = b
    header_dict['Referer'] = 'http://www.tvonline.cc/reg.php'
    ### Register ###
    keyboard = xbmc.Keyboard('', 'Username', False)
    keyboard.doModal()
    username = None
    if keyboard.isConfirmed() and len(keyboard.getText()) > 1:
        username = keyboard.getText()

        password = None
        keyboard = xbmc.Keyboard('', 'Password')
        keyboard.doModal()
        if keyboard.isConfirmed() and len(keyboard.getText()) > 1:
            password = keyboard.getText()
			
            email = None
            keyboard = xbmc.Keyboard('', 'E-mail')
            keyboard.doModal()
            if keyboard.isConfirmed() and len(keyboard.getText()) > 1:
                email = keyboard.getText()
            else:
                return
        else:
            return
    else:
        return

    ### Save settings ###
    ADDON.setSetting('tvo_user', value=username)
    ADDON.setSetting('tvo_pass', value=password)
	
    form_data = ({param1: param1value, 'UserUsername': username, '_method': 'POST', field: fieldvalue, 'email': email, 'subscriptionsPass': password, 'subscriptionsPassword2': password})	
    net.set_cookies(cookie_jar)
    reglink = net.http_POST('http://www.tvonline.cc/reg.php', form_data=form_data, headers=header_dict).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    if 'Invalid Username/Email or password' in reglink:
        notification('[COLOR red]Not logged in at tvonline.cc[/COLOR]', 'Check settings', '5000', iconart)
    else:
        notification('Logged in at tvonline.cc', '', '5000', iconart)
		
def login():
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'www.tvonline.cc'
    header_dict['Referer'] = 'http://www.tvonline.cc/'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
    header_dict['Connection'] = 'keep-alive'#
    #### Get token ###
    net.set_cookies(cookie_jar)
    url = 'http://www.tvonline.cc/login.php'
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)

    tokenparam = re.compile('value="POST"><input type="hidden" name="(.+?)"').findall(link)
    tokenfields = re.compile('name="(.+?)" value="(.+?)" id="(.+?)"></div></form>').findall(link)
    for a, b, c in tokenfields:
        field = a
        fieldvalue = b
    param1 = tokenparam[0]
    header_dict['Referer'] = 'http://www.tvonline.cc/login.php'
    ### Login ###	
    form_data = ({param1: 'login', 'UserUsername': TVO_USER, '_method': 'POST', field: fieldvalue, 'subscriptionsPass': TVO_PASSWORD})	
    net.set_cookies(cookie_jar)
    loginlink = net.http_POST('http://www.tvonline.cc/reg.php', form_data=form_data, headers=header_dict).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    if 'Invalid Username/Email or password' in loginlink:
        notification('[COLOR red]Not logged in at tvonline.cc[/COLOR]', 'Check settings', '5000', iconart)
        startup()
    else:
        notification('Logged in at tvonline.cc', '', '5000', iconart)
	
def CATEGORIES(name):
    if name == None:
        login()
    addDir("Hit TV Shows", 'Hit TV Shows',7,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'HitTVShows.png')), '','')
    addDir("Latest Updates", 'Latest Updates TV Shows',7,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'Latestupdates.png')), '','')
    addDir("Shows with New Episodes", 'New TV Episodes',7,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'NewEpisodes.png')), '','')
    addDir("A-Z", 'url',8,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'A-Z.png')), '','')
    addDir("Search", 'url',6,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'search2.png')), '','')
    addDir("My Watched List", 'http://www.tvonline.cc/wl.php?page=1',9,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'Watchedlist.png')), '','')	

def search():
    keyboard = xbmc.Keyboard('', 'Search TV Show', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            search_show(query)
			
def a_to_z(url):
    alphabet =  ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
    for a in alphabet:
        addDir(a, 'http://www.tvonline.cc/tv/%s.htm' % (a.lower().replace('#', 'num')),2,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', a.replace('#','HASH') + '.png')), '','')
			
def search_show(query):
    url = 'http://www.tvonline.cc/searchlist.php'
    form_data = ({'keyword': query})
    req = POST_URL(url, form_data)
    all_shows = regex_from_to(req,'<br /> <br />', '</div>')
    all_shows = regex_get_all(all_shows, '<li>', '</li>')
    for a in all_shows:
        url = 'http://www.tvonline.cc' + regex_from_to(a, '<a href="', '" title')
        title = regex_from_to(a, 'title="', ' "').replace('Watch free ','')
        thumb = regex_from_to(a, '<img src="', '" ')
        addDir(title, url,3,thumb, '','')
		
def watched_list(url):
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    match = re.compile('<td><a href="(.+?)">(.+?)</a></td>  <td>(.+?)</td>').findall(link.replace("'", "<>"))
    matchpg = re.compile('<a class="p_num" href="(.+?)">(.+?)</a>').findall(link)
    addDir('[COLOR cyan] << Return to Main Menu [/COLOR]', '','','', '','')
    for url, episode, wtime in match:
        url = 'http://www.tvonline.cc' + url.replace("<>", "'")
        name = "%s -%s" % (episode.replace("<>", "'"), wtime)
        showname = episode[:len(episode)-7]
        iconimage = "http://pic.newtvshows.org/" + showname.replace(' ', '-') + ".jpg"
        addDirPlayable(name,url,5,iconimage, showname)
    for url, page in matchpg:
        url = 'http://www.tvonline.cc/wl.php' + url
        title = '[COLOR lime]' + 'Page ' + str(page) + '[/COLOR]'
        addDir(title, url,9,'', '','')
    setView('episodes', 'episodes-view')
		
def shows(url):
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    all_shows = regex_from_to(link,'<br /> <br />', '</div>')
    all_shows = regex_get_all(all_shows, '<li>', '</li>')
    for a in all_shows:
        url = 'http://www.tvonline.cc' + regex_from_to(a, '<a href="', '" title')
        title = regex_from_to(a, 'title="', ' "').replace('Watch free ','')
        thumb = regex_from_to(a, '<img src="', '" ')
        addDir(title, url,3,thumb, '','')
    setView('episodes', 'episodes-view')
		
def grouped_shows(header):
    url = 'http://www.tvonline.cc'
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    all_shows = regex_from_to(link,str(header), '</ul>')
    all_shows = regex_get_all(all_shows, '<li>', '</li>')
    for a in all_shows:
        url = 'http://www.tvonline.cc' + regex_from_to(a, '<a href="', '" title')
        title = regex_from_to(a, 'title="', ' "').replace('Watch free ','')
        if header == "Hit TV Shows":
            try:
                thumb = "http://pic.newtvshows.org/" + title.replace(' ', '-') + ".jpg"
            except:
                thumb = "http://pic.newtvshows.org/" + title.replace(' ', '.') + ".jpg"
        else:
            thumb = regex_from_to(a, '<img src="', '" ')
        addDir(title, url,3,thumb, '','')
    setView('episodes', 'episodes-view')
		
def tv_show(name, url, iconimage):
    episodes = []
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    seasonlist = regex_get_all(link.replace("'", "<>"), '<ul class="ju_list"', '</ul>')
    for s in seasonlist:
        sname = regex_from_to(s, '<strong>', '</strong>').replace(':', '')
        eplist = regex_get_all(str(s), '<li>', '</li>')
        addDir(sname, 'url',4,str(iconimage), eplist,name)
    setView('episodes', 'episodes-view')
		
def tv_show_episodes(name, list, iconimage, showname):
    episodes = re.compile('<li>(.+?):<a href="(.+?)">(.+?)</a></li>').findall(list)
    for epnum, url, epname in episodes:
        epnum = epnum.replace(', ', '-').replace('Ep', 'E')
        url = 'http://www.tvonline.cc' + url.replace("<>", "'")
        name = "%s - %s" % (epnum, clean_file_name(epname))
        addDirPlayable(name,url,5,iconimage, showname)
    setView('episodes', 'episodes-view')
		
def play(name, url, iconimage, showname):
    dp = xbmcgui.DialogProgress()
    dp.create('Opening ' + name)
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    linkurl = 'http://www.tvonline.cc' + regex_from_to(link, 'url: "', '"')
    net.set_cookies(cookie_jar)
    playlink = net.http_GET(linkurl).content.encode("utf-8").rstrip()
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    listitem = xbmcgui.ListItem(showname + ' ' + name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    playlist.add(playlink,listitem)
    xbmcPlayer = xbmc.Player()
    try:
        xbmcPlayer.play(playlist)
    except:
        dialog = xbmcgui.Dialog()
        dialog.ok("Playback failed", "Check your account settings")
    dp.close()
        
		
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
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&list="+str(list)+"&description="+str(description)
        ok=True
        contextMenuItems = []
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirPlayable(name,url,mode,iconimage,showname):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&showname="+urllib.quote_plus(showname)
        ok=True
        #contextMenuItems = []
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
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
        showname=urllib.unquote_plus(params["showname"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass


if mode==None or url==None or len(url)<1:
        CATEGORIES(name)
        
       
elif mode==2:
        shows(url)
		
elif mode==3:
        tv_show(name, url, iconimage)
		
elif mode==4:
        tv_show_episodes(name, list, iconimage, description)
		
elif mode==5:
        play(name, url, iconimage, showname)
		
elif mode==6:
        search()
		
elif mode==7:
        grouped_shows(url)
		
elif mode == 8:
        a_to_z(url)
		
elif mode == 9:
        watched_list(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))



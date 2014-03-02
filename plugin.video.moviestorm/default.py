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
import shutil
from threading import Thread
import cookielib
from t0mm0.common.net import Net
from helpers import clean_file_name
net = Net()


ADDON = settings.addon()
MS_USER = settings.ms_user()
MS_PASSWORD = settings.ms_pass()
MS_EMAIL = settings.ms_email()
ENABLE_SUBS = settings.enable_subscriptions()
TV_PATH = settings.tv_directory()
MOVIE_PATH = settings.movie_directory()
FAV = settings.favourites_file()
SUB = settings.subscription_file()
cookie_jar = settings.cookie_jar()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'fanart.jpg'))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'icon.png'))
base_url = 'http://www.moviestorm/'


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
def login():
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'moviestorm.eu'
    header_dict['Referer'] = 'http://moviestorm.eu/login'
    header_dict['User-Agent'] = 'AppleWebKit/<WebKit Rev>'
    header_dict['Connection'] = 'keep-alive'#

    ### Login ###
    if MS_USER != '':
        form_data = ({'login': 'Login', 'email': MS_EMAIL, 'password': MS_PASSWORD})	
        net.set_cookies(cookie_jar)
        loginlink = net.http_POST('http://moviestorm.eu/login', form_data=form_data, headers=header_dict).content.encode("utf-8").rstrip()
        net.save_cookies(cookie_jar)

def request_video():
    keyboard = xbmc.Keyboard('', 'Movie/TV Show Name', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        movie = keyboard.getText()
        if len(movie) > 0:
            keyboard = xbmc.Keyboard('', 'Season/Episode (optional)', False)
            keyboard.doModal()
            if keyboard.isConfirmed():
                option = keyboard.getText()
                form_data = ({'email': MS_EMAIL, 'name': movie, 'optional': option, 'request': 'Send'})
                link = request_POST(form_data)
                notification(movie, 'requested', '5000', iconart)
        else:
            return
    else:
        return
			
def request_POST(form_data):
    url = 'http://moviestorm.eu/request'
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'moviestorm.eu'
    header_dict['Referer'] = 'http://moviestorm.eu/request'
    header_dict['User-Agent'] = 'AppleWebKit/<WebKit Rev>'
    header_dict['Connection'] = 'keep-alive'#

    ### Login ###
    if MS_USER != '':
        net.set_cookies(cookie_jar)
        requestlink = net.http_POST(url, form_data=form_data, headers=header_dict).content.encode("utf-8").rstrip()
        net.save_cookies(cookie_jar)
        return requestlink
	
def CATEGORIES(name):
    login()
    addDir("Movies", 'url',101,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'movies.png')), '','')
    addDir("TV Series", 'url',102,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'tvseries.png')), '','')
    addDir("TV Shows", 'http://moviestorm.eu/tv_shows',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'tvshows.png')), '','')
    addDir("Genres", 'http://moviestorm.eu/movies',106,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'genres.png')), '','')
    addDir("Search", 'url',6,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'search.png')), '','')
    addDir("My Subscriptions", 'url',16,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'subs.png')), '','')
    addDir("My Favourites", 'url',12,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'favourites.png')), '','')
    if MS_EMAIL != "":
         addDirPlayable("Request a Movie/Show", 'url',18,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'request.png')), '')
		 
def genres(url):    
    link = open_url(url)
    all_genres = regex_from_to(link, '<li><a>Genres</a>', '</ul>')
    match = re.compile('<a href="(.+?)">(.+?)</a>').findall(all_genres)
    for url, name in match:
        if name != 'Adult':
            addDir(name, url,1,'', '','')

def movie_menu():
    addDir("New", 'http://moviestorm.eu/movies',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'new.png')), '','')
    addDir("Popular", 'http://moviestorm.eu/movies/popular',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'popular.png')), '','')
    addDir("In Theatres", 'http://moviestorm.eu/movies/intheaters',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'theatres.png')), '','')

def tvseries_menu():
    addDir("New Episodes", 'http://moviestorm.eu/series/newepisodes/',5,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'new.png')), '','')
    addDir("Popular", 'http://moviestorm.eu/series/popular/',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'popular.png')), '','')
    addDir("All Series", 'http://moviestorm.eu/series/all/',107,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviestorm', 'art', 'allseries.png')), '','')    

def Main(url):
    addDir('[COLOR cyan] << Return to Main Menu [/COLOR]', '','','', '', '')
    f_url = url.find('?pages=')
    if f_url == -1:
        origurl = url
    else:
        origurl=url[:f_url]
    link = open_url(url)
    movies = regex_get_all(link, '<div class="movie_box', '</div>')
    for m in movies:
        title = regex_from_to(m, '<h1>', '</h1>')
        url = regex_from_to(m, '<a href="', '"')
        thumb = regex_from_to(m, 'src="', '"')
        list_data = "%sQQ%sQQ%s" % (title.replace(' & ', '->-').replace(':', ''), url, thumb)
        addDir(title, url,2,thumb, list_data,'sh')
    if '<div class="pagestring">' in link:
        pager = regex_from_to(link, '<div class="pagestring">', '</div>')
        pages = re.compile('<a href="(.+?)pages=(.+?)">(.+?)</a>').findall(pager)
        if len(pages)==0:
            url = origurl + '?pages=1'
            text = '[COLOR lime]' + 'Page 2' + '[/COLOR]'
            addDir(text, url,1,thumb, '','')
        else:
            for q, url, text in pages:
                url = origurl + '?pages=' + url
                text = '[COLOR lime]' + 'Page ' + text + '[/COLOR]'
                if 'aquo' not in text:
                    addDir(text, url,1,thumb, '','')
   
def all_series(url):
    link = open_url(url)
    match = re.compile('<li> <a class="underilne" href="(.+?)">(.+?)</a> </li>').findall(link)	
    for url, name in match:
        list_data = "%sQQ%sQQ%s" % (name.replace(' & ', '->-').replace(':', ''), url, 'missing')
        addDir(name, url,2,'missing', list_data,'sh')

def links(name,url,iconimage):
    epurl = url.replace('http', 'hhhh')
    link = open_url(url).strip().replace('\n', '').replace('\t', '').replace('?', '<>').replace('#', '$')
    if 'SHOW EPISODES' in link:
        if iconimage == 'missing':
            iconimage = regex_from_to(link, '<div class="cover"><a href="', '"')
        season = regex_get_all(link, '688px;">', '<a data-season')
        for s in season:
            season = regex_from_to(s, '688px;">', '<a data-season').rstrip()
            addDir(season, str(link),4,iconimage, name,epurl)
    else:
        match = re.compile('data-id="(.+?)" data-host="iShared.eu" class="ReportLink" >report this link</a></td><td class="quality_td">(.+?)</td><td class="age_td">(.+?)</td><td class="link_td">   <a target="_blank" href="(.+?)">WATCH').findall(link)
        for id,quality,age,url in match:
            text = "%s [COLOR gold][%s][/COLOR] (uploaded %s ago)" % (name, quality, age)
            url = url
            addDirPlayable(text,url,3,iconimage,name)
			
def tv_show_episodes(name, list, iconimage, showname,epurl):
    seasonnum = name.replace('Season ', '')
    episodes = regex_from_to(list, 'SHOW EPISODES</a', '<div class="advert')
    all_episodes = re.compile('<div class="number left"><a style="(.+?)" href="(.+?)">(.+?)</a></div><div class="name left"> <a href="(.+?)">(.+?)</a></div><div class="edate left">(.+?)</div>').findall(episodes)
    for d1,url,epnum,url2,epname,epdate in all_episodes:
        snum = regex_from_to(url, 'season=', '&episode')
        epnum = epnum.replace('Episode ', '')
        url = epurl.replace('hhhh', 'http') + url.replace("<>", "?").replace("$", "#").replace("aNd", "&").replace('hhhh', 'http').replace('href="', '')
        name = "%sx%s - %s - %s" % (snum, epnum, clean_file_name(epname),epdate)
        if snum == seasonnum:
            addDirPlayable(name,url,3,iconimage, showname)
    setView('episodes', 'episodes-view')

def new_episodes(url):
    addDir('[COLOR cyan] << Return to Main Menu [/COLOR]', '','','', '', '')
    f_url = url.find('?pages=')
    if f_url == -1:
        origurl = url
    else:
        origurl=url[:f_url]
    link = open_url(url)
    movies = regex_get_all(link, '<div class="movie_box', '<a class="more_button')
    for m in movies:
        title = regex_from_to(m, '<h1 style="font-size:12px;height:20px;margin-bottom:0px;">', '</h1>')
        url = regex_from_to(m, '<a href="', '"')
        thumb = regex_from_to(m, 'src="', '"')
        show = re.compile('<h2 class="movie_description"><b>(.+?)</b><br />(.+?)</h2>').findall(m)
        for showname, epname in show:
            showname = showname
            epname = epname
            name = "%s - %s - %s" % (showname, title, epname)
            addDirPlayable(name,url,3,thumb, '')

    pager = regex_from_to(link, '<div class="pagestring">', '</div>')
    pages = re.compile('<a href="(.+?)pages=(.+?)">(.+?)</a>').findall(pager)
    if len(pages)==0:
        url = origurl + '?pages=1'
        text = '[COLOR lime]' + 'Page 2' + '[/COLOR]'
        addDir(text, url,5,thumb, '','')
    else:
        for q, url, text in pages:
            url = origurl + '?pages=' + url
            text = '[COLOR lime]' + 'Page ' + text + '[/COLOR]'
            if 'aquo' not in text:
                addDir(text, url,5,thumb, '','')
		
def search():
    keyboard = xbmc.Keyboard('', 'Search Movie/Show', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            search_show(query)
		
def search_show(query):
    url = 'http://moviestorm.eu/search?q=%s&go=Search' % query
    link = open_url(url).replace('\n', '').replace('\t', '')
    movies = regex_get_all(link, '<div class="movie_box">', '<a class="more')
    for m in movies:
        title = regex_from_to(m, '<h1>', '</h1>')
        url = regex_from_to(m, '<a href="', '"')
        thumb = regex_from_to(m, 'src="', '"')
        list_data = "%sQQ%sQQ%s" % (title.replace(' & ', '->-').replace(':', ''), url, thumb)
        addDir(title, url,2,thumb, list_data,'sh')


def play(name, url, iconimage, showname):
    handle = str(sys.argv[1])
    link = open_url(url).strip().replace('\n', '').replace('\t', '')
    try:
        url = regex_from_to(link, 'var xxxx = "', '"')
    except:
        if name.count('-')==4:
            showname = "%s %s" % (showname, name)
        else:
            showname = name
        url = regex_from_to(link, 'target="_blank" href="', '">')
        link = open_url(url).strip().replace('\n', '').replace('\t', '')
        url = regex_from_to(link, 'var xxxx = "', '"')
    filepos = url.index('ses=')-5   
    filetype = url[filepos:filepos+4]
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    listitem = xbmcgui.ListItem(showname, iconImage=iconimage, thumbnailImage=iconimage)
    playlist.add(url,listitem)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    
    if handle != "-1" and name != "auto":
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        try:
            xbmcPlayer.play(playlist)
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("Playback failed", "Check your account settings")

def favourites():
    if os.path.isfile(FAV):
        s = read_from_file(FAV)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('QQ')
                title = list1[0]
                title = title.replace('->-', ' & ')
                url = list1[1]
                thumb = list1[2]
                addDir(title, url,2,thumb, list,'sh')
				
def subscriptions():
    if os.path.isfile(SUB):
        s = read_from_file(SUB)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('QQ')
                title = list1[0]
                title = title.replace('->-', ' & ')
                url = list1[1]
                thumb = list1[2]
                addDir(title, url,3,thumb, list,'sh')

def add_favourite(name, url, iconimage, dir, text):
    list_data = iconimage.replace('hhhh', 'http:')
    splitdata = list_data.split('QQ')
    name = splitdata[0]
    name = name.replace('->-', ' & ')
    thumb = splitdata[2]
    add_to_list(list_data, dir)
    notification(name, "[COLOR lime]" + text + "[/COLOR]", '5000', thumb)
	
def remove_from_favourites(name, url, iconimage, dir, text):
    list_data = iconimage.replace('hhhh', 'http:')
    splitdata = list_data.split('QQ')
    name = splitdata[0]
    name = name.replace('->-', ' & ')
    thumb = splitdata[2]
    remove_from_list(list_data, dir)
    notification(name, "[COLOR orange]" + text + "[/COLOR]", '5000', thumb)
	
def create_tv_show_strm_files(name, url, iconimage, ntf):
    epurl = url.replace('http', 'hhhh')
    dialog = xbmcgui.Dialog()
    n = name
    u = url
    l = iconimage
    list_data = iconimage.replace('hhhh', 'http:')
    splitdata = iconimage.split('QQ')
    name = splitdata[0]
    name = name.replace('->-', ' & ')
    thumb = splitdata[2]
    tv_show_path = create_directory(TV_PATH, name)
    link = open_url(url).strip().replace('\n', '').replace('\t', '').replace('?', '<>').replace('#', '$')
    if 'SHOW EPISODES' in link:
        episodes = regex_from_to(link, 'SHOW EPISODES</a', '<div class="advert')
        all_episodes = re.compile('<div class="number left">(.+?)</div><div class="name left"> (.+?)</div><div class="edate left">(.+?)</div> <div class="link left"><a class="watch_all" href="(.+?)">Watch NOW').findall(episodes)
        if iconimage == 'missing':
            iconimage = regex_from_to(link, '<div class="cover"><a href="', '"')
        else:
            iconimage = thumb
        season = regex_get_all(link, '688px;">', '<a data-season')
        for s in season:
            season = regex_from_to(s, '688px;">', '<a data-season').rstrip()
            seasonnum = season.replace("Season ", "")
            season_path = create_directory(tv_show_path, str(seasonnum))
            for epnum, epname, epdate, url in all_episodes:
                iconimage = regex_from_to(link, '<div class="cover"><a href="', '"')
                snum = regex_from_to(url, 'season=', '&episode')
                epnum = epnum.replace('Episode ', '')
                url = epurl.replace('hhhh', 'http') + url.replace("<>", "?").replace("$", "#").replace("aNd", "&").replace('href="', '')
                display = "%sx%s - %s" % (snum, epnum, clean_file_name(epname))
                if snum == seasonnum:
                   create_strm_file(display, url, "3", season_path, iconimage.replace('hhhh', 'http:'), name)
        if ntf == "true" and ENABLE_SUBS:
            if dialog.yesno("Subscribe?", 'Do you want MovieStorm to automatically add new', '[COLOR gold]' + name + '[/COLOR]' + ' episodes when available?'):
                add_favourite(n, u, l, SUB, "Added to Library/Subscribed")
            else:
                notification(name, "[COLOR lime]Added to Library[/COLOR]", '5000', thumb)
        if xbmc.getCondVisibility('Library.IsScanningVideo') == False:           
            xbmc.executebuiltin('UpdateLibrary(video)')
    else:			
        create_strm_file(n, u, "3", MOVIE_PATH, thumb.replace('hhhh', 'http:'), n)
        if xbmc.getCondVisibility('Library.IsScanningVideo') == False:           
            xbmc.executebuiltin('UpdateLibrary(video)')

def remove_tv_show_strm_files(name, url, iconimage, dir_path):
    dialog = xbmcgui.Dialog()
    splitname = iconimage.split('QQ')
    rname = splitname[0]
    rname = rname.replace('->-', ' & ')
    try:
        path = os.path.join(dir_path, str(rname))
        shutil.rmtree(path)
        remove_from_favourites(name, url, iconimage, SUB, "Removed from Library/Unsubscribed")
        if xbmc.getCondVisibility('Library.IsScanningVideo') == False:
            if dialog.yesno("Clean Library?", '', 'Do you want clean the library now?'):		
                xbmc.executebuiltin('CleanLibrary(video)')		
    except:
        xbmc.log("[MovieStorm] Was unable to remove TV show: %s" % (name)) 
		
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
        xbmc.log("[MovieStorm] Error while creating strm file for : " + name)
		
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
        xbmc.log("[MovieStorm] Failed to fetch subscription")

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
        contextMenuItems = []
        if name == "My Subscriptions":
            contextMenuItems.append(("[COLOR cyan]Refresh Subscriptions[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=17&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
        if description == "sh":
            if find_list(list, FAV) < 0:
                suffix = ""
                contextMenuItems.append(("[COLOR lime]Add to My Favourites[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=11&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
            else:
                suffix = ' [COLOR lime]+[/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from My Favourites[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=13&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
            if find_list(list, SUB) < 0:
                suffix2 = ""
                contextMenuItems.append(("[COLOR lime]Add to XBMC Library/Subscribe[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=14&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
            else:
                suffix2 = ' [COLOR cyan][s][/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from XBMC Library[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=15&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
        liz=xbmcgui.ListItem(name + suffix + suffix2, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirPlayable(name,url,mode,iconimage,showname):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&showname="+urllib.quote_plus(showname)
        ok=True
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

elif mode == 101:
        movie_menu()
		
elif mode == 102:
        tvseries_menu()
		
elif mode == 106:
        genres(url)
		
elif mode == 107:
        all_series(url)
		
elif mode==1:
        Main(url)        
       
elif mode==2:
        links(name,url,iconimage)
		
elif mode==3:
        play(name, url, iconimage, showname)
		
elif mode==4:
        tv_show_episodes(name, url, iconimage, list,description)
		
elif mode==5:
        new_episodes(url)
		
elif mode==6:
        search()
		
elif mode == 7:
        search_show(name)
		
elif mode == 11:
        add_favourite(name, url, list, FAV, "Added to Favourites")
		
elif mode == 12:
        favourites()
		
elif mode == 13:
        remove_from_favourites(name, url, list, FAV, "Removed from Favourites")
		
elif mode == 14:
        create_tv_show_strm_files(name, url, list, "true")
		
elif mode == 15:
        remove_tv_show_strm_files(name, url, list, TV_PATH)
		
elif mode == 16:
        subscriptions()
		
elif mode == 17:
        get_subscriptions()
		
elif mode == 18:
        request_video()
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))



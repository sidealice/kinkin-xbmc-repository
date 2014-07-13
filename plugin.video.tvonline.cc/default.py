'''
kinkin
'''

import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import settings
import time
from datetime import date, datetime
from threading import Timer
from hashlib import md5
from helpers import clean_file_name
import shutil
from hashlib import md5
import hashlib
from threading import Thread
import requests
import urlresolver
from helpers import clean_file_name
from metahandler import metahandlers
metainfo = metahandlers.MetaData()


ADDON = settings.addon()
TVO_USER = settings.tvo_user()
TVO_PASSWORD = settings.tvo_pass()
TVO_EMAIL = settings.tvo_email()
ENABLE_SUBS = settings.enable_subscriptions()
ENABLE_META = settings.enable_meta()
TV_PATH = settings.tv_directory()
CACHE_PATH = settings.cache_path()
FAV = settings.favourites_file()
SUB = settings.subscription_file()
cookie_jar = settings.cookie_jar()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'Fanart2.jpg'))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'icon.png'))
base_url = 'http://www.tvonline.cc/'


def open_url(url, cache_time=3600):
    trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0')
    h = hashlib.md5(url).hexdigest()
    print url,h
    cache_file = os.path.join(CACHE_PATH, h)
    age = get_file_age(cache_file)
    print "TVonline.........FILE AGE IS " + str(age)
    if age > 0 and age < cache_time:
        r = read_from_file(cache_file, silent=True).translate(trans_table)
        print "TVonline.........use CACHE"
        if r:
            return r
    else:
        response = urllib2.urlopen(req)
        link=response.read().translate(trans_table)
        write_to_file(cache_file, link)
        print "TVonline.........NO CACHE"
        response.close()
        return link
	
def get_file_age(file_path):
    try:    
        stat = os.stat(file_path)
        fileage = datetime.fromtimestamp(stat.st_mtime)
        now = datetime.now()
        delta = now - fileage
        return delta.seconds
    except:
        return -1
	

def CATEGORIES(name):
    addDir("Popular Shows", 'http://tvshows.ec/new',2,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'HitTVShows.png')), 'no','')
    addDir("Top Shows", 'url',27,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'HitTVShows.png')), '','')
    addDir("Genres", 'url',30,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'HitTVShows.png')), '','')
    addDir("A-Z", 'url',8,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'A-Z.png')), '','')
    addDir("Search", 'url',6,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'search2.png')), '','')
    addDir("New Episodes Added", 'http://tvshows.ec/latest',41,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'NewEpisodes.png')), '','')
    addDir("TV Schedule", 'http://tvshows.ec/tvschedule/-1',40,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'schedule.png')), '','')
    addDir("My Favourites", 'url',12,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'Favourites.png')), '','')
    if ENABLE_SUBS:
        addDir("My Subscriptions", 'url',16,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'Subscriptions.png')), '','')
    else:
        addDir("[COLOR orange] My Subscriptions (ENABLE IN SETTINGS)[/COLOR]", 'url',16,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'Subscriptions.png')), '','')
    

def topshows():
    addDir("Top TV Shows", 'Top TVShows',7,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'HitTVShows.png')), '','')
    addDir("Top Animation", 'Top Animation',7,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'HitTVShows.png')), '','')
    addDir("Top Documentary", 'Top Documentary',7,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'HitTVShows.png')), '','')
    addDir("Top Reality", 'Top Reality',7,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'HitTVShows.png')), '','')
    addDir("Top Sport", 'Top Sport',7,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', 'HitTVShows.png')), '','')
def genres():
    url1 = 'http://tvshows.ec/'
    link = open_url(url1).rstrip()
    match = re.compile('href="(.+?)" title="Search for(.+?)">(.+?)</a>').findall(link)
    for url,d1,title in match:
        url = url1 + url
        if title != 'ADULT':
            addDir(title, url,2,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', title.lower() + '.png')), '1','')
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
	
def search():
    keyboard = xbmc.Keyboard('', 'Search TV Show', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            shows(query,'1')
			
def tvschedule(url):
    link = open_url(url).rstrip()
    match=re.compile('<li><a title="Watch Episodes Released(.+?)" href="(.+?)">(.+?)</a></li>').findall(link)
    for t1,url,title in match:
        url = 'http://tvshows.ec' + url
        addDir(title, url,41,"", "",'menu')
		
def schedule_episodes(name,url,iconimage):
    link = open_url(url).rstrip()#
    match = re.compile('<li><a title="Watch (.+?)Online For Free" href="(.+?)">(.+?)</a></li>').findall(link)
    for title,url,title1 in match:
        url = 'http://tvshows.ec' + url
        showname = title[:title.find(' Season')]
        en = regex_from_to(title,'Episode ', ' ')
        sn = regex_from_to(title,'Season ', ' ')
        if len(en) == 1:
            enum = "%s%s" % ('E0', en)
        else:
            enum = "%s%s" % ('E', en)
        if len(sn) == 1:
            snum = "%s%s" % ('S0', sn)
        else:
            snum = "%s%s" % ('S', sn)
        seasonepi = "%s%s" % (snum, enum)
        title = title.rstrip()
        if ENABLE_META:
            try:
                infoLabels=get_meta(showname,'episode',year=None,season=sn,episode=en)
                if infoLabels['title']=='':
                    name = title
                else:
                    name = "%s %s %s" % (showname, seasonepi, infoLabels['title'])
                if infoLabels['cover_url']=='':
                    iconimage=""
                else:
                    iconimage=infoLabels['cover_url']
            except:
                pass
        else:
            infoLabels =None
            iconimage=""
            name = title
        try:
            addDirPlayable(name.replace(u'\u2019',"'"),url,5,iconimage, showname,infoLabels=infoLabels)
        except:
            addDirPlayable(title,url,5,iconimage, showname,infoLabels=infoLabels)
    setView('episodes', 'episodes-view')

def a_to_z(url):
    alphabet =  ['09', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
    for a in alphabet:
        addDir(a, 'http://tvshows.ec/letters/%s' % (a.lower().replace('#', 'num')),25,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvonline.cc', 'art', a.replace('09','HASH') + '.png')), '0<>50','menu')
		
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
                if ENABLE_META:
                    infoLabels = get_meta(title,'tvshow',year=None,season=None,episode=None,imdb=None)
                    if infoLabels['title']=='':
                        name=title
                    else:
                        name=infoLabels['title']
                    if infoLabels['cover_url']=='':
                        iconimage=thumb
                    else:
                        iconimage=infoLabels['cover_url']
                else:
                    infoLabels =None
                    iconimage=thumb
                addDir(title, url,3,thumb, list,'sh',infoLabels=infoLabels)
				
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
                if ENABLE_META:
                    infoLabels = get_meta(title,'tvshow',year=None,season=None,episode=None,imdb=None)
                    if infoLabels['title']=='':
                        name=title
                    else:
                        name=infoLabels['title']
                    if infoLabels['cover_url']=='':
                        iconimage=thumb
                    else:
                        iconimage=infoLabels['cover_url']
                else:
                    infoLabels =None
                    iconimage=thumb
                addDir(title, url,3,thumb, list,'sh',infoLabels=infoLabels)

		
def shows(url,page):
    baseurl = url
    if page != 'no':
        np = int(page) + 1
        if 'http' not in url:
            url = 'http://tvshows.ec/TVshows/%s-page-%s' % (url,page)
        else:
            url = url + '/' + str(page)
        
    dp = xbmcgui.DialogProgress()
    dp.create("TVonline",'Searching')
    dp.update(0)
    link = open_url(url).rstrip()
    match = re.compile('</div><div class="results"><a href="(.+/?)" title="(.+/?)"><img class="results-poster" alt="(.+/?)" src="(.+/?)" /></a><div class="results-heading">(.+/?)href="(.+/?)" title="(.+/?)<div id="desc">(.+/?)</div><div').findall(link)
    nItem = len(match)
    count = 0
    for url,t,title,thumb,d1,url1,d2,plot in match:
        count = count + 1
        url = 'http://tvshows.ec' + url
        titlelist = str(count) + ' of ' + str(nItem) + ': ' + title
        progress = count / float(nItem) * 100               
        dp.update(int(progress), 'Adding title',titlelist)
        if dp.iscanceled():
            return
        if ENABLE_META:
            infoLabels = get_meta(title,'tvshow',year=None,season=None,episode=None,imdb=None)
            if infoLabels['title']=='':
                name=title
            else:
                name=infoLabels['title']
            if infoLabels['cover_url']=='':
                iconimage=thumb
            else:
                iconimage=infoLabels['cover_url']
        else:
            infoLabels =None
            iconimage=thumb
        list_data = "%sQQ%sQQ%s" % (title.replace(' & ', '->-').replace(':', ''), url, iconimage)
        addDir(str(title), str(url),3,iconimage, list_data,'sh',infoLabels=infoLabels)
    if page != 'no':
        addDir('Next page >>', baseurl,2,'', str(np),'')
    setView('episodes', 'episodes-view')
	
def shows_az(url,page):
    nexturl=url
    minpage = page.split('<>')[0]
    maxpage = page.split('<>')[1]
    nextmin = int(maxpage) + 1
    nextmax = int(maxpage) + 50
    nextlist = "%s<>%s" % (nextmin,nextmax)
    dp = xbmcgui.DialogProgress()
    dp.create("TVonline",'Searching')
    dp.update(0)
    link = open_url(url).rstrip()
    match = re.compile('<li><a href="(.+?)" title="(.+?)" style="(.+?)">(.+?)</a></li>').findall(link)
    nAllItem = len(match)
    nItem = 50
    count = 0
    for url,t,d1,title in match:
        count = count + 1
        if count >= int(minpage) and count <= int(maxpage):
            title = title.rstrip()
            url = 'http://tvshows.ec' + url
            titlelist = str(count - int(minpage)) + ' of ' + str(nItem) + ' (' + str(nAllItem) + ' total): ' + title
            progress = count / float(nItem) * 100               
            dp.update(int(progress), 'Adding title',titlelist)
            if dp.iscanceled():
                return
            if ENABLE_META:
                infoLabels = get_meta(title,'tvshow',year=None,season=None,episode=None,imdb=None)
                if infoLabels['title']=='':
                    name=title
                else:
                    name=infoLabels['title']
                if infoLabels['cover_url']=='':
                    iconimage=iconart
                else:
                    iconimage=infoLabels['cover_url']
            else:
                infoLabels =None
                iconimage=iconart
            list_data = "%sQQ%sQQ%s" % (title.replace(' & ', '->-').replace(':', ''), url, iconimage)
            addDir(str(title), str(url),3,iconimage, list_data,'sh',infoLabels=infoLabels)
    if nextmin < nAllItem:
        addDir('Next page (' + nextlist.replace('<>','-') + ')', nexturl,25,'', nextlist,'menu')
    setView('episodes', 'episodes-view')
	
def grouped_shows(header):
    years = ['1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001','2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010','2011', '2012', '2013', '2014', '2015', '2016', '2017','2018', '2019', '2020', '2021', '2022', '...', '201']
    url = 'http://tvshows.ec/'
    link = open_url(url).replace('  ', ' ').rstrip()
    all_shows = regex_from_to(link,str(header), '</div></div>')
    match= re.compile('<li><span>(.+?)</span><a href="(.+?)" title="(.+?)">(.+?)</a></li>').findall(all_shows)
	                  
    for num,url,t1,title in match:
        for y in years:
            if y in title:
                title = title.replace(str(y),'').rstrip()
        url = 'http://tvshows.ec' + url
        if ENABLE_META:
            infoLabels = get_meta(title,'tvshow',year=None,season=None,episode=None,imdb=None)
            if infoLabels['title']=='':
                name=title
            else:
                name=infoLabels['title']
            if infoLabels['cover_url']=='':
                iconimage=iconart
            else:
                iconimage=infoLabels['cover_url']
        else:
            infoLabels =None
            iconimage=iconart
        list_data = "%sQQ%sQQ%s" % (title.replace(' & ', '->-').replace(':', ''), url, iconimage)
        addDir(str(title), url,3,iconimage, list_data,'sh',infoLabels=infoLabels)
        
    setView('episodes', 'episodes-view')
	
def tv_show(name, url, iconimage):
    showname = name.replace('&','and')
    season = []
    episodes = []
    link = open_url(url).rstrip()
    data = regex_from_to(link, '<div id="recent">', 'div class="')
    match = re.compile('<li>(.+?)href="(.+?)" title="(.+?)" > (.+?) </a>').findall(data)
    for d1,url,t1,title in match:
        sname = 'Season ' + regex_from_to(title, 'Season ', ' Episode')
        if sname not in season:
            season.append(sname)
            sn = sname.replace('Season ','')
            if ENABLE_META:
                infoLabels=get_meta(name,'tvshow',year=None,season=sn,episode=None)
                if infoLabels['title']=='':
                    name=name
                else:
                    name=infoLabels['title']
                if infoLabels['cover_url']=='':
                    iconimage=iconimage
                else:
                    iconimage=infoLabels['cover_url']
            else:
                infoLabels =None
                iconimage=iconimage
            addDir(sname, 'url',4,iconimage, data,str(showname),infoLabels=infoLabels)
    setView('episodes', 'episodes-view')
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
	
def tv_show_episodes(name, list, iconimage, showname):
    dp = xbmcgui.DialogProgress()
    dp.create("TVonline",'Grabbing episodes...')
    dp.update(0)
    list = list.encode('ascii', 'ignore')
    showname = showname.replace('and','&')
    episodes = re.compile('<li>(.+?)href="(.+?)" title="(.+?)" > (.+?)</a>').findall(list)
    nItem = len(episodes)
    count = 0
    sn = name.replace('Season ', '')
    for d1,url,t1,title in episodes:
        count = count + 1
        url = 'http://tvshows.ec' + url
        sen = regex_from_to(title, 'Season ', ' Episode')
        en = regex_from_to(title, 'Episode ', ' ')
        if len(en) == 1:
            enum = "%s%s" % ('E0', en)
        else:
            enum = "%s%s" % ('E', en)
        if len(sen) == 1:
            snum = "%s%s" % ('S0', sen)
        else:
            snum = "%s%s" % ('S', sen)
        seasonepi = "%s%s" % (snum, enum)
        title = title.rstrip()
        titlelist = str(count) + ': ' + title
        progress = count / float(nItem) * 100               
        dp.update(int(progress), 'Adding title',titlelist)
        if dp.iscanceled():
            return
        if sen == sn:
            if ENABLE_META:
                infoLabels=get_meta(showname,'episode',year=None,season=sen,episode=en)
                if infoLabels['title']=='':
                    name = title
                else:
                    name = "%s %s" % (seasonepi, infoLabels['title'])
                if infoLabels['cover_url']=='':
                    iconimage=iconimage
                else:
                    iconimage=infoLabels['cover_url']
            else:
                infoLabels =None
                iconimage=iconimage
                name = title
            if 'gray' not in d1:
                try:
                    addDirPlayable(name.replace(u'\u2019',"'"),url,5,iconimage, showname,infoLabels=infoLabels)
                except:
                    addDirPlayable(title,url,5,iconimage, showname,infoLabels=infoLabels)
    setView('episodes', 'episodes-view')
    if ENABLE_META:
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_EPISODE)
    else:
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
		
def play(name, url, iconimage, showname):
    origurl=url
    urllist = []
    dp = xbmcgui.DialogProgress()
    dp.create("TVonline",'Resolving links')
    dp.update(0)
    handle = str(sys.argv[1])
    try:
        link = requests.get(url,allow_redirects=False)
        url1 = link.headers['location']
        link = open_url(url1)
        all_links = regex_get_all(link, '<div id="video-content">', '</iframe>')
        nItem = len(all_links)
    except:
        link = open_url(url)
        all_links = regex_get_all(link, 'hostButton', 'embed')
        nItem = len(all_links)
        if nItem == 0:
            all_links = regex_get_all(link, '<td class="video-title">', '</td>')
            nItem = len(all_links)
    count = 0
    for a in all_links:
        count = count + 1
        try:
            host = regex_from_to(a, 'value="', '"')
            id = regex_from_to(a, 'id="link', '"')
            url = 'http://tvshows.ec/Link/%s' % id
        except:
            try:
                data = regex_from_to(a, '<a target="', 'a>')
                host = regex_from_to(data, '">', '<')
                id = regex_from_to(data, '/Link/', '"')
                url = 'http://tvshows.ec/Link/%s' % id
            except:
                url=regex_from_to(a, 'src="', '"')
                host = regex_from_to(url, 'http://', '/')
                id = 'primary'
        urllist.append(url)
        titlelist = str(count) + ' of ' + str(nItem) + ': ' + host
        progress = len(urllist) / float(nItem) * 100               
        dp.update(int(progress), 'Adding link',host)
        if dp.iscanceled():
            return
        try:
            dp = xbmcgui.DialogProgress()
            dp.create("TVonline: Trying Link",titlelist)
            if id == 'primary':
                url1 = url
            else:
                response = requests.get(url,allow_redirects=False)
                url1 = response.headers['location']
            playlink = resolve_url(url1)
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playlist.clear()
            listitem = xbmcgui.ListItem(showname + ' ' + name, iconImage=iconimage, thumbnailImage=iconimage)
            playlist.add(playlink,listitem)
            xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	
            if handle != "-1":
                listitem.setProperty("IsPlayable", "true")
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
            else:
                xbmcPlayer.play(playlist)
            return
        except:
            pass
    if 'Sorry we do not have any links' in link:
        notification(name, "[COLOR red]No links available[/COLOR]", '4000', iconimage)

def resolve_url(url):
    validresolver = urlresolver.HostedMediaFile(url)
    if validresolver:
        try:
            playlink = urlresolver.resolve(url)
        except:
            pass
    return playlink    

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
    link = open_url(url).rstrip()
    data = regex_from_to(link, '<div id="recent">', 'div class="')
    episodes = re.compile('<li>(.+?)href="(.+?)" title="(.+?)" > (.+?)</a>').findall(data)
    for d1,url,t1,title in episodes:
        url = 'http://tvshows.ec' + url
        sen = regex_from_to(title, 'Season ', ' Episode')
        en = regex_from_to(title, 'Episode ', ' ')
        if len(en) == 1:
            enum = "%s%s" % ('E0', en)
        else:
            enum = "%s%s" % ('E', en)
        if len(sen) == 1:
            snum = "%s%s" % ('S0', sen)
        else:
            snum = "%s%s" % ('S', sen)
        seasonepi = "%s%s" % (snum, enum)
        season_path = create_directory(tv_show_path, str(sen))
        display = "%s %s" % (seasonepi, title)
        if 'gray' not in d1:
            create_strm_file(display, url, "5", season_path, thumb, name)

    if ntf == "true" and ENABLE_SUBS:
        if dialog.yesno("Subscribe?", 'Do you want TVonline to automatically add new', '[COLOR gold]' + name + '[/COLOR]' + ' episodes when available?'):
            add_favourite(n, u, l, SUB, "Added to Library/Subscribed")
        else:
            notification(name, "[COLOR lime]Added to Library[/COLOR]", '4000', thumb)
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
        xbmc.log("[TVonline] Was unable to remove TV show: %s" % (name)) 
   
		
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
    #xbmc.executebuiltin("Container.Refresh")
    
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
		
def get_meta(name,types=None,year=None,season=None,episode=None,imdb=None,episode_title=None):
    if 'tvshow' in types:
        meta = metainfo.get_meta('tvshow',name,'','','')
    if 'episode' in types:
        meta = metainfo.get_episode_meta(name, '', season, episode)
    infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Episode': meta['episode'],'Aired': meta['premiered'],'Playcount': meta['playcount'],'Overlay': meta['overlay']}
        
    return infoLabels
	
def clear_cache():
    cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.tvonline.cc/cache'), '')
		
    for root, dirs, files in os.walk(cache_path):
        for f in files:
            age = get_file_age(os.path.join(root, f))
            if age > 3600:
    	        os.unlink(os.path.join(root, f))
	
		
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


def addDir(name,url,mode,iconimage,list,description,infoLabels=None):
        suffix = ""
        suffix2 = ""
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+str(iconimage)+"&list="+str(list)+"&description="+str(description)
        ok=True
        contextMenuItems = []
        if name == "My Subscriptions":
            contextMenuItems.append(("[COLOR cyan]Refresh Subscriptions[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=18&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
        if description == "sh":
            if find_list(list, FAV) < 0:
                suffix = ""
                contextMenuItems.append(("[COLOR lime]Add to TVonline Favourites[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=11&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
            else:
                suffix = ' [COLOR lime]+[/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from TVonline Favourites[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=13&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
            if find_list(list, SUB) < 0:
                suffix2 = ""
                contextMenuItems.append(("[COLOR lime]Add to XBMC Library/Subscribe[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=14&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
            else:
                suffix2 = ' [COLOR cyan][s][/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from XBMC Library[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=15&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
        liz=xbmcgui.ListItem(name + suffix + suffix2, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels=infoLabels)
        try:
            liz.setProperty( "fanart_image", infoLabels['fanart'] )
        except:
            liz.setProperty('fanart_image', fanart )
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirPlayable(name,url,mode,iconimage,showname,infoLabels=None):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&showname="+urllib.quote_plus(showname)
        ok=True
        contextMenuItems = []
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels=infoLabels)
        try:
            liz.setProperty( "fanart_image", infoLabels['fanart'] )
        except:
            liz.setProperty('fanart_image', fanart )
        contextMenuItems.append(("[COLOR red]Report an error[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=10&showname=%s)'%(sys.argv[0],name, url, showname)))
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
        shows(url,list)
		
elif mode == 25:
        shows_az(url,list)
		
elif mode==3:
        tv_show(name, url, iconimage)
		
elif mode==4:
        tv_show_episodes(name, list, iconimage, description)
		
elif mode==5:
        play(name, url, iconimage.replace('hhhh', 'http:'), showname)
		
elif mode==6:
        search()
		
elif mode==7:
        grouped_shows(url)
		
	
elif mode == 8:
        a_to_z(url)
		
elif mode == 9:
        watched_list(url)
		
elif mode == 10:
        report_error(name, url, showname)
		
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
		
elif mode == 18:
        get_subscriptions()
		
elif mode == 26:
        clear_cache()
		
elif mode == 27:
        topshows()
		
elif mode == 30:
        genres()
		
elif mode == 40:
        tvschedule(url)
		
elif mode == 41:
        schedule_episodes(name,url,iconimage)
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))



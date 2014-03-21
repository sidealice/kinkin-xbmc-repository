'''
kinkin
'''
#coding=UTF8
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
import requests
from threading import Thread
import cookielib
from t0mm0.common.net import Net
from helpers import clean_file_name
import random
from metahandler import metahandlers
metainfo = metahandlers.MetaData()
net = Net()


ADDON = settings.addon()
ENABLE_META = settings.enable_meta()
MOVIE_PATH = settings.movie_directory()
FAV = settings.favourites_file()
FAV_MUSIC = settings.favourites_music_file()
FAV_ARTISTS = settings.favourites_artists_file()
SUB = settings.subscription_file()
SORT = settings.default_sort()
LANGUAGE = settings.default_language()
SUBTITLE = settings.default_subtitle()
MAX_MV = settings.play_max()
PC_ENABLE = settings.enable_pc()
PC_WATERSHED = settings.watershed_pc()
PC_RATING = settings.pw_required_at()
PC_PASS = settings.pc_pass()
PC_DEFAULT = settings.pc_default()
PC_TOGGLE = settings.enable_pc_settings()
CUSTOM_PC = settings.custom_pc_file()
cookie_jar = settings.cookie_jar()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.youtubeonfire', 'fanart.jpg'))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.youtubeonfire', 'icon.png'))
movie_url = 'http://www.movietube.co/'
posturl = 'http://movietube.co/index.php'
ytplayerfixed = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.youtubeonfire', 'helpers', 'YouTubePlayer.py'))
ytplayercopyto = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.youtube', ''))
ytplayerorig = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.youtube', 'YouTubePlayer.py'))
ytplayerbak = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.youtubeonfire', 'helpers', 'youtubeplayer_bak'))
art = 'http://kinkin-xbmc-repository.googlecode.com/svn/trunk/zips/plugin.video.youtubeonfire/art/'



def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
def POST_URL(url,a,c,p):#, form_data
    form_dict = {}
    form_dict['a'] = a
    form_dict['c'] = c
    form_dict['p'] = p
    header_dict = {}
    header_dict['Accept'] = 'text/html, */*; q=0.01'
    header_dict['Accept-Language'] = 'en-US,en;q=0.5'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Cache-Control'] = 'no-cache'
    header_dict['Pragma'] = 'no-cache'
    if 'mvtube' in url:
        header_dict['Host'] = 'mvtube.co'
    elif 'knowledge' in url:
        header_dict['Host'] = 'knowledgetube.co'
    else:
        header_dict['Host'] = 'www.movietube.co'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    if 'mvtube' in url:
        if a == 'retrieveplaylists':
            header_dict['Referer'] = 'http://mvtube.co/details.php'
        else:
            header_dict['Referer'] = 'http://mvtube.co/search.php'
    elif 'knowledge' in url:
        header_dict['Referer'] = 'http://knowledgetube.co/search.php'
    else:
        header_dict['Referer'] = 'http://www.movietube.co/search.php'
    #header_dict['Content-Length'] = '113'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0'
    header_dict['X-Requested-With'] = 'XMLHttpRequest'
    net.set_cookies(cookie_jar)
    trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
    req = net.http_POST(url, form_data=form_dict, headers=header_dict).content.translate(trans_table).rstrip()
    net.save_cookies(cookie_jar)
    return req
	
def GET_URL(url):
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    header_dict['Host'] = 'www.movietube.co'
    header_dict['Referer'] = 'http://www.youtubeonfire.com/'
    header_dict['User-Agent'] = '	Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0'
    net.set_cookies(cookie_jar)
    req = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    return req
	
def pc_setting():
    pw = ""
    dialog = xbmcgui.Dialog()
    keyboard = xbmc.Keyboard(pw, 'Enter your PIN/Password', True)
    keyboard.doModal()
    if keyboard.isConfirmed():
        pw = keyboard.getText()
        if pw == PC_PASS:
            if PC_TOGGLE == "UNLOCKED":
                ADDON.setSetting('enable_pc_settings', value='LOCKED')
                xbmc.executebuiltin("Container.Refresh")
            else:
                ADDON.setSetting('enable_pc_settings', value='UNLOCKED')
                xbmc.executebuiltin("Container.Refresh")
                ADDON.openSettings()				
        else:
            dialog.ok("Incorrect PIN/Password","")

def parental_control(name,mpaa):
    if mpaa != "G" and mpaa != "PG" and mpaa != "PG-13" and mpaa != "R":
        mpaa = "Unrated"
    dialog = xbmcgui.Dialog()
    rating_list = ["No thanks, I'll choose later", "G", "PG","PG-13", "R"]
    rating_list_return = ["No thanks, I'll choose later", "G", "PG","PG-13", "R"]
    if mpaa=="Unrated" or mpaa=="":
        mpaa = PC_DEFAULT
        if os.path.isfile(CUSTOM_PC):
            s = read_from_file(CUSTOM_PC)
            if name in s:
                search_list = s.split('\n')
                for list in search_list:
                    if list != '':
                        list1 = list.split('<>')
                        title = list1[0]
                        cmpaa = list1[1]
                        if title==name:
                            mpaa=cmpaa
            else:		
                rating_id = dialog.select("No rating found....set/save your own?", rating_list)
                if(rating_id < 0):
                    return (None, None)
                    dialog.close()
                if(rating_id == 0):
                    mpaa = PC_DEFAULT
                else:
                    pw=''
                    keyboard = xbmc.Keyboard(pw, 'Enter your PIN/Password to save the rating', True)
                    keyboard.doModal()
                    if keyboard.isConfirmed():
                        pw = keyboard.getText()
                    else:
                        pw=''
                    if pw == PC_PASS:
                        mpaa = rating_list_return[rating_id]
                        content = '%s<>%s' % (name, mpaa)
                        add_to_list(content,CUSTOM_PC)
                    else:
                        mpaa = PC_DEFAULT


    if mpaa == "PLAY":
        mpaa_n = 0
    elif mpaa == "G":
        mpaa_n = 1
    elif mpaa == "PG":
        mpaa_n = 2
    elif mpaa == "PG-13":
        mpaa_n = 3
    elif mpaa == "R" or mpaa == "REQUIRE PIN":
        mpaa_n = 4
    return mpaa_n			

	
def CATEGORIES(name):
    addDir("Movies", 'url',100,art + 'movies.png', '1<>""','qq')
    addDir("Music Videos", 'url',200,art + 'musicvideos.png', '1<>""','qq')
    addDir("Knowledge", 'url',300,art + 'knowledge.png', '1<>""','qq')
    addDirPlayable('Apply YouTube fix','url',999,art + 'youtubefix.png', '','')
    if PC_TOGGLE == 'LOCKED':
        addDirPlayable('[COLOR lime]UNLOCK Parental Control Settings[/COLOR]','url',800,art + 'pcunlocked.png', '','')
    else:
        addDirPlayable('[COLOR red]LOCK Parental Control Settings[/COLOR]','url',800,art + 'pcunlocked.png', '','')


def movie_directory(name):
    addDir("Featured", 'http://www.movietube.co/index.php',7,art + 'movies/' + 'featured.png', '1<><><>Score','qq')
    addDir("Newly Added", 'http://www.movietube.co/index.php',7,art + 'movies/' + 'newlyadded.png', '1<><><>addTime','qq')
    addDir("Newly Released", 'http://www.movietube.co/index.php',7,art + 'movies/' + 'newlyreleased.png', '1<><><>ReleaseDate','qq')
    addDir("Top Rated", 'http://www.movietube.co/index.php',7,art + 'movies/' + 'toprated.png', '1<><><>TomatoFresh','qq')
    addDir("Movies by Genre", 'url',101,art + 'movies/' + 'moviesbygenre.png', '1<>','qq')
    addDir("Movies by Quality/Rating", 'url',102,art + 'movies/' + 'moviesbyrating.png', '1<>','qq')
    addDir("Movies by Year", 'http://www.youtubeonfire.com/search.php',103,art + 'movies/' + 'moviesbyyear.png', '1<>','qq')
    addDir("Search", 'url',104,art + 'movies/' + 'search.png', '','')
    addDir("Favourites", 'url',105,art + 'movies/' + 'favourites.png', '','')
	
def movie_directory_1(name):
    addDir("All Movies", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'allmovies.png', '1<><><>','qq')
    addDir("Action", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'action.png', '1<>Action<><>','qq')
    addDir("Adventure", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'adventure.png', '1<>Adventure<><>','qq')
    addDir("Animation", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'animation.png', '1<>Animation<><>','qq')
    addDir("Biography", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'biography.png', '1<>Biography<><>','qq')
    addDir("Comedy", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'comedy.png', '1<>Comedy<><>','qq')
    addDir("Crime", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'crime.png', '1<>Crime<><>','qq')
    addDir("Documentary", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'documentary.png', '1<>Documentary<><>','qq')
    addDir("Drama", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'drama.png', '1<>Drama<><>','qq')
    addDir("Family", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'family.png', '1<>Family<><>','qq')
    addDir("Fantasy", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'fantasy.png', '1<>Fantasy<><>','qq')
    addDir("History", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'history.png', '1<>History<><>','qq')
    addDir("Horror", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'horror.png', '1<>Horror<><>','qq')
    addDir("Mystery", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'mystery.png', '1<>Mystery<><>','qq')
    addDir("Romance", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'romance.png', '1<>Romance<><>','qq')
    addDir("Sci-Fi", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'sci-fi.png', '1<>Sci-Fi<><>','qq')
    addDir("War", 'http://www.movietube.co/index.php',7,art + 'moviesbygenre/' + 'war.png', '1<>War<><>','qq')
    
	
def movie_directory_2(name):
    addDir("1080P", 'http://www.movietube.co/index.php',7,art + 'moviesbyrating/' + '1080p.png', '1<>1080<><>','qq')
    addDir("720P", 'http://www.movietube.co/index.php',7,art + 'moviesbyrating/' + '720p.png', '1<>720<><>','qq')
    addDir("G/PG-13", 'http://www.movietube.co/index.php',7,art + 'moviesbyrating/' + 'gpg13.png', '1<>PG<><>','qq')
    addDir("R-Rated", 'http://www.movietube.co/index.php',7,art + 'moviesbyrating/' + 'r-rated.png', '1<>R-Rated<><>','qq')
	
def movie_directory_3(name,url):
    req = GET_URL(url)
    years = regex_from_to(req, '<input type="hidden"  id="Year"', '</ul>')
    match = re.compile('data="(.+?)">(.+?)</a>').findall(years)
    for year, name in match:
        addDir(name, 'http://www.movietube.co/index.php',7,art + 'moviesbyyear/' + year + '.png', '1<><>'+year+'<>','qq')
		
def favourites_movies():
    if os.path.isfile(FAV):
        s = read_from_file(FAV)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                title = title.replace('->-', ' & ').replace('qq', ',')
                url = list1[1]
                thumb = list1[2]
                metatitle = title.split(' [COLOR ')[0].replace(' (', '<>')
                metatitle = metatitle.replace(')','').split('<>')
                try:
                    metayear = metatitle[1]
                except:
                    metayear = ""
                if ENABLE_META:
                    infoLabels = get_meta(metatitle[0],'movie',year=metayear)
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
                addDir(title, url,3,iconimage, list,'movfav',infoLabels=infoLabels)
        setView('movies', 'movies-view')
		
def search_movie():
    keyboard = xbmc.Keyboard('', 'Search Movies', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            search_moviefile(query)
			
def search_moviefile(query):
    url = 'http://www.youtubeonfire.com/index.php'
    form_dict = {}
    form_dict['a'] = 'retrieve'
    form_dict['c'] = 'result'
    form_dict['p'] = '{"KeyWord":"%s","Page":"1","NextToken":""}' % query
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Accept-Language'] = 'en-US,en;q=0.5'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'www.youtubeonfire.com'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Referer'] = 'http://www.youtubeonfire.com/'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0'
    net.set_cookies(cookie_jar)
    req = net.http_POST(url, form_data=form_dict, headers=header_dict).content.rstrip()
    net.save_cookies(cookie_jar)
    all = regex_get_all(req, '<div class="idx">', '<div class="ytlk">')
    for a in all:
        all_td = regex_get_all(a,  '<td', '</td>')
        vurl = regex_from_to(all_td[0], 'v=', '"')
        url = '{"KeyWord":"' + vurl + '"}'
        hosturl = 'http://www.movietube.co/watch.php?v=' + vurl
        thumb = regex_from_to(all_td[0], 'img src="', '"')
        title = regex_from_to(all_td[1], 'target="_blank">', '</a>').replace('&nbsp', '').replace('<img', '')
        mpaa = regex_from_to(all_td[1], 'light class="text">', ' ').replace('&nbsp', '').replace('<img', '')
        tomato = regex_from_to(all_td[1], '/>', '</h3_light')
        quality = regex_from_to(all_td[2], 'height="20" />', '</h3>')
        metatitle = title.split(' [COLOR ')[0].replace(' (', '<>')
        metatitle = metatitle.replace(')','').split('<>')
        try:
            metayear = metatitle[1]
        except:
            metayear = ""
        if ENABLE_META:
            infoLabels = get_meta(metatitle[0],'movie',year=metayear)
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
        addDir(str(title) + ' [COLOR lime][max ' + quality + '][/COLOR]' + ' ' + mpaa, url,3,iconimage, hosturl,'mov',infoLabels=infoLabels)
    setView('movies', 'movies-view')

def movies(name,url,page,token):
    origurl=url
    print origurl,page
    token = token.replace(' ', '+')
    splitpage=page.split('<>')
    page = splitpage[0]
    genre = splitpage[1]
    year = splitpage[2]
    if splitpage[3] =='':
        sort = SORT
    else:
        sort = splitpage[3]
    
    if token == 'qq':
        token = ''
        p = '{"Page":"%s","NextToken":"%s","VideoYoutubeType":"%s","Genere":"%s","Year":"%s","SubTitle":"%s","Sortby":"%s"}' % (page,token,LANGUAGE,genre,year,SUBTITLE,sort)
    else:
        line = token.split('\n')
        p = '{"Page":"%s","NextToken":"%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s","VideoYoutubeType":"%s","Genere":"%s","Year":"%s","SubTitle":"%s","Sortby":"%s"}' % (page,line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],LANGUAGE,genre,year,SUBTITLE,sort)
    a = 'retrieve'
    c = 'song'

    req = POST_URL(url,a,c,p).decode("string-escape").replace('&nbsp', '')
    token = str(req).split('|')[0]
    all = regex_get_all(req, '<div class="idx">', '<div class="ytlk">')
    for a in all:
        all_td = regex_get_all(a,  '<td', '</td>')
        vurl = regex_from_to(all_td[0], 'v=', '"')
        url = '{"KeyWord":"' + vurl + '"}'
        hosturl = 'http://www.movietube.co/watch.php?v=' + vurl
        thumb = regex_from_to(all_td[0], 'img src="', '"')
        title = regex_from_to(all_td[1], 'target="_blank">', '</a>').replace('&nbsp', '').replace('<img', '')
        mpaa = regex_from_to(all_td[1], 'light class="text">', ' ').replace('&nbsp', '').replace('<img', '')
        tomato = regex_from_to(all_td[1], '/>', '</h3_light')
        quality = regex_from_to(all_td[2], 'height="20" />', '</h3>')
        metatitle = title.split(' [COLOR ')[0].replace(' (', '<>')
        metatitle = metatitle.replace(')','').split('<>')
        try:
            metayear = metatitle[1]
        except:
            metayear = ""
        if ENABLE_META:
            infoLabels = get_meta(metatitle[0],'movie',year=metayear)
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
        addDir(str(title) + ' [COLOR lime][max ' + quality + '][/COLOR]' + ' ' + mpaa, url,3,iconimage, hosturl,'mov',infoLabels=infoLabels)

    nextpage=int(page)+1
    nextpage = "%s<>%s<>%s<>%s" % (nextpage,genre,year,sort)
    addDir("Next Page", 'http://www.movietube.co/index.php',7,art +  'nextpage.png', nextpage,token)
    setView('movies', 'movies-view')
        

def movie_quality(name,url,iconimage,list):
    try:
        mpaa = name.split('[/color] ')[1]
    except:
        try:
            mpaa = name.split('[/COLOR] ')[1]
        except:
            mpaa = "Unrated"
  
    if '[color' in name:
        splitname = name.split('[color lime][max ')
        name = splitname[0].rstrip()
        q = splitname[1].replace('][/color]', '')
    else:
        splitname = name.split('[COLOR lime][max ')
        name = splitname[0].rstrip()
        q = splitname[1].replace('][/COLOR]', '').replace('&nbsp', '').replace('<img', '')
    
    a = 'getplayerinfo'
    c = 'result'
    p = url 
    req = POST_URL(posturl,a,c,p)

    #PARENTAL CONTROL
    now = time.strftime("%H")
    dialog = xbmcgui.Dialog()
    if PC_ENABLE:
        mpaa = parental_control(name,mpaa)
    else:
        mpaa = 0
    pw=''
    if mpaa >= PC_RATING and PC_ENABLE and ((int(now) < int(PC_WATERSHED) and int(now) > 6) or int(PC_WATERSHED) == 25):
        keyboard = xbmc.Keyboard(pw, 'Enter your PIN/Password to play', True)
        keyboard.doModal()
        if keyboard.isConfirmed():
            pw = keyboard.getText()
        else:
            pw=''
    if int(now) >= int(PC_WATERSHED) or not(PC_ENABLE) or ((pw == PC_PASS) or mpaa < PC_RATING or (int(now) < 6 and int(PC_WATERSHED) != 25)):
        if 'src="//www.youtube.com/embed' in req:
            vlink = regex_get_all(req, 'src="//www.youtube.com/embed/', '"')
            for link in vlink:
                link = link.replace('src="//www.youtube.com/embed/', '').replace('"', '')
                url = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + link
                infoLabels =None
                list = "%s<>%s<>%s" % (list,url,name)
                addDirPlayable('[COLOR lime]'+ q + '[/COLOR] | ' + name,url,5,iconimage, list,infoLabels=infoLabels)
        elif 'streamin.to' in req:
            url = regex_from_to(req, 'src="', '"')
            try:
                size = get_file_size(url)
                size = "%.2fGB" % size
            except:
                size = ""
            infoLabels =None
            list = "%s<>%s<>%s" % (list,url,name)
            addDirPlayable('[COLOR lime]'+ q + '[/COLOR] ' + size + ' | ' + name,url,5,iconimage, list,infoLabels=infoLabels)
        elif 'docs.google.com' in req:
            url = regex_from_to(req, 'src="', '"')
            try:
                size = get_file_size(url)
                size = "%.2fGB" % size
            except:
                size = ""
            infoLabels =None
            list = "%s<>%s<>%s" % (list,url,name)
            addDirPlayable('[COLOR lime]'+ q + '[/COLOR] ' + size + ' | ' + name,url,5,iconimage, list,infoLabels=infoLabels)
        else:
            match = re.compile('<source data-res="(.+?)" src="(.+?)"').findall(req)
            for quality, url in match:
                quality = quality + 'p'
                try:
                    size = get_file_size(url)
                    size = "%.2fGB" % size
                except:
                    size = ""
                infoLabels =None
                list = "%s<>%s<>%s" % (list,url,name)
                addDirPlayable('[COLOR lime]'+ quality + '[/COLOR] ' + size + ' | ' + name,url,5,iconimage, list,infoLabels=infoLabels)
    else:
        dialog.ok("You cannot play this video","PIN incorrect")
        		
def play_movie(name,url,iconimage,hosturl):
    spliturl = hosturl.split('<>')
    url = spliturl[1]
    hosturl = spliturl[0]
    name = spliturl[2]	
    
    if 'plugin://plugin.video.youtube' in url:
        url1 = url
    elif 'http://watch32.com' in url:
        header_dict = {}
        header_dict['Accept'] = 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5'
        header_dict['Accept-Language'] = 'en-US,en;q=0.5'
        header_dict['Connection'] = 'keep-alive'
        header_dict['Referer'] = 'http://www.youtubeonfire.com/watch.php?v=y36iVzlH4fs'#hosturl
        header_dict['Range'] = 'bytes=0-'
        header_dict['Host'] = 'watch32.com'
        header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0'
        response = requests.get(url,headers=header_dict,allow_redirects=False)
        url1 = response.headers['location']
        net.save_cookies(cookie_jar)

    elif 'docs.google.com' in url:
        header_dict = {}
        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header_dict['Accept-Language'] = 'en-US,en;q=0.5'
        header_dict['Accept-Encoding'] = 'gzip, deflate'
        header_dict['Connection'] = 'keep-alive'
        header_dict['Referer'] = hosturl
        header_dict['Host'] = 'docs.google.com'
        header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0'
        #net.set_cookies(cookie_jar)
        req = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
        #net.save_cookies(cookie_jar)
        url1 = 'https://r' + regex_from_to(req, 'https://r','https://r').replace('|', '').replace('\u003d','=').replace('\u0026','&')
    elif 'streamin.to' in url:
        header_dict = {}
        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header_dict['Accept-Language'] = 'en-US,en;q=0.5'
        header_dict['Connection'] = 'keep-alive'
        header_dict['Referer'] = hosturl
        header_dict['Host'] = 'streaming.to'
        req = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
        streamer = regex_from_to(req, 'streamer: "', '"')
        playpath = regex_from_to(req, 'file: "', '"')
        swfurl = 'http://streamin.to/player/player.swf'
        pageurl = hosturl
        url1 = "%s playpath=%s swfUrl=%s pageUrl=%s" % (streamer, playpath, swfurl, pageurl)
    else:
        header_dict = {}
        header_dict['Accept'] = 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5'
        header_dict['Accept-Language'] = 'en-US,en;q=0.5'
        header_dict['Connection'] = 'keep-alive'
        header_dict['Range'] = 'bytes=0-'
        header_dict['Referer'] = hosturl
        header_dict['Host'] = 'redirector.googlevideo.com'
        response = requests.get(url,headers=header_dict,allow_redirects=False)
        url1 = response.headers['location']
    listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, path=url1)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    handle = str(sys.argv[1])    
    if handle != "-1":
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer.play(url1, listitem)
		
def strm_movie_quality(name,url,iconimage,list):
    try:
        mpaa = name.split('[/color] ')[1]
    except:
        mpaa = name.split('[/COLOR] ')[1]
    download = ""
    if 'download' in list:
        splitlist = list.split('<>')
        url = splitlist[0]
        name = splitlist[1]
        download = splitlist[2]
    hosturl = 'http://www.movietube.co/watch.php?v=' + url
    dialog = xbmcgui.Dialog()
    menu_texts = []
    menu_data = []
    if '[color' in name:
        splitname = name.split('[color lime][max ')
        name = splitname[0].rstrip()
        q = splitname[1].replace('][/color]', '')
    else:
        splitname = name.split('[COLOR lime][max ')
        name = splitname[0].rstrip()
        q = splitname[1].replace('][/COLOR]', '')
    
    a = 'getplayerinfo'
    c = 'result'
    p = url 
    req = POST_URL(posturl,a,c,p)
	
    #PARENTAL CONTROL
    now = time.strftime("%H")
    dialog = xbmcgui.Dialog()
    if PC_ENABLE:
        mpaa = parental_control(name,mpaa)
    else:
        mpaa = 0
    pw=''
    if mpaa >= PC_RATING and PC_ENABLE and ((int(now) < int(PC_WATERSHED) and int(now) > 6) or int(PC_WATERSHED) == 25):
        keyboard = xbmc.Keyboard(pw, 'Enter your PIN/Password to play', True)
        keyboard.doModal()
        if keyboard.isConfirmed():
            pw = keyboard.getText()
        else:
            pw=''
    if int(now) >= int(PC_WATERSHED) or not(PC_ENABLE) or ((pw == PC_PASS) or mpaa < PC_RATING or (int(now) < 6 and int(PC_WATERSHED) != 25)):
        if 'src="//www.youtube.com/embed' in req:
            vlink = regex_get_all(req, 'src="//www.youtube.com/embed/', '"')
            for link in vlink:
                link = link.replace('src="//www.youtube.com/embed/', '').replace('"', '')
                url = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + link
                menu_texts.append('[COLOR lime]'+ q + '[/COLOR] | ' + name)
                menu_data.append(url)
        elif 'docs.google.com' in req:
            url = regex_from_to(req, 'src="', '"')
            try:
                size = get_file_size(url)
                size = "%.2fGB" % size
            except:
                size = ""
            menu_texts.append('[COLOR lime]'+ q + '[/COLOR] ' + size + ' | ' + name)
            menu_data.append(url)
        elif 'streamin.to' in req:
            url = regex_from_to(req, 'src="', '"')
            try:
                size = get_file_size(url)
                size = "%.2fGB" % size
            except:
                size = ""
            menu_texts.append('[COLOR lime]'+ q + '[/COLOR] ' + size + ' | ' + name)
            menu_data.append(url)
        else:
            match = re.compile('<source data-res="(.+?)" src="(.+?)"').findall(req)
            for quality, url in match:
                quality = quality + 'p'
                try:
                    size = get_file_size(url)
                    size = "%.2fGB" % size
                except:
                    size = ""
                menu_texts.append('[COLOR lime]'+ quality + '[/COLOR] ' + size + ' | ' + name)
                menu_data.append(url)
			
        if MAX_MV and not 'download' in list:
            menu_id =0
        else:
            menu_id = dialog.select('Select Quality', menu_texts)
        if(menu_id < 0):
            return (None, None)
            dialog.close()
        else:	
            url = menu_data[menu_id]
            name = menu_texts[menu_id]
        
            if download == 'download':
                download_only(name,url)	
            else:			
                strm_movie(name,url,iconimage,hosturl)
    else:
        dialog.ok("You cannot play this video","PIN incorrect")
        		
def strm_movie(name,url,iconimage,hosturl):
    splitname = name.split(' | ')
    name = splitname[1]
    
    if 'plugin://plugin.video.youtube' in url:
        url1 = url
    elif 'http://watch32.com' in url:
        header_dict = {}
        header_dict['Accept'] = 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5'
        header_dict['Accept-Language'] = 'en-US,en;q=0.5'
        header_dict['Connection'] = 'keep-alive'
        header_dict['Referer'] = 'http://www.youtubeonfire.com/watch.php?v=y36iVzlH4fs'#hosturl
        header_dict['Range'] = 'bytes=0-'
        header_dict['Host'] = 'watch32.com'
        header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0'
        response = requests.get(url,headers=header_dict,allow_redirects=False)
        url1 = response.headers['location']
        net.save_cookies(cookie_jar)
    elif 'docs.google.com' in url:
        header_dict = {}
        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header_dict['Accept-Language'] = 'en-US,en;q=0.5'
        header_dict['Connection'] = 'keep-alive'
        header_dict['Referer'] = hosturl
        header_dict['Host'] = 'docs.google.com'
        req = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
        url1 = 'https://r' + regex_from_to(req, 'https://r','https://r').replace('|', '').replace('\u003d','=').replace('\u0026','&')
    elif 'streamin.to' in url:
        header_dict = {}
        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header_dict['Accept-Language'] = 'en-US,en;q=0.5'
        header_dict['Connection'] = 'keep-alive'
        header_dict['Referer'] = hosturl
        header_dict['Host'] = 'streaming.to'
        req = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
        streamer = regex_from_to(req, 'streamer: "', '"')
        playpath = regex_from_to(req, 'file: "', '"')
        swfurl = 'http://streamin.to/player/player.swf'
        pageurl = hosturl
        url1 = "%s playpath=%s swfUrl=%s pageUrl=%s" % (streamer, playpath, swfurl, pageurl)
    else:
        header_dict = {}
        header_dict['Accept'] = 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5'
        header_dict['Accept-Language'] = 'en-US,en;q=0.5'
        header_dict['Connection'] = 'keep-alive'
        header_dict['Range'] = 'bytes=0-'
        header_dict['Referer'] = hosturl
        header_dict['Host'] = 'redirector.googlevideo.com'
        response = requests.get(url,headers=header_dict,allow_redirects=False)
        url1 = response.headers['location']
    listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, path=url1)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    handle = str(sys.argv[1])    
    if handle != "-1":
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer.play(url1, listitem)

def download_only(name,url):
    splitname=name.split(' | ')
    filename = splitname[1] + '.mp4'
    WAITING_TIME = 5
    directory=MOVIE_PATH
    data_path = os.path.join(directory, filename)#clean_file_name(name, use_blanks=False)
    dlThread = DownloadFileThread(name, url, data_path, WAITING_TIME)
    dlThread.start()
    wait_dl_only(WAITING_TIME, "Starting Download")
    if os.path.exists(data_path):
        notification('Download started', name, '5000', iconimage)
        scan_library()
		
class DownloadFileThread(Thread):
    def __init__(self, name, url, data_path, WAITING_TIME):
        self.data = url
        self.path = data_path
        self.waiting = WAITING_TIME
        self.name = name
        Thread.__init__(self)

    def run(self):
        start_time = time.time() + 20 + self.waiting
        waiting = self.waiting
        path = self.path
        data = self.data
        name = self.name
        #try:
        urllib.urlretrieve(data, path)#, lambda nb, bs, fs: self._dlhook(nb, bs, fs, self, start_time, path, waiting)
        #except:
            #if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError):
                #time.sleep(2)
                #os.remove(path)
                #return False 
            #else: 
                #raise
            #return False
        notification('Download finished', name, '5000', iconart)
		
    def _dlhook(self, numblocks, blocksize, filesize, dt, start_time, path, waiting):
        raise StopDownloading('Stopped Downloading')
        callEndOfDirectory = False
		
class StopDownloading(Exception): 
    def __init__(self, value): 
        self.value = value 
    def __str__(self): 
        return repr(self.value)
		
def get_file_size(url):
    usock = urllib2.urlopen(url)
    size = usock.info().get('Content-Length')
    if size is None:    
        size = 0
    size = float(size) # in bytes
    size = size / 1024.0# in KB (KiloBytes)
    size = size / 1024.0# in MB
    size = size / 1024.0# in GB

    return size

#KNOWLEDGE
def knowledge_menu(name):
    form_dict = {}
    form_dict['NavigatonType'] = 's'
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Accept-Language'] = 'en-US,en;q=0.5'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'knowledgetube.co'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Referer'] = 'http://knowledgetube.co/search.php'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0'
    net.set_cookies(cookie_jar)
    req = net.http_POST('http://knowledgetube.co/search.php', form_data=form_dict, headers=header_dict).content.rstrip().replace('\n', '')
    net.save_cookies(cookie_jar)
    addDir("Featured", 'http://knowledgetube.co/index.php',205,art + 'knowledge/' + 'featured.png', '1<><><><>Rate','qq')
    addDir("Newly Added", 'http://knowledgetube.co/index.php',205,art + 'knowledge/' + 'newlyadded.png', '1<><><><>addTime','qq')
    match = re.compile('<a style="(.+?)inline-block;" href="(.+?)data="(.+?)">(.+?)</a>').findall(req)
    for d1,d2,data,title in match:
        if title != 'Newly Added':
            addDir(title, 'http://knowledgetube.co/index.php',205,art + 'knowledge/' + title.replace(' ', '').lower() + '.png', '1<><>' + str(data) + '<><>Rate','qq')


#MUSIC
def music_video_menu(name):
    addDir("Billboard Chart", 'http://mvtube.co/index.php',205,art + 'music/' + 'billboardcharts.png', '1<><>BillBoard<><>','qq')
    addDir("Most Popular", 'http://mvtube.co/index.php',205,art + 'music/' + 'popular.png', '1<><><><>YouTubeView','qq')
    addDir("Top Rated", 'http://mvtube.co/index.php',205,art + 'music/' + 'toprated.png', '1<><><><>YouTubeScore','qq')
    addDir("Newly Added", 'http://mvtube.co/index.php',205,art + 'music/' + 'newlyadded.png', '1<><><><>addTime','qq')
    addDir("High Definition", 'http://mvtube.co/index.php',205,art + 'music/' + 'hd.png', '1<><><><>HD','qq')
    addDir("Moods", 'url',207,art + 'music/' + 'moods.png', '','')
    addDir("Artists", 'http://mvtube.co/index.php',208,art + 'music/' + 'artists.png', '1<><><><>','qq')
    addDir("Artist A-Z", 'url',202,art + 'music/' + 'artista-z.png', '','')
    addDir("Playlists", 'http://mvtube.co/index.php',208,art + 'music/' + 'playlists.png', '1<><><><>','qq')
    addDir("Favourite Videos", 'url',206,art + 'music/' + 'favouritevideo.png', '','')
    addDir("Favourite Artists", 'url',201,art + 'music/' + 'favouriteartist.png', '','')
	
def music_moods(name,url):
    addDir("Sexy", 'http://mvtube.co/index.php',205,art + 'music/' + 'sexy.png', '1<><>Sexy<><>YouTubeView','qq')
    addDir("Dance", 'http://mvtube.co/index.php',205,art + 'music/' + 'dance.png', '1<><>Dance<><>YouTubeView','qq')
    addDir("Love", 'http://mvtube.co/index.php',205,art + 'music/' + 'love.png', '1<><>Love<><>YouTubeView','qq')
    addDir("Happy", 'http://mvtube.co/index.php',205,art + 'music/' + 'happy.png', '1<><>Happy<><>YouTubeView','qq')
    addDir("Sad", 'http://mvtube.co/index.php',205,art + 'music/' + 'sad.png', '1<><>Sad<><>YouTubeView','qq')
    addDir("Male", 'http://mvtube.co/index.php',205,art + 'music/' + 'male.png', '1<><><>Male<>YouTubeView','qq')
    addDir("Female", 'http://mvtube.co/index.php',205,art + 'music/' + 'female.png', '1<><><>Female<>YouTubeView','qq')
	
def a_to_z(url):
    alphabet =  ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
    for a in alphabet:
        addDir(a, 'http://www.azvideos.com/%s.html' % (a.lower().replace('#', '19')),203,art + a +'.png', '','')
    
def a_to_z_list(name, url):
    link = open_url(url)
    match=re.compile('<a href="(.+?)">(.+?)</a><br><br>').findall(link)
    for url, title in match:
        url = 'http://www.azvideos.com/' + url
        addDir(title, url,204,art + 'music/' + name.lower().replace('#', '19') +'.png', '','')
        
def a_to_z_videos(name, url, iconimage):
    link = open_url(url)#d1,url,thumb,d2,d3,title
    match=re.compile('<FONT (.+?)href="../(.+?)"><img src="(.+?)" border(.+?)<a href="(.+?)">(.+?)</a></FONT>').findall(link)
    for d1,url,thumb,d2,d3,title in match:
        url = 'http://www.azvideos.com/' + url 
        addDirVideo(title,url,210,thumb,'',str(url))


def music(name,url,page,token):
    origurl = url
    token = token.replace(' ','+')

    splitpage=page.split('<>')
    page = splitpage[0]
    language = splitpage[1]
    mood = splitpage[2]
    mf = splitpage[3]
    sort = splitpage[4]
	
    if len(token)>50:
        line = token.split('\n')

    if token == 'qq':
        token = ''
        if 'billboard' in mood.lower():
            p = '{"Page":"%s","NextToken":"%s","BillBoard":"%s"}' % (page, token,mood)
        elif 'artist_pl' in sort or sort == 'playlists':
            p = '{"Keyword":"%s","Page":"%s","NextToken":"%s"}' % (language, page, token)
        elif 'knowledge' in url:
            p = '{"Page":"%s","NextToken":"%s","VideoYoutubeType":"%s","Sortby":"%s"}' % (page,token,mood,sort)
        else:
            p = '{"Page":"%s","NextToken":"%s","VideoYoutubeType":"%s","Color":"%s","SingerSex":"%s","Sortby":"%s"}' % (page,token,LANGUAGE,mood,mf,sort)
        
    else:
        if mood == 'BillBoard':
            p = '{"Page":"%s","NextToken":"%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s","BillBoard":"%s"}' % (page,line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8], mood)
        elif sort == 'artist_pl' or sort == 'playlists':
            p = '{"Keyword":"%s","Page":"%s","NextToken":"%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s"}' % (language,page,line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8])
        elif 'knowledge' in url:
            p = '{"Page":"%s","NextToken":"%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s","VideoYoutubeType":"%s","Sortby":"%s"}' % (page,line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],mood,sort)
        else:
            p = '{"Page":"%s","NextToken":"%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s","VideoYoutubeType":"%s","Color":"%s","SingerSex":"%s","Sortby":"%s"}' % (page,line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],LANGUAGE,mood,mf,sort)
    a = 'retrieve'
    if 'billboard' in mood.lower():
        c = 'chart'
    elif 'artist_pl' in sort:
        c = 'detail'
        a = 'retrievesingers'
    elif sort == 'playlists':
        c = 'detail'
        a = 'retrieveplaylists'
    else:
        c = 'song'
        a = 'retrieve'
		
    req = POST_URL(url,a,c,p).replace('&nbsp', '').replace("'", '"')
    token = str(req).split('|')[0]
    #token = token.replace('%0a', '\n')

    if 'knowledge' in url:
        match = re.compile('<tr style="(.+?)<img src="(.+?)" /></a></td><td><div class="dtl"><span class="dtl_name">(.+?)">(.+?)</a></span><br/>(.+?)<div class="vors">(.+?)</div></td><td width="250"><div class="ctm"></div></td><td width="50"><div class="ytlk"><a href="(.+?)v=(.+?)" target="_blank"><img src="./views/images/ytlink.png" /></a></div></td></tr>').findall(req)
        for d1,thumb,d2,title,d3,dt,d4,vurl in match:
            title = title.decode("utf8").encode("utf8").replace('"',"'")
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + vurl
            addDirVideo(title,'useicon',210,thumb,'',str(vurl))
    else:
        match2 = re.compile('<tr style="(.+?)value="(.+?)<div class="idx">(.+?)</div></td><td width="(.+?)<img src="(.+?)" /></a></td><td><div class="dtl"><span class="dtl_name">(.+?)">(.+?)</a></span><span class="dtl_singer">(.+?)watch.(.+?)v=(.+?)" target="_blank"><img src="./views/images/ytlink.png" /></a></div></td></tr>').findall(req)
        for d1,d2,pos,d3,thumb,d4,title,d5,d6,vurl in match2:
            title = title.decode("utf8").encode("utf8").replace('"',"'")
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + vurl
            addDirVideo(title,'useicon',210,thumb,'',str(vurl))
    if len(token)>50:		
        nextpage=int(page)+1
        print language
        nextpage = "%s<>%s<>%s<>%s<>%s" % (nextpage,language,mood,mf,sort)
        addDir("Next Page", origurl,205,art +  'nextpage.png', nextpage,token)
		
def queue_all(name,url,page,token):
    token = token.replace('%0a', '\n')
    splitpage=page.split('<>')
    page = splitpage[0]
    language = splitpage[1]
    mood = splitpage[2]
    mf = splitpage[3]
    sort = splitpage[4]
	
    if len(token)>50:
        line = token.split('\n')

   
    if token == 'qq':
        token = ''
        if 'billboard' in name.lower():
            p = '{"Page":"%s","NextToken":"%s","BillBoard":"%s"}' % (page, token, mood)
        elif 'artist_pl' in sort or sort == 'playlists':
            p = '{"Keyword":"%s","Page":"%s","NextToken":"%s"}' % (language, page, token)
        else:
            p = '{"Page":"%s","NextToken":"%s","VideoYoutubeType":"%s","Color":"%s","SingerSex":"%s","Sortby":"%s"}' % (page,token,LANGUAGE,mood,mf,sort)
        
    else:
        if 'billboard' in name.lower():
            p = '{"Page":"%s","NextToken":"%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s","BillBoard":"%s"}' % (page,line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],mood)
        elif sort == 'artist_pl' or sort == 'playlists':
            p = '{"Keyword":"%s","Page":"%s","NextToken":"%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s"}' % (language,page,line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8])
        else:
            p = '{"Page":"%s","NextToken":"%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s","VideoYoutubeType":"%s","Color":"%s","SingerSex":"%s","Sortby":"%s"}' % (page,line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],LANGUAGE,mood,mf,sort)
    a = 'retrieve'
    if 'billboard' in name.lower():
        c = 'chart'
    elif 'artist_pl' in sort:
        c = 'detail'
        a = 'retrievesingers'
    elif sort == 'playlists':
        c = 'detail'
        a = 'retrieveplaylists'
    else:
        c = 'song'
		
    req = POST_URL(url,a,c,p).replace('&nbsp', '').replace("'", '"')
    token = str(req).split('|')[0]
    token = token.replace('%0a', '\n')

    match2 = re.compile('<tr style="(.+?)value="(.+?)<div class="idx">(.+?)</div></td><td width="(.+?)<img src="(.+?)" /></a></td><td><div class="dtl"><span class="dtl_name">(.+?)">(.+?)</a></span><span class="dtl_singer">(.+?)watch.(.+?)v=(.+?)" target="_blank"><img src="./views/images/ytlink.png" /></a></div></td></tr>').findall(req)
    for d1,d2,pos,d3,thumb,d4,title,d5,d6,vurl in match2:
        title = title.decode("utf8").encode("utf8").replace('"',"'")
        url = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + vurl
        play_music_video(title, url, thumb,False)
	
def music_artists(name,url,page,token):
    splitpage=page.split('<>')
    page = splitpage[0]
    language = splitpage[1]
    mood = splitpage[2]
    mf = splitpage[3]
    sort = splitpage[4]
    
    if token == 'qq':
        token = ''
        p = '{"Page":"%s","NextToken":"%s"}' % (page, token)
    else:
        line = token.split('\n')
        p = '{"Page":"%s","NextToken":"%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s\\n%s"}' % (page,line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8])
    a = 'retrieve'
    if 'artist' in name.lower():
        c = 'artist'
    else:
        c = 'playlist'
    req = POST_URL(url,a,c,p).replace('&nbsp', '')
    try:
        token = str(req).split('|')[0]
    except:
        pass
    if c == 'artist': 
        match = re.compile('<li><span class="pdl3"><b>(.+?)</b></span>(.+?)data="(.+?)"><img src="(.+?)" width=(.+?)data="(.+?)">(.+?)</a></span></li>').findall(req)
        for pos,d1,artist,thumb,d2,data,d3 in match:
            url = 'http://mvtube.co/index.php'
            data = "%s<>%s<>%s<>%s<>%s" % ('1',data,'','','artist_pl')
            addDir(artist, url,205,thumb, data,'qq')
        nextpage=int(page)+1
        nextpage = "%s<>%s<>%s<>%s<>%s" % (nextpage,language,mood,mf,sort)
        addDir("Artist Next Page", 'http://mvtube.co/index.php',208,art +  'nextpage.png', nextpage,token)
    else:                  #
        all_pl = regex_get_all(req,'<li>', '</li>')
        for pl in all_pl:
            url = 'http://mvtube.co/index.php'
            data1 = regex_from_to(pl, 'data="', '"')
            thumb = regex_from_to(pl, 'img src="', '"')
            title = regex_from_to(pl, 'class="grey" data="', '</span>')
            title = regex_from_to(title, '">', '</a>').lstrip()
            data = "%s<>%s<>%s<>%s<>%s" % ('1',data1,'','','playlists')
            addDir(title, url,205,thumb, data,'qq')


	
def favourites_music():
    if os.path.isfile(FAV_MUSIC):
        s = read_from_file(FAV_MUSIC)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                title = title.replace('->-', ' & ')
                url = list1[1]
                thumb = list1[2]
                if 'azvideo' in url:
                   addDirVideo(title,url,210,thumb,'mus',url)
                else:
                    addDirVideo(title,'useicon',210,thumb,'mus',url)
				
def favourite_artists():
    if os.path.isfile(FAV_ARTISTS):
        s = read_from_file(FAV_ARTISTS)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                title = title.replace('->-', ' & ')
                url = list1[1]
                thumb = list1[2]
                if 'mvtube' in url:
                    data = "%s<>%s<>%s<>%s<>%s" % ('1',list1[4],list1[5],list1[6],'favartist_pl')
                    addDir(title, url,205,thumb, data,'qq')
                else:
                    data = "%s<>%s<>%s<>%s<>%s" % ('','','','','favartist_pl')
                    addDir(title, url,204,thumb, data,'qq')

def play_music_video(name, url, iconimage,clear):
    if 'azvideo' in url:
        link = open_url(url)
        if 'dailymotion' in link:
            url = regex_from_to(link, 'movie" value="', '"').replace('swf', 'embed/video')
            link = open_url(url)
            if 'stream_h264_hd1080_url":"http' in link:
                url = regex_from_to(link, 'stream_h264_hd1080_url":"', '"').replace('\/', '/')
            elif 'stream_h264_hd_url":"http' in link:
                url = regex_from_to(link, 'stream_h264_hd_url":"', '"').replace('\/', '/')
            elif 'stream_h264_hq_url":"http' in link:
                url = regex_from_to(link, 'stream_h264_hq_url":"', '"').replace('\/', '/')
            elif 'stream_h264_ld_url":"http' in link:
                url = regex_from_to(link, 'stream_h264_ld_url":"', '"').replace('\/', '/')
            elif 'stream_h264_url":"http' in link:
                url = regex_from_to(link, 'stream_h264_url":"', '"').replace('\/', '/')
        else:
            vurl = regex_from_to(link, 'src="//www.youtube.com/embed/', '"')
            url = str('plugin://plugin.video.youtube/?action=play_video&videoid=' + vurl)
    
    if url == 'useicon':
        url = iconimage
    if 'http://img.youtube.com/vi/' in url:
        iconimage = url
        vurl = regex_from_to(url, 'http://img.youtube.com/vi/', '/mqdefault')
        url = str('plugin://plugin.video.youtube/?action=play_video&videoid=' + vurl)
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
			
	

def add_favourite(name, url, iconimage, dir, text):
    list_data = iconimage.replace('hhhh', 'http:')
    splitdata = list_data.split('<>')
    name = splitdata[0]
    name = name.replace('->-', ' & ').replace('qq', ',')
    thumb = splitdata[2]
    add_to_list(list_data, dir)
    notification(name, "[COLOR lime]" + text + "[/COLOR]", '5000', thumb)
	
def remove_from_favourites(name, url, iconimage, dir, text):
    list_data = iconimage.replace('hhhh', 'http:')
    splitdata = list_data.split('<>')
    name = splitdata[0]
    name = name.replace('->-', ' & ').replace('qq', ',')
    thumb = splitdata[2]
    remove_from_list(list_data, dir)
    notification(name, "[COLOR orange]" + text + "[/COLOR]", '5000', thumb)
	


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
	
def create_strm_file(name, url, mode, dir_path, iconimage,list):
    splitlist = list.split('<>')
    list = splitlist[0]
    name = splitlist[1]
    if '[color' in name:
        splitname = name.split('[color lime][max ')
        name1 = splitname[0].rstrip()
    else:
        splitname = name.split('[COLOR lime][max ')
        name1 = splitname[0].rstrip()
	
    try:
        strm_string = create_url(name, mode, url=list, iconimage=iconimage, list=list)
        #name1 = re.sub(r'\[[^]]*\]', '', name1)
        filename = clean_file_name("%s.strm" % name1)
        path = os.path.join(dir_path, filename)
        if not os.path.exists(path):
            stream_file = open(path, 'w')
            stream_file.write(strm_string)
            stream_file.close()
            scan_library()
    except:
        xbmc.log("[YouTube on Fire] Error while creating strm file for : " + name)
		
def create_url(name, mode, url, iconimage, list):
    name = urllib.quote(str(name))
    data = str(url)
    iconimage = urllib.quote(str(iconimage))
    list = urllib.quote(str(list))
    mode = str(mode)
    url = sys.argv[0] + '?name=%s&url=%s&mode=%s&iconimage=%s&list=%s' % (name, data, mode, iconimage, list)
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
		
def scan_library():
    if xbmc.getCondVisibility('Library.IsScanningVideo') == False:           
        xbmc.executebuiltin('UpdateLibrary(video)')

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
    print query
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        for l in lines:
            print l
        index = lines.index(query)
        return index
    except:
        return -1
		
def add_to_list(list, file):
    list = list.replace('artist_pl', 'favartist_pl')
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
		
def get_meta(name,types=None,year=None):
    if 'movie' in types:
        meta = metainfo.get_meta('movie',name,year)
    infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Aired': meta['premiered']}
        
    return infoLabels
	
def youtubefix():
    shutil.copy2(ytplayerorig, ytplayerbak)
    shutil.copy2(ytplayerfixed, ytplayercopyto)    
    notification('YouTube Player Fix Applied', 'Fix Applied, original backed up', '3000', iconart)	
		
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
        favlist="%s<>%s<>%s" % (name.replace(',', 'qq'),url,iconimage)
        favlist2="%s<>%s<>%s<>%s" % (name,url,iconimage,list)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+str(iconimage)+"&list="+str(list)+"&description="+str(description)
        ok=True
        contextMenuItems = []
        if "mov" in description:
            contextMenuItems.append(("[COLOR cyan]Download Movie[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=109&iconimage=%s&list=%s)'%(sys.argv[0], name, url,iconimage, str(url)+'<>'+str(name)+'<>'+'download')))
            contextMenuItems.append(("[COLOR lime]Add to XBMC Library[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=106&iconimage=%s&list=%s)'%(sys.argv[0], name, url,iconimage, str(url)+'<>'+str(name))))
            if description != 'movfav':
                suffix = ""
                contextMenuItems.append(("[COLOR lime]Add to Addon Favourites[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=11&list=%s)'%(sys.argv[0], name.replace(',', ' '), url, str(favlist).replace('http:','hhhh'))))
            else:
                suffix = ' [COLOR lime]+[/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from Addon Favourites[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=13&list=%s)'%(sys.argv[0], name.replace(',', ' '), url, str(favlist).replace('http:','hhhh'))))
        if 'mvtube' in url or 'azvideo'in url:
            if 'favartist_pl' in list:
                contextMenuItems.append(('Remove from Favourites', 'XBMC.RunPlugin(%s?mode=215&name=%s&url=%s&iconimage=%s)'% (sys.argv[0], name, iconimage, favlist2)))
            elif mode == 205 or mode == 204:
                contextMenuItems.append(('Mark as Favourite', 'XBMC.RunPlugin(%s?mode=214&name=%s&url=%s&iconimage=%s)'% (sys.argv[0], name, iconimage, favlist2)))
            contextMenuItems.append(("[COLOR lime]Queue all videos[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=209&list=%s&description=%s)'%(sys.argv[0], name, url,list, description)))
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
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.unquote_plus(iconimage)+"&showname="+urllib.quote_plus(showname)
        ok=True
        
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels=infoLabels)
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
	
def addDirVideo(name,url,mode,iconimage,list,vurl):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+str(iconimage)+"&list="+str(list)+"&vurl="+str(vurl)
        ok=True
        text = "%s<>%s<>%s" % (name, vurl,iconimage)
        text1 = "%s<>%s<>%s" % (name, url,iconimage)
        if list == 'mus':
            contextMenuItems.append(('Remove from Favourites', 'XBMC.RunPlugin(%s?mode=213&name=%s&url=%s&iconimage=%s)'% (sys.argv[0], name, iconimage, text)))
        else:
            if 'azvideo' in url:
                contextMenuItems.append(('Mark as Favourite', 'XBMC.RunPlugin(%s?mode=212&name=%s&url=%s&iconimage=%s)'% (sys.argv[0], name, iconimage, text1)))
            else:
                contextMenuItems.append(('Mark as Favourite', 'XBMC.RunPlugin(%s?mode=212&name=%s&url=%s&iconimage=%s)'% (sys.argv[0], name, iconimage, text)))
        if 'azvideo' in url:
            contextMenuItems.append(('Queue video', 'XBMC.RunPlugin(%s?mode=211&name=%s&iconimage=%s&url=%s)'% (sys.argv[0], name,iconimage,url)))
        else:
            contextMenuItems.append(('Queue video', 'XBMC.RunPlugin(%s?mode=211&name=%s&iconimage=%s&url=%s)'% (sys.argv[0], name,vurl,iconimage)))
        
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, False)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
      
              
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
try:
        vurl=str(params["vurl"])
except:
        pass


if mode==None or url==None or len(url)<1:
        CATEGORIES(name)
        #GET_URL(movie_url)
        
elif mode==100:
        movie_directory(name)
		
elif mode==101:
        movie_directory_1(name)
		
elif mode==102:
        movie_directory_2(name)
		
elif mode==103:
        movie_directory_3(name,url)
		
elif mode==104:
        search_movie()
		
elif mode==105:
        favourites_movies()
		
elif mode==106:
        create_strm_file(name, url, '109', MOVIE_PATH, iconimage,list)
		
elif mode==3:
        movie_quality(name,url,iconimage,list)
		
elif mode==5:
        play_movie(name,url,iconimage,showname)
		
elif mode==109:
        strm_movie_quality(name,url,iconimage,list)
		
elif mode==110:
        strm_movie(name,url,iconimage,showname)
		
elif mode==111:
        download_only(name,url)
		
elif mode==6:
        search()
		
elif mode==7:
        movies(name,url,list,description)
		
elif mode == 17:
        search_show(name)
		
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
		
elif mode == 200:
        music_video_menu(name)
		
elif mode==201:
        favourite_artists()
		
elif mode == 202:
        a_to_z(url)
		
elif mode == 203:
        a_to_z_list(name,url)
		
elif mode == 204:
        a_to_z_videos(name, url, iconimage)
		
elif mode == 205:
        music(name,url,list,description)
		
elif mode==206:
        favourites_music()

elif mode==207:
        music_moods(name,url)
		
elif mode == 208:
        music_artists(name,url,list,description)
		
elif mode == 209:
        queue_all(name,url,list,description)
		
elif mode == 210:
        play_music_video(name, url, iconimage,True)
		
elif mode == 211:
        play_music_video(name, url, iconimage,False)
		
elif mode == 212:
        add_favourite(name, url, iconimage, FAV_MUSIC, "Added to Favourites")
	
elif mode == 213:
        remove_from_favourites(name, url, iconimage, FAV_MUSIC, "Removed from Favourites")
		
elif mode == 214:
        add_favourite(name, url, iconimage, FAV_ARTISTS, "Added to Favourites")
	
elif mode == 215:
        remove_from_favourites(name, url, iconimage, FAV_ARTISTS, "Removed from Favourites")
		
elif mode == 216:
        play_az(name,url,iconimage)
		
elif mode == 300:
        knowledge_menu(name)

elif mode == 800:
        pc_setting()
		
elif mode == 999:
        youtubefix()
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))



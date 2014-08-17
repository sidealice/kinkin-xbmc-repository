'''
kinkin
'''

import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import settings
import time,datetime
from datetime import date, datetime
from threading import Timer
from hashlib import md5
import hashlib
from helpers import clean_file_name
import json
import glob
import shutil
from threading import Thread
import cookielib
from t0mm0.common.net import Net
from helpers import clean_file_name
import urlresolver
from metahandler import metahandlers
metainfo = metahandlers.MetaData()
net = Net()
if os.path.exists(xbmc.translatePath("special://home/addons/")+'script.module.hubparentalcontrol'):
    HUBPC = True
    from hubparentalcontrol import parentalcontrol
else:
    HUBPC = False


ADDON = settings.addon()
TRAILER_RESTRICT = settings.restrict_trailer()
TRAILER_QUALITY = settings.trailer_quality()
TRAILER_ONECLICK = settings.trailer_one_click()
MS_ACCOUNT = settings.ms_account()
MS_USER = settings.ms_user()
MS_PASSWORD = settings.ms_pass()
ENABLE_SUBS = settings.enable_subscriptions()
AUTOPLAY = settings.autoplay()
TV_PATH = settings.tv_directory()
MOVIE_PATH = settings.movie_directory()
CACHE_PATH = settings.cache_path()
FAV = settings.favourites_file()
FAV_MOVIE = settings.favourites_movies_file()
SUB = settings.subscription_file()
ENABLE_META = settings.enable_meta()
cookie_jar = settings.cookie_jar()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'fanart.jpg'))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'icon.png'))
base_url = 'http://www.flixanity.com/'


def open_url(url,referer, cache_time=3600):
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'www.flixanity.com'
    header_dict['Referer'] = referer
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0'
    header_dict['Connection'] = 'keep-alive'
    h = hashlib.md5(url).hexdigest()
    cache_file = os.path.join(CACHE_PATH, h)
    age = get_file_age(cache_file)
    if age > 0 and age < cache_time:
        r = read_from_file(cache_file, silent=True)
        if r:
            return r
    else:
        net.set_cookies(cookie_jar)
        link = net.http_GET(url,  headers=header_dict).content.encode("utf-8").rstrip()
        net.save_cookies(cookie_jar)
        write_to_file(cache_file, link)
        return link
	
def open_gurl(url, cache_time=3600):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0')
    h = hashlib.md5(url).hexdigest()
    cache_file = os.path.join(CACHE_PATH, h)
    age = get_file_age(cache_file)
    print "FliXanity.........FILE AGE IS " + str(age)
    if age > 0 and age < cache_time:
        r = read_from_file(cache_file, silent=True)
        print "FliXanity.........use CACHE"
        if r:
            return r
    else:
        response = urllib2.urlopen(req)
        link=response.read()
        write_to_file(cache_file, link)
        print "FliXanity.........NO CACHE"
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
	
def login():
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'www.flixanity.com'
    header_dict['Referer'] = 'http://www.flixanity.com/'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0'
    header_dict['Connection'] = 'keep-alive'#

    ### Login ###
    if MS_USER != '':
        form_data = ({'action': 'login', 'username': MS_USER, 'password': MS_PASSWORD})	
        net.set_cookies(cookie_jar)
        loginlink = net.http_POST('http://www.flixanity.com/', form_data=form_data, headers=header_dict).content.encode("utf-8").rstrip()
        if 'Welcome Back %s' % MS_USER in loginlink:
            notification('FliXanity', 'Welcome Back %s' % MS_USER, '4000', iconart)
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

	
def CATEGORIES(name):
    if MS_USER != "" and MS_ACCOUNT:
        try:
            login()
        except:
            pass
    addDir("Movies", 'url',101,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'movies.png')), '','')
    addDir("TV Shows", 'url',102,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'tvshows.png')), '','')
    addDir("Favourite Movies", 'url',19,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'favouritemovies.png')), '','')
    addDir("Favourite TV Shows", 'url',12,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'favouritetvshows.png')), '','')
    addDir("TV Subscriptions", 'url',16,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'tvshowsubscriptions.png')), '','')
		 
def movie_menu():
    addDir("Box Office Movies", 'http://www.flixanity.com/featuredmovies',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'boxoffice.png')), '1','a')
    addDir("HD Movies", 'http://www.flixanity.com/hdmovies',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'movies.png')), '1','a')
    addDir("New Movies", 'http://www.flixanity.com/new-movies',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'newmovies.png')), '1','a')
    addDir("Alphabetical", 'http://www.flixanity.com/movies/abc',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'a-z.png')), '1','a')
    addDir("IMDB Rating", 'http://www.flixanity.com/movies/imdb_rating',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'imdbrating.png')), '1','a')
    addDir("Popular Movies", 'http://www.flixanity.com/movies/favorites',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'popular.png')), '1','a')
    addDir("All Movies", 'http://www.flixanity.com/movies',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'all.png')), '1','a')
    addDir("Movie Genres", 'url',4,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'genres.png')), '1','')
    addDir("Search Movies", 'url',6,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'search.png')), '1','')
    if MS_ACCOUNT:
        addDir("Movie Picks 4 U", 'http://www.flixanity.com/recommend-movies',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'toppicks.png')), '1','')

def movie_genre_menu(url):
    addDir("Adventure", 'http://www.flixanity.com/movie-tags/adventure',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'adventure.png')), '1','a')
    addDir("Animation", 'http://www.flixanity.com/movie-tags/animation',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'animation.png')), '1','a')
    addDir("Biography", 'http://www.flixanity.com/movie-tags/adventure',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'biography.png')), '1','a')
    addDir("Comedy", 'http://www.flixanity.com/movie-tags/comedy',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'comedy.png')), '1','a')
    addDir("Crime", 'http://www.flixanity.com/movie-tags/crime',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'crime.png')), '1','a')
    addDir("Documentary", 'http://www.flixanity.com/movie-tags/documentary',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'documentary.png')), '1','a')
    addDir("Drama", 'http://www.flixanity.com/movie-tags/drama',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'drama.png')), '1','a')
    addDir("Family", 'http://www.flixanity.com/movie-tags/family',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'family.png')), '1','a')
    addDir("Fantasy", 'http://www.flixanity.com/movie-tags/fantasy',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'fantasy.png')), '1','a')
    addDir("Horror", 'http://www.flixanity.com/movie-tags/horror',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'horror.png')), '1','a')
    addDir("Music", 'http://www.flixanity.com/movie-tags/music',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'music.png')), '1','a')
    addDir("Musical", 'http://www.flixanity.com/movie-tags/musical',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'musical.png')), '1','a')
    addDir("Romance", 'http://www.flixanity.com/movie-tags/romance',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'romance.png')), '1','a')
    addDir("Sci-Fi", 'http://www.flixanity.com/movie-tags/sci-fi',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'scifi.png')), '1','a')
    addDir("Sport", 'http://www.flixanity.com/movie-tags/sport',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'sport.png')), '1','a')
    addDir("Thriller", 'http://www.flixanity.com/movie-tags/thriller',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'thriller.png')), '1','a')
    addDir("War", 'http://www.flixanity.com/movie-tags/war',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'war.png')), '1','a')
    addDir("Western", 'http://www.flixanity.com/movie-tags/western',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'western.png')), '1','a')
    addDir("WWE/WWF", 'http://www.flixanity.com/movie-tags/wwf-wwe',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'wwewwf.png')), '1','a')	

def tvseries_menu():
    addDir("Newest Episodes", 'http://www.flixanity.com/new-shows',5,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'newepisodes.png')), '1','n')
    addDir("Newest Shows", 'http://www.flixanity.com/tv-shows/date',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'newtvshows.png')), '1','a')
    addDir("Alphabetical", 'url',108,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'a-z.png')), '1','alpha')
    addDir("IMDB Rating", 'http://www.flixanity.com/tv-shows/imdb_rating',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'imdbrating.png')), '1','a')
    addDir("All TV Shows", 'http://www.flixanity.com/tv-shows',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'all.png')), '1','a')
    addDir("TV Show Genres", 'url',7,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'genres.png')), '1','a')
    addDir("Search TV Shows", 'url',6,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'search.png')), '1','n') 
    addDir("TV Schedule", 'http://www.flixanity.com/tvschedule',109,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'tvshows.png')), '1','n')

def tvshow_genre_menu(url):
    addDir("Adventure", 'http://www.flixanity.com/tv-tags/adventure',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'adventure.png')), '1','a')
    addDir("Animation", 'http://www.flixanity.com/tv-tags/animation',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'animation.png')), '1','a')
    addDir("Comedy", 'http://www.flixanity.com/tv-tags/comedy',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'comedy.png')), '1','a')
    addDir("Crime", 'http://www.flixanity.com/tv-tags/crime',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'crime.png')), '1','a')
    addDir("Documentary", 'http://www.flixanity.com/tv-tags/documentary',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'documentary.png')), '1','a')
    addDir("Drama", 'http://www.flixanity.com/tv-tags/drama',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'drama.png')), '1','a')
    addDir("Family", 'http://www.flixanity.com/tv-tags/family',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'family.png')), '1','a')
    addDir("Fantasy", 'http://www.flixanity.com/tv-tags/fantasy',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'fantasy.png')), '1','a')
    addDir("Food TV", 'http://www.flixanity.com/tv-tags/foodtv',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'foodtv.png')), '1','a')
    addDir("Horror", 'http://www.flixanity.com/tv-tags/horror',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'horror.png')), '1','a')
    addDir("Kids", 'http://www.flixanity.com/tv-tags/kids',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'kids.png')), '1','a')
    addDir("Music", 'http://www.flixanity.com/tv-tags/music',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'music.png')), '1','a')
    addDir("Mystery", 'http://www.flixanity.com/tv-tags/mystery',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'mystery.png')), '1','a')
    addDir("Top Picks", 'http://www.flixanity.com/tv-tags/our-top-picks',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'toppicks.png')), '1','a')
    addDir("Reality TV", 'http://www.flixanity.com/tv-tags/reality-tv',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'realitytv.png')), '1','a')
    addDir("Romance", 'http://www.flixanity.com/tv-tags/romance',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'romance.png')), '1','a')
    addDir("Sci-Fi", 'http://www.flixanity.com/tv-tags/sci-fi',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'scifi.png')), '1','a')
    addDir("Sport", 'http://www.flixanity.com/tv-tags/sport',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'sport.png')), '1','a')
    addDir("Talk Shows", 'http://www.flixanity.com/tv-tags/talk-show',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'talkshows.png')), '1','a')
    addDir("Thriller", 'http://www.flixanity.com/tv-tags/thriller',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'thriller.png')), '1','a')
    addDir("War", 'http://www.flixanity.com/tv-tags/war',29,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'war.png')), '1','a')

def tvschedule(url):
    url = 'http://www.flixanity.com/tvschedule/20140711'
    #time.strftime("%Y%m%d")
    count = 0
    link = open_gurl(url)
    all_episodes = regex_get_all(link, '<tr class="sch_last">', '</tr>')
    for a in all_episodes:
        all_td = regex_get_all(link, '<td>', '</td>')
        count = count + 1
        if count < 51:
            thumb = regex_from_to(all_td[0], '<img src="', '"')
            try:
                url = regex_from_to(all_td[0], '</a><a href="', '"')
            except:
                url = 'not available'
            showname = regex_from_to(all_td[1],'">', '<')
            title = regex_from_to(all_td[1], '<br />', '<')
            spliturl = url.split('/')
            episode = spliturl[8]
            season = spliturl[6]
            name = title
            if ENABLE_META:
                infoLabels=get_meta(showname,'episode',year=None,season=season,episode=episode)
                if infoLabels['title']=='':
                    name=title
                else:
                    name="%s - %sx%s  %s" % (showname,season,episode,infoLabels['title'])
                if infoLabels['cover_url']=='':
                    iconimage=thumb
                else:
                    iconimage=infoLabels['cover_url']
            else:
                infoLabels =None
                iconimage=thumb
                name = showname + ' - ' + title
            try:
                if AUTOPLAY:
                    addDirPlayable(name, url,2,iconimage, showname,infoLabels=infoLabels)
                else:
                    addDir(name, url,2,iconimage, showname,'sh',infoLabels=infoLabels)
            except:
                pass
    setView('episodes', 'episodes-view')


def a_to_z(url):
    alphabet =  ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
    for a in alphabet:
        addDir(a, 'http://www.flixanity.com/tv-shows/abc',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'a-z.png')), '1','alpha')
		
def Main_sort(name,url,list,showname):
    if 'tv' not in url:
        addDir("Year", url + '/year',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'movies.png')), '1','a')
    addDir("ABC", url + '/abc',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'movies.png')), '1','a')
    addDir("Newest", url + '/date',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'movies.png')), '1','a')
    addDir("IMDB Rating", url + '/imdb_rating',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'movies.png')), '1','a')
    if 'hdmovies' in url:
        addDir("Popular", url + '/favorites',1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'movies.png')), '1','a')
	
def Main(name,url,page,pagin):
    HD = ''
    nm = name
    if pagin == 'alpha' and nm == '#':
        nm = 'AAA'
    if '<>' in pagin:
        nexturl=url
        minpage = pagin.split('<>')[0]
        maxpage = pagin.split('<>')[1]
        nextmin = int(maxpage) + 1
        nextmax = int(maxpage) + 50
        nextlist = "%s<>%s" % (nextmin,nextmax)
    else:
        minpage = '0'
        maxpage = '1000'
    trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
    dp = xbmcgui.DialogProgress()
    dp.create("FliXanity",'Searching')
    dp.update(0)
    url1 = url
    url = "%s/%s" % (url,page)
    nextpage = int(page) + 1
    referer = 'http://www.flixanity.com/'
    link = open_gurl(url).replace('\n', '').replace('\t', '').replace('\u00e0', 'a')
    data = regex_from_to(link, 'MAIN CONTAINER', 'div id="footer')
    match = re.compile('<div class=(.+?)<img class="img-preview spec-border"(.+?)src="(.+?)" alt="(.+?)<h3><a href="(.+?)">(.+?)</a></h3>').findall(data)
    if '<>' in pagin:
        nAllItem = len(match)
        nItem = 50
    else:
        nItem = len(match)
    count = 0
    for ribbon,d2,thumb,d1,url,title in match:
        if '>HD<' in ribbon:
            HD = 'HD'
        if '>NEW<' in ribbon:
            HD = 'NEW'
        if title[:1] == '0' or title[:1] == '1' or title[:1] == '2' or title[:1] == '3' or title[:1] == '4' or title[:1] == '5' or title[:1] == '6' or title[:1] == '7' or title[:1] == '8' or title[:1] == '9':
            cap = 'AAA'
        else:
            cap = title[:1]
        name = title
        count = count + 1
        if (pagin == 'alpha' and cap == nm) or (pagin != 'alpha' and (count >= int(minpage) and count <= int(maxpage))):
            id = regex_from_to(thumb, 'thumbs/', '.jpg')
            thumb = 'http://www.flixanity.com/templates/trakt/timthumb.php?src=http://www.flixanity.com/thumbs/%s.jpg&w=200&h=300&zc=1' % id
            if '<>' in pagin:
                titlelist = str(count - int(minpage)) + ' of ' + str(nItem) + ' (' + str(nAllItem) + ' total): ' + title
            elif pagin == 'alpha':
                titlelist = title
            else:
                titlelist = str(count) + ' of ' + str(nItem) + ': ' + title
            progress = count / float(nItem) * 100               
            dp.update(int(progress), 'Adding title',titlelist)
            if dp.iscanceled():
                return
            if not 'shows' in url1 and not 'tv-tags' in url1:
                if ENABLE_META:
                    infoLabels = get_meta(title,'movie')
                    if infoLabels['title']=='':
                        name=title
                    else:
                        name=infoLabels['title']
                    if infoLabels['cover_url']=='':
                        iconimage=thumb
                    else:
                        iconimage=infoLabels['cover_url']
                    if infoLabels['year']=='':
                        year=''
                    else:
                        year=" (%s)" % infoLabels['year']
                else:
                    infoLabels =None
                    iconimage=thumb
                    year = ''
                name2 = "%s%s [COLOR cyan]%s[/COLOR]" % (name.replace('\u00e0', 'a'), year, HD)
                if AUTOPLAY:
                    addDirPlayable(name2, url,2,iconimage, 'movies',infoLabels=infoLabels)
                else:
                    addDir(name2, url,2,iconimage, title,'movies',infoLabels=infoLabels)
                setView('movies', 'movies-view')
            else:
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
                    if infoLabels['year']=='':
                        year=''
                    else:
                        year=" (%s)" % infoLabels['year']
                else:
                    infoLabels =None
                    iconimage=thumb
                    year = ''
                name2 = "%s%s [COLOR cyan]%s[/COLOR]" % (name.replace('\u00e0', 'a'), year, HD)
                addDir(name2, url,103,iconimage, 'sh',title,infoLabels=infoLabels)
                setView('tvshows', 'tvshows-view')
    if not '<>' in pagin:#'Box Office' not in nm and 'New Movies' not in nm and 'New Episodes' not in nm and not 'shows' in url1 and not 'tv-tags' in url1
        addDir("Next Page >>", url1,1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.flixanity', 'art', 'new.png')), nextpage,'a')
    elif '<>' in pagin and nextmin < nAllItem:
        addDir('Next page (' + nextlist.replace('<>','-') + ')', nexturl,1,'', '1',nextlist)
	
def tvseries_seasons(name,url,thumb,showname):
    showname = name[:name.find('(')]
    thumb = thumb + '&w=200&h=300&zc=1'
    url1 = url
    link = open_gurl(url)
    data = regex_from_to(link, 'id="season-list"', '</ul>')
    match = re.compile("<a href='(.+?)'>(.+?)</a>").findall(data)
    for url, title in match:
        if ENABLE_META:
            season = title.replace('Season ', '')
            infoLabels=get_meta(showname,'tvshow',year=None,season=season,episode=None)
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
        addDir(title, url,104,iconimage, 'sh', showname,infoLabels=infoLabels)
    setView('seasons', 'seasons-view')
		
def tvseries_episodes(name, url, thumb, showname):
    trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
    nm = name
    thumb = thumb + '&w=200&h=300&zc=1'
    url1 = url
    link = open_gurl(url)
    all_episodes = regex_get_all(link, '<li class="episodes">', '<span class="item-overlay">')
    for a in all_episodes:
        thumb = regex_from_to(a, 'show-thumbnail"  src="', '"')
        titleurl = regex_from_to(a, '<a class="link"', '</a>')
        title = regex_from_to(titleurl, 'title="', '"').replace('Season ', '').replace(', Episode ', 'x')
        url = regex_from_to(titleurl, 'href="', '"')
        spliturl = url.split('/')
        episode = spliturl[8]
        season = spliturl[6]
        name = title
        if ENABLE_META:
            
            infoLabels=get_meta(showname,'episode',year=None,season=season,episode=episode)
            if infoLabels['title']=='':
                name=title
            else:
                name="%sx%s  %s" % (season,episode,infoLabels['title'])
            if infoLabels['cover_url']=='':
                iconimage=thumb
            else:
                iconimage=infoLabels['cover_url']
        else:
            infoLabels =None
            iconimage=thumb
        #name = name.translate(trans_table)
        if AUTOPLAY:
            addDirPlayable(name, url,2,iconimage, showname,infoLabels=infoLabels)
        else:
            addDir(name, url,2,iconimage, 'sh', showname,infoLabels=infoLabels)
    setView('episodes', 'episodes-view')
    if ENABLE_META:
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_EPISODE)
    else:
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
		
def new_episodes(name, url, thumb):
    count = 0
    link = open_gurl(url)
    all_episodes = regex_get_all(link, '<li class="episodes">', '<span class="item-overlay">')
    for a in all_episodes:
        count = count + 1
        if count < 51:
            thumb = regex_from_to(a, 'img-preview spec-border"  src="', '"')
            url = regex_from_to(a, '<a href="', '"')
            showname = regex_get_all(a,'title="', '"')[1]
            showname = showname.replace('title=','').replace('"','')
            title = regex_from_to(a, 'p class="name">', '</p>').replace('Season ', '').replace(', Episode ', 'x')
            spliturl = url.split('/')
            episode = spliturl[8]
            season = spliturl[6]
            name = title
            if ENABLE_META:
                infoLabels=get_meta(showname,'episode',year=None,season=season,episode=episode)
                if infoLabels['title']=='':
                    name=title
                else:
                    name="%s - %sx%s  %s" % (showname,season,episode,infoLabels['title'])
                if infoLabels['cover_url']=='':
                    iconimage=thumb
                else:
                    iconimage=infoLabels['cover_url']
            else:
                infoLabels =None
                iconimage=thumb
                name = showname + ' - ' + title
            try:
                if AUTOPLAY:
                    addDirPlayable(name, url,2,iconimage, showname,infoLabels=infoLabels)
                else:
                    addDir(name, url,2,iconimage, 'sh', showname,infoLabels=infoLabels)
            except:
                pass
    setView('episodes', 'episodes-view')
    

def search(name):
    keyboard = xbmc.Keyboard('', name, False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            if name == 'Search Movies':
                search_movie(name,query)
            else:
                search_show(name,query)
			
def search_movie(name,query):
    timestamp = int(round(time.time() * 1000))
    url = 'http://www.flixanity.com/ajax/search.php'
    header_dict = {}
    header_dict['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'www.flixanity.com'
    header_dict['Referer'] = 'http://www.flixanity.com/index.php?menu=search&query%s' % query
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0'
    header_dict['Connection'] = 'keep-alive'#
    header_dict['X-Requested-With'] = 'XMLHttpRequest'
    header_dict['Pragma'] = 'no-cache'
    header_dict['Cache-Control'] = 'no-cache'
    form_dict = {}
    form_dict['limit'] = '5'
    form_dict['q'] = query
    form_dict['timestamp'] = str(timestamp)
    form_dict['verifiedCheck'] = ''
    link = net.http_POST(url, form_data=form_dict, headers=header_dict).content.encode("utf-8").replace('\/','/').rstrip()
    match=re.compile('"permalink":"(.+?)","image":"(.+?)","title":"(.+?)","meta":"(.+?)"').findall(link)
    for url,thumb,title,type in match:
        if 'Movie' in type:
            if ENABLE_META:
                infoLabels = get_meta(title,'movie')
                if infoLabels['title']=='':
                    name=title
                else:
                    name=infoLabels['title']
                if infoLabels['cover_url']=='':
                    iconimage=thumb
                else:
                    iconimage=infoLabels['cover_url']
                if infoLabels['year']=='':
                    year=''
                else:
                    year=" (%s)" % infoLabels['year']
            else:
                infoLabels =None
                iconimage=thumb
                year = ''
                name = title
            name = "%s%s" % (name.replace('\u00e0', 'a'), year)
            if AUTOPLAY:
                addDirPlayable(name, url,2,iconimage, 'movies',infoLabels=infoLabels)
            else:
                addDir(name, url,2,iconimage, '','movies',infoLabels=infoLabels)
            setView('movies', 'movies-view')
		
def search_show(name,query):
    timestamp = int(round(time.time() * 1000))
    url = 'http://www.flixanity.com/ajax/search.php'
    header_dict = {}
    header_dict['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'www.flixanity.com'
    header_dict['Referer'] = 'http://www.flixanity.com/index.php?menu=search&query%s' % query
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0'
    header_dict['Connection'] = 'keep-alive'#
    header_dict['X-Requested-With'] = 'XMLHttpRequest'
    header_dict['Pragma'] = 'no-cache'
    header_dict['Cache-Control'] = 'no-cache'
    form_dict = {}
    form_dict['limit'] = '5'
    form_dict['q'] = query
    form_dict['timestamp'] = str(timestamp)
    form_dict['verifiedCheck'] = ''

    link = net.http_POST(url, form_data=form_dict, headers=header_dict).content.encode("utf-8").replace('\t', '').replace('\u00e0', 'a').replace('\/','/').rstrip()
    match=re.compile('"permalink":"(.+?)","image":"(.+?)","title":"(.+?)","meta":"(.+?)"').findall(link)
    for url,thumb,title,type in match:
        if 'TV show' in type:
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
                if infoLabels['year']=='':
                    year=''
                else:
                    year=" (%s)" % infoLabels['year']
            else:
                infoLabels =None
                iconimage=thumb
                name = title
                year = ''
            name = "%s%s" % (name.replace('\u00e0', 'a'), year)
            addDir(name.encode('utf-8'), url,103,iconimage, 'sh',name.encode('utf-8'),infoLabels=infoLabels)
    setView('tvshows', 'tvshows-view')
		
def links(name,url,iconimage,showname):
    if HUBPC:
        if showname == 'movies':
            PC = parentalcontrol.checkrating(name,None,None,'movies')
        else:
            PC = parentalcontrol.checkrating(showname,None,None,'tvshow')
        if PC != 'PC_PLAY':
            return
    urllist = []
    dp = xbmcgui.DialogProgress()
    dp.create("FliXanity",'Searching for links')
    dp.update(0)
    dialog = xbmcgui.Dialog()
    link = open_gurl(url)
    link = link.replace('IFRAME SRC', 'iframe src')
    embeds = regex_from_to(link, 'var embeds', '</script>')
    links = regex_get_all(embeds, ' src="', '"')
    nItem = len(links)
    count = 0
    for l in links:
        count = count + 1
        url = l.replace('http://www.flixanity.com/jwplayer/gkplugins/player.php?', '').replace(' src=','').replace('"','')
        if 'googlevideo' in url:
            title = 'googlevideo'
        else:
            try:
                title = regex_from_to(url, 'http://', '/')
            except:
                try:
                    title = regex_from_to(url, 'https://', '/')
                except:
                    title = url
        title = title.replace('embed.','').replace('api.','').replace('www.','')
        urllist.append(url)
        titlelist = str(count) + ' of ' + str(nItem) + ': ' + title
        progress = len(urllist) / float(nItem) * 100               
        dp.update(int(progress), 'Adding link',title)
        if dp.iscanceled():
            return
        if AUTOPLAY:
            try:
                dp = xbmcgui.DialogProgress()
                dp.create("FliXanity: Trying Links",titlelist)
                play(title,url,iconimage,name)
                return
            except:
                pass
        addDirPlayable(title,url,3,iconimage,name)
			
def stream_links(name,url,iconimage,showname):
    if HUBPC:
        if showname == 'movies':
            PC = parentalcontrol.checkrating(name,None,None,'movies')
        else:
            PC = parentalcontrol.checkrating(showname,None,None,'tvshow')
        if PC != 'PC_PLAY':
            return
    urllist = []
    menu_texts = []
    menu_data = []
    dp = xbmcgui.DialogProgress()
    dp.create("FliXanity",'Searching for links')
    dp.update(0)
    dialog = xbmcgui.Dialog()
    link = open_gurl(url)
    link = link.replace('IFRAME SRC', 'iframe src')
    embeds = regex_from_to(link, 'var embeds', '</script>')
    links = regex_get_all(embeds, ' src="', '"')
    nItem = len(links)
    count = 0
    handle = str(sys.argv[1]) 
    for l in links:
        count = count + 1
        url = l.replace('http://www.flixanity.com/jwplayer/gkplugins/player.php?', '').replace(' src=','').replace('"','')
        if 'googlevideo' in url:
            title = 'googlevideo'
        else:
            try:
                title = regex_from_to(url, 'http://', '/')
            except:
                try:
                    title = regex_from_to(url, 'https://', '/')
                except:
                    title = url
        title = title.replace('embed.','').replace('api.','').replace('www.','')
        menu_texts.append(title)
        menu_data.append(url)
        urllist.append(url)
        titlelist = str(count) + ' of ' + str(nItem) + ': ' + title
        progress = len(urllist) / float(nItem) * 100               
        dp.update(int(progress), 'Adding link',title)
        if dp.iscanceled():
            return
        if AUTOPLAY:
            try:
                dp = xbmcgui.DialogProgress()
                dp.create("FliXanity: Trying Links",titlelist)
                play(title,url,iconimage,name)
                return
            except:
                pass
    menu_id = dialog.select('Select Source', menu_texts)
    if(menu_id < 0):
        return (None, None)
        dialog.close()
    else:	
        url = menu_data[menu_id]
        title = menu_texts[menu_id]
        play(title, url, iconimage, name)

		
def play(name, url, iconimage, showname):
    if 'googlevideo' in url:
        playlink = url
    else:
       playlink = resolve_url(url)
    listitem = xbmcgui.ListItem(showname, iconImage=iconimage, thumbnailImage=iconimage, path=playlink)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    handle = str(sys.argv[1])    
    if handle != "-1":
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer.play(playlink, listitem)
	
def resolve_url(url): 
    if 'docs.google.com' in url:
        link = open_gurl(url)
        stream = regex_from_to(link, 'fmt_stream_map', 'fmt_list')
        playlink = 'https' + regex_from_to(stream,'https', 'https').replace('|','').replace('\u003d', '=').replace('\u0026', '&')
    elif 'vodlocker' in url:
        link = open_gurl(url)
        playlink = regex_from_to(link, 'file: "', '"')
    elif 'played.to' in url:
        header_dict = {}
        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header_dict['Accept-Encoding'] = 'gzip, deflate'
        header_dict['Accept-Language'] = 'en-US,en;q=0.5'
        header_dict['Host'] = 'played.to'
        header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0'
        header_dict['Connection'] = 'keep-alive'
        net.set_cookies(cookie_jar)
        link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
        net.save_cookies(cookie_jar)
        try:
            playlink = regex_from_to(link, 'file: "', '"')
        except:
            form_dict = {}
            form_dict['fname'] = regex_from_to(link, 'name="fname" value="', '"')
            form_dict['hash'] = regex_from_to(link, 'name="hash" value="', '"')
            form_dict['id'] = regex_from_to(link, 'name="id" value="', '"')
            form_dict['imhuman'] = regex_from_to(link, 'name="imhuman" value="', '"')
            form_dict['op'] = regex_from_to(link, 'name="op" value="', '"')
            form_dict['referer'] = ""
            form_dict['usr_login'] = ""
            header_dict = {}
            header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            header_dict['Accept-Encoding'] = 'gzip, deflate'
            header_dict['Accept-Language'] = 'en-US,en;q=0.5'
            header_dict['Host'] = 'played.to'
            header_dict['Referer'] = url
            header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0'
            header_dict['Connection'] = 'keep-alive'
            net.set_cookies(cookie_jar)
            link = net.http_POST(url, form_data=form_dict, headers=header_dict).content.encode("utf-8").rstrip()
            net.save_cookies(cookie_jar)
            playlink = regex_from_to(link, 'file: "', '"')
    elif 'vidto' in url:
        url = 'http://vidto.me/%s.html' % regex_from_to(url, 'embed-', '-')
        header_dict = {}
        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header_dict['Accept-Encoding'] = 'gzip, deflate'
        header_dict['Accept-Language'] = 'en-US,en;q=0.5'
        header_dict['Host'] = 'vidto.me'
        header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0'
        header_dict['Connection'] = 'keep-alive'
        net.set_cookies(cookie_jar)
        link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
        net.save_cookies(cookie_jar)
        try:
            playlink = regex_from_to(link, 'file: "', '"')
        except:
            xbmc.sleep(1000)
            form_dict = {}
            form_dict['fname'] = regex_from_to(link, 'name="fname" value="', '"')
            form_dict['hash'] = regex_from_to(link, 'name="hash" value="', '"')
            form_dict['id'] = regex_from_to(link, 'name="id" value="', '"')
            form_dict['imhuman'] = regex_from_to(link, 'name="imhuman" value="', '"')
            form_dict['op'] = regex_from_to(link, 'name="op" value="', '"')
            form_dict['referer'] = ""
            form_dict['usr_login'] = ""
            header_dict = {}
            header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            header_dict['Accept-Encoding'] = 'gzip, deflate'
            header_dict['Accept-Language'] = 'en-US,en;q=0.5'
            header_dict['Host'] = 'vidto.me'
            header_dict['Referer'] = url
            header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0'
            header_dict['Connection'] = 'keep-alive'
            net.set_cookies(cookie_jar)
            link = net.http_POST(url, form_data=form_dict, headers=header_dict).content.encode("utf-8").replace("'", '"').rstrip()
            
            net.save_cookies(cookie_jar)
            try:
                playlink = regex_from_to(link, 'file: "', '"')#file_link = 
            except:
                playlink = regex_from_to(link, 'file_link = "', '"')
    elif 'ishared' in url:
        link = open_gurl(url).strip().replace('\n', '').replace('\t', '')
        try:
            playlink = regex_from_to(link, 'var zzzz = "', '"')
        except:
            findfile = regex_from_to(link, 'playlist:', 'type')
            key = regex_from_to(findfile, 'file: ', ',')
            playlink = regex_from_to(link, 'var ' + key + ' = "', '"')#
    elif 'allmyvideos' in url:
        link = open_gurl(url).strip().replace('\n', '').replace('\t', '')
        data = regex_from_to(link, 'primary" : "flash"', 'file_id')
        try:
            playlink = regex_from_to(data, 'file" : "', '"')
        except:
            playlink = regex_from_to(data, 'file": "', '"')
    elif 'firrredrive' in url:
        trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
        hosturl = url
        header_dict = {}
        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header_dict['Host'] = 'www.firedrive.com'
        header_dict['Referer'] = str(hosturl)
        net.set_cookies(cookie_jar)
        link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
        net.save_cookies(cookie_jar)
        confirm = regex_from_to(link, 'confirm" value="', '"')
        form_data = ({'confirm': confirm})
        url = url.replace('embed', 'file')
        header_dict['Referer'] = str(url)
        net.set_cookies(cookie_jar)
        link = net.http_POST(url, form_data=form_data,headers=header_dict).content.translate(trans_table).rstrip()
        sources = regex_from_to(link, 'sources:', 'fileref')
        fileurl = regex_from_to(sources, "file: '", "'")
        if 'hd=' in sources:
            playlink = fileurl.replace('stream', 'hd')
        else:
            playlink = fileurl	
    else:
        validresolver = urlresolver.HostedMediaFile(url)
        if validresolver:
            try:
                playlink = urlresolver.resolve(url)
            except:
                pass
    return playlink
	
def view_trailer(name, url, iconimage,showname):
    if ' (' in name:
        name = name.split(' (')[0]
    if HUBPC:
        if showname == 'movies':
            PC = parentalcontrol.checkrating(name,None,None,'movies')
        else:
            PC = parentalcontrol.checkrating(showname,None,None,'tvshow')
        if PC != 'PC_PLAY':
            return
    menu_texts = []
    menu_data = []
    menu_res = []
    menu_list_item = []
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Searching for trailer')
    dialog = xbmcgui.Dialog()
    try:
        url = "http://www.hd-trailers.net/movie/" + name.lower().replace(' ','-').replace(':','-')
        response = open_gurl(url)
        match=re.compile('href="http://(.+?)" rel=(.+?)title="(.+?)">(.+?)</a></td>').findall(response) 
        if len(match)==0:
            url = "http://www.hd-trailers.net/movie/" + name.lower().replace(' ','-').replace(':','-').replace('and','-')
            response = open_gurl(url)
            match=re.compile('href="http://(.+?)" rel=(.+?)title="(.+?)">(.+?)</a></td>').findall(response) 
            if len(match)==0:
                dialog.ok("Trailer Search", 'No trailers found for:', name) 
                return
        for url, info, title, res in match:
            print url
            if url.find('apple')>0:
                url = '%s|User-Agent=QuickTime' % ("http://" + url)
            elif url.find('youtube')>0:
                video_id = url.replace('www.youtube.com/watch?v=','')
                url = (
                    'plugin://plugin.video.youtube/'
                    '?action=play_video&videoid=%s' % video_id
                )
            else:
                url = "http://" + url
            if TRAILER_RESTRICT:
                if url.find('yahoo')<0 and res==TRAILER_QUALITY:
                    menu_texts.append("[%s] %s" % (res, clean_file_name(title, use_blanks=False)))
                    menu_list_item.append(clean_file_name(title, use_blanks=False))
                    menu_data.append(url)
                    menu_res.append(res)
            else:
                if url.find('yahoo')<0:
                    menu_texts.append("[%s] %s" % (res, clean_file_name(title, use_blanks=False)))
                    menu_list_item.append(clean_file_name(title, use_blanks=False))
                    menu_data.append(url)
                    menu_res.append(res)
					
        if TRAILER_ONECLICK:
            menu_id =0
        else:
            menu_id = dialog.select('Select Trailer', menu_texts)
        if(menu_id < 0):
            return (None, None)
            dialog.close()
        else:	
            url = menu_data[menu_id]
            name = menu_texts[menu_id]
            list_item = menu_list_item[menu_id]
			
        pDialog.close()
    
        listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, path=url)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        handle = str(sys.argv[1])    
        if handle != "-1":
            listitem.setProperty("IsPlayable", "true")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        else:
            xbmcPlayer.play(url, listitem)
    except:
        dialog.ok("Trailer Search", 'No trailers found for:', name)
	
def download(name, url, iconimage, dir):
    if 'googlevideo' in url:
        playlink = url
    else:
       playlink = resolve_url(url)
    filename = name + '.mp4'
    WAITING_TIME = 5
    data_path = os.path.join(dir, filename)
    dlThread = DownloadFileThread(name, playlink, data_path, WAITING_TIME)
    dlThread.start()
    wait_dl_only(WAITING_TIME, "Starting Download")
    if os.path.exists(data_path):
        notification('Download started', name, '3000', iconimage)
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
        urllib.urlretrieve(data, path)
        notification('Download finished', name, '5000', iconart)

		
def scan_library():
    if xbmc.getCondVisibility('Library.IsScanningVideo') == False:           
        xbmc.executebuiltin('UpdateLibrary(video)')

def favourites():
    if os.path.isfile(FAV):
        s = read_from_file(FAV)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
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
                    name = title
                addDir(name, url,103,iconimage, 'sh',name,infoLabels=infoLabels)
                setView('episodes', 'episodes-view')
				
def favourite_movies():
    if os.path.isfile(FAV_MOVIE):
        s = read_from_file(FAV_MOVIE)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                url = list1[1]
                thumb = list1[2]
                if ENABLE_META:
                    infoLabels = get_meta(title,'movie')
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
                    name = title
                if AUTOPLAY:
                    addDirPlayable(name, url,2,iconimage, 'movies',infoLabels=infoLabels)
                else:
                    addDir(name, url,2,iconimage, '','movies',infoLabels=infoLabels)
                setView('movies', 'movies-view')

				
				
def subscriptions():
    if os.path.isfile(SUB):
        s = read_from_file(SUB)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
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
                    name = title
                addDir(name, url,103,iconimage, 'sh',name,infoLabels=infoLabels)
                setView('episodes', 'episodes-view')

def add_favourite(name, url, iconimage, dir, text):
    list_data = "%s<>%s<>%s" % (name, url, iconimage)
    add_to_list(list_data, dir)
    notification(text, "[COLOR lime]" + name + "[/COLOR]", '3000', iconimage)
	
def remove_from_favourites(name, url, list_data, dir, text):
    splitdata = list_data.split('<>')
    name = splitdata[0]
    thumb = splitdata[2]
    remove_from_list(list_data, dir)
    notification(name, "[COLOR orange]" + text + "[/COLOR]", '5000', thumb)

def add_to_library(name, url, iconimage):
    create_strm_file(name, url, "21", MOVIE_PATH, iconimage, name)
    notification(name.upper(), "[COLOR lime]Added to Library[/COLOR]", '3000', iconimage)
    if xbmc.getCondVisibility('Library.IsScanningVideo') == False:           
        xbmc.executebuiltin('UpdateLibrary(video)')
	
def create_tv_show_strm_files(name, url, iconimage, ntf):
    if ' (' in name:
        name = name[:name.find(' (')]
    showurl = url
    showname=name
    dialog = xbmcgui.Dialog()
    list_data = "%s<>%s<>%s" % (name,url,iconimage)
    tv_show_path = create_directory(TV_PATH, name)
    link = open_gurl(url)
    all_episodes = regex_get_all(link, '<li class="episodes">', '<span class="item-overlay">')
    data = regex_from_to(link, 'id="season-list"', '</ul>')
    match = re.compile("<a href='(.+?)'>(.+?)</a>").findall(data)
    for url,season in match:
        seasonnum = season.replace("Season ", "")
        season_path = create_directory(tv_show_path, str(seasonnum))
        for a in all_episodes:
            titleurl = regex_from_to(a, '<a class="link"', '</a>')
            url = regex_from_to(titleurl, 'href="', '"')
            spliturl = url.split('/')
            episode = spliturl[8]
            season = spliturl[6]
            display = "%s %sx%s" % (showname, season, episode)
            if season == seasonnum:
                create_strm_file(display, url, "21", season_path, iconimage, showname)
    if ntf == "true" and ENABLE_SUBS:
        if dialog.yesno("Subscribe?", 'Do you want FliXanity to automatically add new', '[COLOR gold]' + showname + '[/COLOR]' + ' episodes when available?'):
            add_favourite(showname, showurl, iconimage, SUB, "Added to Library/Subscribed")
        else:
            notification(showname, "[COLOR lime]Added to Library[/COLOR]", '3000', iconimage)
    else:
        if ntf != 'serv':
            notification(showname, "[COLOR lime]Added to Library[/COLOR]", '3000', iconimage)
    if xbmc.getCondVisibility('Library.IsScanningVideo') == False:           
        xbmc.executebuiltin('UpdateLibrary(video)')

def remove_tv_show_strm_files(name, url, iconimage, dir_path):
    dialog = xbmcgui.Dialog()
    splitname = iconimage.split('<>')
    rname = splitname[0]
    try:
        path = os.path.join(dir_path, str(rname))
        shutil.rmtree(path)
        remove_from_favourites(name, url, iconimage, SUB, "Removed from Library/Unsubscribed")
        if xbmc.getCondVisibility('Library.IsScanningVideo') == False:
            if dialog.yesno("Clean Library?", '', 'Do you want clean the library now?'):		
                xbmc.executebuiltin('CleanLibrary(video)')		
    except:
        xbmc.log("[FliXanity] Unable to remove TV show: %s" % (name)) 
		
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
                    list1 = list.split('<>')
                    title = list1[0]
                    url = list1[1]
                    thumb = list1[2]
                    create_tv_show_strm_files(title, url, list, "serv")
    except:
        xbmc.log("[MovieStorm] Failed to fetch subscription")
		
def clear_cache():
    cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.flixanity/cache'), '')
		
    for root, dirs, files in os.walk(cache_path):
        for f in files:
            age = get_file_age(os.path.join(root, f))
            if age > 3600:
    	        os.unlink(os.path.join(root, f))

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
        #xbmc.executebuiltin("Container.Refresh")
		
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
    if 'movie' in types:
        meta = metainfo.get_meta('movie',clean_file_name(name, use_blanks=False),year)
        infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Aired': meta['premiered'],'year': meta['year']}
    else:
        if 'tvshow' in types:
            meta = metainfo.get_meta('tvshow',clean_file_name(name, use_blanks=False),'','','')
            infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Episode': meta['episode'],'Aired': meta['premiered'],'Playcount': meta['playcount'],'Overlay': meta['overlay'],'year': meta['year']}
            #infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Episode': meta['episode'],'Aired': meta['premiered'],'Playcount': meta['playcount'],'Overlay': meta['overlay']}
        elif 'episode' in types:
            meta = metainfo.get_episode_meta(clean_file_name(name, use_blanks=False), '', season, episode)
            infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Episode': meta['episode'],'Aired': meta['premiered'],'Playcount': meta['playcount'],'Overlay': meta['overlay']}
        elif 'season' in types:
            meta = metainfo.get_episode_meta(clean_file_name(name, use_blanks=False), '', season,None)
            infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Episode': meta['episode'],'Aired': meta['premiered'],'Playcount': meta['playcount'],'Overlay': meta['overlay']}
    #infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Aired': meta['premiered']}

        
    return infoLabels
		
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


def addDir(name,url,mode,iconimage,list,showname,infoLabels=None):
        suffix = ""
        suffix2 = ""
        list1 = "%s<>%s<>%s" % (name.lower(),url,iconimage)
        list2 = "%s<>%s<>%s" % (name,url,iconimage)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&list="+str(list)+"&showname="+urllib.quote_plus(showname)
        ok=True
        contextMenuItems = []
        if showname == "movies":
            contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
            contextMenuItems.append(("[COLOR cyan]View Trailer[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=27&iconimage=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(url), urllib.quote(iconimage))))
            contextMenuItems.append(("[COLOR lime]Add to XBMC Library[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=20&iconimage=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(url), urllib.quote(iconimage))))
            if find_list(list1, FAV_MOVIE) < 0:
                suffix = ""
                contextMenuItems.append(("[COLOR lime]Add to Favourite Movies[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=10&iconimage=%s)'%(sys.argv[0], urllib.quote(name), url, urllib.quote(iconimage))))
            else:
                suffix = ' [COLOR lime]+[/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from Favourite Movies[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=9&iconimage=%s)'%(sys.argv[0], urllib.quote(name), url, str(list1))))
        if name == "TV Subscriptions":
            contextMenuItems.append(("[COLOR cyan]Refresh Subscriptions[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=17&iconimage=%s)'%(sys.argv[0], urllib.quote(name), url, urllib.quote(iconimage))))
        if list == "sh":
            contextMenuItems.append(('TV Show Information', 'XBMC.Action(Info)'))
            if find_list(list1, FAV) < 0:
                suffix = ""
                contextMenuItems.append(("[COLOR lime]Add to Favourite TV Shows[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=11&iconimage=%s)'%(sys.argv[0], urllib.quote(name), url, urllib.quote(iconimage))))
            else:
                suffix = ' [COLOR lime]+[/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from Favourite TV Shows[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=13&iconimage=%s)'%(sys.argv[0], urllib.quote(name), url, str(list1))))
            if find_list(list2, SUB) < 0:
                suffix2 = ""
                contextMenuItems.append(("[COLOR lime]Add to XBMC Library/Subscribe[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=14&iconimage=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(url), urllib.quote(iconimage))))
            else:
                suffix2 = ' [COLOR cyan][s][/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from XBMC Library[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=15&iconimage=%s)'%(sys.argv[0], urllib.quote(name), url, str(list2))))
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
        list1 = "%s<>%s<>%s" % (name.lower(),url,iconimage)
        list2 = "%s<>%s<>%s" % (name,url,iconimage)
        ok=True
        contextMenuItems = []
        contextMenuItems.append(("[COLOR lime]Download[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=25&iconimage=%s)'%(sys.argv[0], urllib.quote(showname), urllib.quote(url), urllib.quote(iconimage))))
        if showname == "movies":
            contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
            contextMenuItems.append(("[COLOR cyan]View Trailer[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=27&iconimage=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(url), urllib.quote(iconimage))))
            contextMenuItems.append(("[COLOR lime]Add to XBMC Library[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=20&iconimage=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(url), urllib.quote(iconimage))))
            if find_list(list1, FAV_MOVIE) < 0:
                suffix = ""
                contextMenuItems.append(("[COLOR lime]Add to Favourite Movies[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=10&iconimage=%s)'%(sys.argv[0], urllib.quote(name), url, urllib.quote(iconimage))))
            else:
                suffix = ' [COLOR lime]+[/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from Favourite Movies[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=9&iconimage=%s)'%(sys.argv[0], urllib.quote(name), url, str(list1))))
        if showname == "sh":
            contextMenuItems.append(('TV Show Information', 'XBMC.Action(Info)'))
            if find_list(list1, FAV) < 0:
                suffix = ""
                contextMenuItems.append(("[COLOR lime]Add to Favourite TV Shows[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=11&iconimage=%s)'%(sys.argv[0], urllib.quote(name), url, urllib.quote(iconimage))))
            else:
                suffix = ' [COLOR lime]+[/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from Favourite TV Shows[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=13&iconimage=%s)'%(sys.argv[0], urllib.quote(name), url, str(list1))))
            if find_list(list2, SUB) < 0:
                suffix2 = ""
                contextMenuItems.append(("[COLOR lime]Add to XBMC Library/Subscribe[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=14&iconimage=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(url), urllib.quote(iconimage))))
            else:
                suffix2 = ' [COLOR cyan][s][/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from XBMC Library[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=15&iconimage=%s)'%(sys.argv[0], urllib.quote(name), url, str(list2))))
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels=infoLabels)
        try:
            liz.setProperty( "fanart_image", infoLabels['fanart'] )
        except:
            liz.setProperty('fanart_image', fanart )
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
              
params=get_params()

url=None
name=None
mode=None
iconimage=None
showname=None



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


if mode==None or url==None or len(url)<1:
        CATEGORIES(name)

elif mode == 101:
        movie_menu()
		
elif mode == 102:
        tvseries_menu()
		
elif mode == 103:
        tvseries_seasons(name,url,iconimage,list)
		
elif mode==104:
        tvseries_episodes(name, url, iconimage, list)
		
elif mode == 7:
        tvshow_genre_menu(url)
		
elif mode == 8:
        tvshow_genre_menu(url)
		
elif mode == 106:
        genres(url)
		
elif mode == 107:
        all_series(url)
		
elif mode == 108:
        a_to_z(url)
		
elif mode == 109:
        tvschedule(url)
		
elif mode==29:
        Main_sort(name,url,list,showname)  
		
elif mode==1:
        Main(name,url,list,showname)        
       
elif mode==2:
        links(name,url,iconimage,showname)
		
elif mode==3:
        play(name, url, iconimage, showname)

elif mode==4:
        movie_genre_menu(url)
		
elif mode==6:
        search(name)
		
#elif mode==4:
        #tv_show_episodes(name, url, iconimage, list,description)
		
elif mode==5:
        new_episodes(name, url, iconimage)
		
		
elif mode == 10:
        add_favourite(name, url, iconimage, FAV_MOVIE, "Added to Favourites")
		
elif mode == 9:
        remove_from_favourites(name, url, iconimage, FAV_MOVIE, "Removed from Favourites")
		
elif mode == 11:
        add_favourite(name, url, iconimage, FAV, "Added to Favourites")
		
elif mode == 12:
        favourites()
		
elif mode == 19:
        favourite_movies()
		
elif mode == 13:
        remove_from_favourites(name, url, iconimage, FAV, "Removed from Favourites")
		
elif mode == 14:
        create_tv_show_strm_files(name, url, iconimage, "true")
		
elif mode == 15:
        remove_tv_show_strm_files(name, url, iconimage, TV_PATH)
		
elif mode == 16:
        subscriptions()
		
elif mode == 17:
        get_subscriptions()
		
elif mode == 18:
        request_video()
		
elif mode == 20:
        add_to_library(name, url, iconimage)
		
elif mode==21:
        stream_links(name,url,iconimage,list)
		
elif mode == 25:
        if name[1:2] == 'x' and (name[3:4] == ' ' or name[4:5] == ' '):
            download(name, url, iconimage, TV_PATH)
        else:
            download(name, url, iconimage, MOVIE_PATH)
		
elif mode == 26:
        clear_cache()
		
elif mode == 27:
        view_trailer(name, url, iconimage, 'movies')
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))



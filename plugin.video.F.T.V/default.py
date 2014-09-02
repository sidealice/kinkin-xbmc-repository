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
import plugintools
from t0mm0.common.net import Net
net = Net()


ADDON = settings.addon()
FILMON_KEEP = settings.keep_session_flag()
FILMON_ACCOUNT = settings.filmon_account()
FILMON_USER = settings.filmon_user()
FILMON_QUALITY = settings.filmon_quality()
AUTO_SWITCH = settings.auto_switch()
STRM_TYPE = settings.stream_type()
FILMON_PASS = md5(settings.filmon_pass()).hexdigest()
FILMON_PASSWORD = settings.filmon_pass()
MY_VIDEOS = settings.my_videos()
MY_AUDIO = settings.my_audio()
OTHER_MENU = settings.other_menu()
HIDDEN_FILE = settings.hidden_file()
FAV_CHAN = settings.favourite_channels()
FAV_MOV = settings.favourite_movies()
SORT_ALPHA = settings.sort_alpha()
DOWNLOAD_PATH = settings.download_path()
MOVIE_DIR = settings.movie_directory()
cookie_jar = settings.cookie_jar()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'fanart.jpg'))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'icon.png'))
channel_list = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V/helpers', 'channel.list'))
cartoonlinks = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V/helpers', 'cartoonlinks.list'))
group_list = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V/helpers', 'groups.list'))
xml_list = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V/helpers', 'FilmOn.xml'))
ct_list = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V/helpers', 'cartoons.list'))
base_url = 'http://www.filmon.com/'
disneyjrurl = 'http://www.disney.co.uk/disney-junior/content/video.jsp?b='
session_url = 'http://www.filmon.com/api/init/'



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
    header_dict['Host'] = 'www.filmon.com'
    header_dict['Referer'] = 'http://www.filmon.com/'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>)'# AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>
    header_dict['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    header_dict['X-Requested-With'] = 'XMLHttpRequest'
    net.set_cookies(cookie_jar)
    req = net.http_POST(url, form_data=form_data, headers=header_dict)
    return req.content

def login():
    if FILMON_ACCOUNT:
        header_dict = {}
        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        header_dict['Host'] = 'www.filmon.com'
        header_dict['Referer'] = 'http://www.filmon.com/'
        header_dict['User-Agent'] = 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>'
        header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
        header_dict['Connection'] = 'keep-alive'
        form_data = ({'login': FILMON_USER, 'password': FILMON_PASSWORD,'remember': '1'})	
        net.set_cookies(cookie_jar)
        login = net.http_POST('http://www.filmon.com/user/login', form_data=form_data, headers=header_dict)
        net.save_cookies(cookie_jar)
        keep_alive()


def keep_alive():
    url = "http://www.filmon.com/api/keep-alive?session_key=%s" % session_key
    #url = "http://www.filmon.com/ajax/keepAlive"
    net.set_cookies(cookie_jar)
    net.http_GET(url)
    net.save_cookies(cookie_jar)
    tloop = Timer(60.0, keep_alive)
    tloop.start()
	
def CATEGORIES():
    hidden_links = read_from_file(HIDDEN_FILE)
    login()
    if MY_VIDEOS:
        addDir('My Video Addons','url',141,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'video_addons.jpg')), '', '')
    if MY_AUDIO:
        addDir('My Audio Addons','url',145,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'audio_addons.jpg')), '', '')
    addDir('Non Geo','url',110,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'xml.png')), '', '')
    addDir('Cartoons & More','url',399,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'disney_junior.jpg')), '', '')
    addDir('FilmOn Demand ','url',199,'http://www.filmon.com/tv/themes/filmontv/img/mobile/filmon-logo-stb.png', '', '')
    addDir('My Channels','url',122,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'my_channels.jpg')), '', '')
    addDir('My Recordings','url',131,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'f_record.jpg')), '', '')
    addDir('Favourite Channels','url',415,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'my_channels.jpg')), '', '')
    addDir('Favourite Movies','url',415,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'my_channels.jpg')), '', '')
    net.set_cookies(cookie_jar)
    url = 'http://www.filmon.com/groups'
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    if "UK LIVE TV" not in link:
        if not "UK LIVE TV" in hidden_links:
            addDir("UK LIVE TV",'url',123,'http://static.filmon.com/couch/groups/5/big_logo.png', '','')
    all_groups = regex_get_all(link, '<li class="group-item">', '</li>')
    for groups in all_groups:
        group_id = regex_from_to(groups, 'http://static.filmon.com/couch/groups/','/big_logo.png')
        title = regex_from_to(groups, 'title="', '"').replace('&amp;', '&')
        thumb = 'http://static.filmon.com/couch/groups/%s/big_logo.png'	% group_id
        url = base_url + regex_from_to(groups, '<a href="/', '">')
        if not title in hidden_links:
            addDir(title,url,123,thumb, '','')
    setView('episodes', 'episodes-view')
    if FILMON_USER in link and FILMON_ACCOUNT:
        notification('Logged in at Filmon', FILMON_USER, '5000', iconart)

		
def group_channels(url, title):
    url = str(url)
    gt = str(title)
    name_lst = []
    if url != 'url':
        net.set_cookies(cookie_jar)
        link = net.http_GET(url).content.encode("utf-8").rstrip()

        channels = regex_get_all(link, '<li class="channel', '</li>')
        for channel in channels:
            alias = regex_from_to(channel, 'alias="', '" channel_id')
            channel_id = regex_from_to(channel, 'id="', '" alias')
            title = regex_from_to(channel, 'channel_title">', '</')
            name_lst.append(title)
            try:
                description = clean_file_name(regex_from_to(channel, '<p>', '</p>'), use_blanks=False)
            except:
                description = ""
            thumb = 'http://static.filmon.com/couch/channels/%s/extra_big_logo.png' % str(channel_id)
            url = base_url + regex_from_to(channel, 'href="/', '" class')
            addDirPlayable(title,url,125,thumb,channel_id,description, alias, "grp")
    # read from channel list

    s = read_from_file(channel_list)
    search_list = s.split('\n')
    for list in search_list:
        if list != '':
            list1 = list.split('<>')
            st_grp = list1[0]
            st_name = list1[1]
            st_id = list1[2]
            st_url = list1[3]
            par = "%s<>%s" % (st_id, st_url)
            thumb = 'http://static.filmon.com/couch/channels/%s/extra_big_logo.png' % str(st_id).rstrip()
            if st_grp == gt  and st_name not in name_lst:#
                addDirPlayable(st_name,gt,125,thumb,par,"", "", "lst")

    if gt == 'UK LIVE TV':
        addDirPlayable('Chelsea TV','http://www.watchfeed.co/watch/44-1/chelsea-tv.html',15,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'chelsea.jpg')), '', '', '', "")
    setView('episodes', 'episodes-view')
    if SORT_ALPHA:    
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
		
def favourites():
    url = base_url + 'my/favorites'
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    channels = regex_get_all(link, '<a class="left"', '/a>')
    for c in channels:
        ch_url = regex_from_to(c, 'href="/', '">')
        ch_id = ch_url.split('/')
        ch_id = ch_id[1]
        url = base_url + ch_url
        title = regex_from_to(c, '>', '<').encode("utf-8")
        thumb = 'http://static.filmon.com/couch/channels/%s/extra_big_logo.png' % str(ch_id)
        addDirPlayable(title,url,125,thumb,str(ch_id),"", title, "fav")
        setView('episodes', 'episodes-view')
 
		
def add_fav(name, ch_id, iconimage):
    url = base_url + 'ajax/toggleFavorite'
    form_data = ({'channel': ch_id})
    req = POST_URL(url, form_data)
    text = req.replace('"','').replace('{','').replace('}','').replace(","," - ")
    if "enable" in text and "true" in text:
        notification('Toggle My Channels', name + ' added', '5000', iconart)
    if "disable" in text and "true" in text:
        notification('Toggle My Channels', name.upper() + ' removed', '5000', iconart)
        xbmc.executebuiltin("Container.Refresh")	


def tv_guide(name, url, iconimage):
    url = base_url + 'tvguide/' + name
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    alias = regex_from_to(link, '"alias":"', '"')
    tvg_list = regex_from_to(link, 'var channelJson', 'title":"HD - Year"')
    programmes = regex_get_all(tvg_list, '{"programme"', 'vendor_id')
    utc_now = datetime.datetime.now()
    for p in programmes:
        p_id = regex_from_to(p, 'programme":"', '"')
        try:
            try:
                start = regex_from_to(p, 'startdatetime":"', '"')
            except:
                start = regex_from_to(p, 'startdatetime":', ',"')
            start_time = datetime.datetime.fromtimestamp(int(start))
            end_time = datetime.datetime.fromtimestamp(int(regex_from_to(p, 'enddatetime":"', '"')))
        except:
            start_time = datetime.datetime.fromtimestamp(int(regex_from_to(p, 'startdatetime":', ',')))
            end_time = datetime.datetime.fromtimestamp(int(regex_from_to(p, 'enddatetime":', ',')))
        description = regex_from_to(p, 'programme_description":"', '"')
        p_name = regex_from_to(p, 'programme_name":"', '"')
        allow_dvr = regex_from_to(p, 'allow_dvr":', ',')
        channel_id = regex_from_to(p, 'channel_id":"', '",')
        title = "%s - %s" % (start_time.strftime('%d %b %H:%M'),p_name)
        try:
            matchthumb = regex_from_to(p, 'type":"2"', 'cop')
            thumb = regex_from_to(matchthumb, 'url":"', '"').replace("\/", "/")
        except:
            thumb = iconimage
        if end_time > utc_now:
            if start_time < utc_now and end_time > utc_now:
                url = base_url + 'channel/' + alias
                addDirPlayable('[COLOR cyan]' + title + '[/COLOR]',url,125,thumb,channel_id,description, start, "gd")
            else:
                if allow_dvr == "true":
                    addDirPlayable(title,channel_id,129,thumb,p_id,description, start, "gd")
                else:
                    addDirPlayable(title + "  [COLOR red](not recordable)[/COLOR]",channel_id,"",thumb,p_id,description, start, "gd")
            setView('episodes', 'epg')

		
def play_filmon(name,url,iconimage,ch_id):
    grpurl = url
    if url == "LOCAL TV" or url == "UK LIVE TV":
        parsplit = ch_id.split('<>')
        swap_ch = parsplit[0]
        swap_url = parsplit[1]
    else:
        swap_ch = ch_id


    if url == "LOCAL TV":
        url = 'http://www.filmon.com/channel/filmon-studio'
        ch_id = '1676'
    if url == "UK LIVE TV":
        url = 'http://www.filmon.com/channel/channel-5'
        ch_id = '22'

    pp = url.replace('/channel/', '/tv/')
    net.set_cookies(cookie_jar)
    streamerlink = net.http_GET(url).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    swfplay = 'http://www.filmon.com' + regex_from_to(streamerlink, '"streamer":"', '",').replace("\/", "/")

    name = name.replace('[COLOR cyan]','').replace('[/COLOR]','')
    dp = xbmcgui.DialogProgress()
    dp.create('Opening ' + name.upper())
    utc_now = datetime.datetime.now()
    channel_name=name
    cl= 23 + len(ch_id)
    net.set_cookies(cookie_jar)
    header_dict = {}
    header_dict['Accept'] = '*/*'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Accept-Language'] = 'en-US,en;q=0.5'
    header_dict['Host'] = 'www.filmon.com'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Referer'] = 'http://www.filmon.com/tvguide'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0'
    header_dict['X-Requested-With'] = 'XMLHttpRequest'
    if FILMON_QUALITY == '480p':
        quality = 'high'
    else:
        quality = 'low'
    churl = 'http://www.filmon.com/ajax/getChannelInfo?channel_id=%s&quality=%s&flash-player-type=rtmp' % (ch_id, quality)
    link = net.http_GET(churl, headers=header_dict).content
    net.save_cookies(cookie_jar)
    link = json.loads(link)
    link = str(link)

    next_p = regex_from_to(link, "next_playing'", "u'title")
    try:
        n_start_time = datetime.datetime.fromtimestamp(int(regex_from_to(next_p, "startdatetime': u'", "',")))
        n_end_time = datetime.datetime.fromtimestamp(int(regex_from_to(next_p, "enddatetime': u'", "',")))
        n_programme_name = regex_from_to(next_p, "programme_name': u'", "',")
        n_start_t = n_start_time.strftime('%H:%M')
        n_end_t = n_end_time.strftime('%H:%M')
        n_p_name = "[COLOR cyan]Next: %s (%s-%s)[/COLOR]" % (n_programme_name, n_start_t, n_end_t)
    except:
        n_p_name = ""
		
    now_p = regex_from_to(link, "now_playing':", "u'tvguide")
    try:
        start_time = datetime.datetime.fromtimestamp(int(regex_from_to(now_p, "startdatetime': u'", "',")))
        end_time = datetime.datetime.fromtimestamp(int(regex_from_to(now_p, "enddatetime': u'", "',")))
        programme_name = regex_from_to(now_p, "programme_name': u'", "',")
        description = ""
        start_t = start_time.strftime('%H:%M')
        end_t = end_time.strftime('%H:%M')
        p_name = "%s (%s-%s)" % (programme_name, start_t, end_t)
        dp.update(50, p_name)
    except:
        try:
            p_name = programme_name
        except:
            p_name = name
    try:
        timeout = regex_from_to(link, "u'watch-timeout': u'", "',")
    except:
        timeout = '86500'
    timeout = int(timeout)
	
    if FILMON_QUALITY == '480p' and (AUTO_SWITCH == False or timeout > 1800):
        urlhls = regex_from_to(link, "name': u'HD', u'url': u'", "',")
    else:
        urlhls = regex_from_to(link, "name': u'SD', u'url': u'", "',")
		
    url2 = urlhls.split('/')
    urlrtmp = "rtmp://%s/live/%s" % (url2[2],url2[5].replace('playlist.m3u8',''))
    name = url2[4]
    url3 = url2[2]
    
    name = name.replace('.l.stream', '.low.stream').replace('.lo.stream', '.low.stream')
    if grpurl == "UK LIVE TV":
        name = name.replace('22', swap_ch)
        urlrtmp = urlrtmp.replace(url3, swap_url)
    if grpurl == "LOCAL TV":
        name = name.replace('1676', swap_ch)
        urlrtmp = urlrtmp.replace(url3, swap_url)
    
    if name.endswith('m4v'):
        app = 'vodlast'
    else:
        appfind = url[7:].split('/')
        app = 'live/' + appfind[2]

    if STRM_TYPE == 'RTMP':		
        if url.endswith('/'):
            STurl = str(urlrtmp) + ' playpath=' + name + ' swfUrl=' + swfplay + ' pageUrl=' + pp + ' live=true timeout=45 swfVfy=true'
        else:
            STurl = str(urlrtmp) + '/' + name + ' playpath=' + name + ' swfUrl=' + swfplay + ' pageUrl=' + pp + ' live=true timeout=45 swfVfy=true'
    else:
        STurl = urlhls
		
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    handle = str(sys.argv[1])
    try:
        if ch_id == '857' or 'http' not in grpurl:
            listitem = xbmcgui.ListItem(channel_name, iconImage=iconimage, thumbnailImage=iconimage, path=STurl)
        else:
            listitem = xbmcgui.ListItem(p_name + ' ' + n_p_name, iconImage=iconimage, thumbnailImage=iconimage, path=STurl)
        if handle != "-1":	
            listitem.setProperty("IsPlayable", "true")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        else:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(STurl,listitem)
    except:
        listitem = xbmcgui.ListItem(channel_name, iconImage=iconimage, thumbnailImage=iconimage, path=STurl)
        if handle != "-1":
            listitem.setProperty("IsPlayable", "true")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        else:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(STurl,listitem)
    dp.close()
    keep_alive()
	
def non_geo():
    url = 'http://www.filmon.com/channel/filmon-studio'
    ch_id = '1676'

    pp = url.replace('/channel/', '/tv/')
    streamerlink = net.http_GET(url).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    swfplay = 'http://www.filmon.com' + regex_from_to(streamerlink, '"streamer":"', '",').replace("\/", "/")

    cl= '27'
    net.set_cookies(cookie_jar)
    header_dict = {}
    header_dict['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Accept-Language'] = 'en-US,en;q=0.5'
    header_dict['Content-Length'] = str(cl)
    header_dict['Host'] = 'www.filmon.com'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Pragma'] = '	no-cache'
    header_dict['Referer'] = 'http://www.filmon.com/'
    header_dict['User-Agent'] = 'AppleWebKit/<WebKit Rev>'
    header_dict['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    header_dict['X-Requested-With'] = 'XMLHttpRequest'
    form_data = ({'channel_id': ch_id, 'quality': 'low'})
    churl = 'http://www.filmon.com/ajax/getChannelInfo'
    link = net.http_POST(churl, form_data=form_data, headers=header_dict).content
    link = json.loads(link)
    link = str(link)
    url_ch5 = regex_from_to(link, "serverURL': u'", "',")
    urls_ch5 = url_ch5.split('/')
    url2_ch5 = urls_ch5[2]
    url4_ch5 = urls_ch5[4]
    url4 = url4_ch5
    url4_ch5 = url4_ch5.replace('id=', '')
    name_ch5 = regex_from_to(link, "streamName': u'", "',")
    name_ch5 = name_ch5.replace('.l.stream', '.low.stream').replace('.lo.stream', '.low.stream')

    try:
        timeout = regex_from_to(link, "expire_timeout': u'", "',")
    except:
        timeout = '86500'
    if FILMON_QUALITY == "480p":
        name_ch5 = name_ch5.replace('low', 'high')
    if name_ch5.endswith('m4v'):
        app = 'vodlast'
    else:
        appfind = url[7:].split('/')
        app = 'live/' + appfind[2]
	
    list = read_from_file(xml_list)
    all_streams = regex_get_all(list, '<stream>', '</stream>')
    for s in all_streams:
        title = regex_from_to(s, '<title>', '</title>').replace(' [Borg TV Update]', '')
        swfUrl = regex_from_to(s, '<swfUrl>', '</swfUrl>')
        link = regex_from_to(s, '<link>', '</link>').replace('"', '').replace(':1935/', '').replace('rtmp://', '').replace('/live/', '')
        linkedge = regex_from_to(s, '<link>', '</link>').replace('"', '').replace(':1935/', '')
        linkcdn = regex_from_to(s, '<link>', '</link>').replace('"', '').replace(':1935', '')
        pageUrl = regex_from_to(s, '<pageUrl>', '</pageUrl>')
        playpath = regex_from_to(s, '<playpath>', '</playpath>')
        advanced = regex_from_to(s, '<advanced>', '</advanced>').replace('-a ', '').replace(' -o- -b 96000000', '')

        ppsplit = playpath.split('.')
        ch_id = ppsplit[0]
        thumb = 'http://static.filmon.com/couch/channels/%s/extra_big_logo.png' % str(ch_id)#+ '.mp4' + advpp
        name = name_ch5.replace('1676', ch_id)
        url = url_ch5.replace(url2_ch5, link)

        if "World Cup" in title:
            STurl = 'rtmp://' + link + advanced +' playpath=' + playpath + ' swfUrl=' + swfUrl + ' pageUrl=' + pageUrl + ' live=1 timeout=10 swfVfy=1'#
        elif url.endswith('/'):
            STurl = str(url) + ' playpath=' + name + ' app=' + app + ' swfUrl=' + swfplay + ' pageUrl=' + pp + ' live=1 timeout=10 swfVfy=1'
        else:
            STurl = str(url) + '/' + name + ' playpath=' + name + ' swfUrl=' + swfplay + ' pageUrl=' + pp + ' live=1 timeout=10 swfVfy=1'

        addDirPlayable(title,str(STurl),111,thumb,str(ch_id),link, title, "ng")
		
def add_ng(title,ch_id,link):
    grp_texts = []
    dialog = xbmcgui.Dialog()
    s = read_from_file(group_list)
    grp_list = s.split('\n')
    for grp in grp_list:
        grp_texts.append(grp)
		
    menu_id = dialog.select('Select Group', grp_texts)
    if(menu_id < 0):
        return (None, None)
        dialog.close()
    else:	
        grpname = grp_texts[menu_id]
        list_data = "%s<>%s<>%s<>%s" % (grpname, title, ch_id, link)
        add_to_list(list_data, channel_list)
        notification(title + ' added to:', grpname, '5000', iconart)

def play_ng(name,url,iconimage):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    handle = str(sys.argv[1])
    listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, path=url)    
    if handle != "-1":	
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(url,listitem)	

def record_programme(name,ch_id,p_id,start):
    dialog = xbmcgui.Dialog()
    url = base_url + 'dvr/add'
    form_data = ({'channel_id': ch_id, 'programme_id': p_id,'start_time': start})	
    
    if dialog.yesno("Record Programme?", '', name.upper()):
        req = POST_URL(url, form_data)
        text = regex_from_to(req, 'reason":"', '"}').replace('"',' ')
        notification('Record Programme', name.upper() + ' ' + text.upper(), '5000', iconart)
		
def delete_recording(name,start,iconimage):
    dialog = xbmcgui.Dialog()
    url = base_url + 'dvr/remove'
    form_data = ({'record_id': start})	
    
    if dialog.yesno("Delete Recording?", '', name.upper()):
        req = POST_URL(url, form_data)
        text = regex_from_to(req, 'reason":"', '"}').replace('"',' ')
        notification('Delete Recording', name.upper() + ' ' + text.upper(), '5000', iconart)
        xbmc.executebuiltin("Container.Refresh")

	
def recordings(url):
    url = base_url + 'my/recordings'
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    t = regex_from_to(link, '<span class="total" >', '</span>')
    r = regex_from_to(link, 'span class="recordedTime recorded">', '</span>')
    a = regex_from_to(link, '<span class="leftTime available">', '</span>')
    acc_status = "Allowed: %shrs - Recorded: %shrs - Available %shrs" % (t, r, a)
    addLink('[COLOR cyan]'+acc_status+'[/COLOR]',"","","","","", "", "", "")
    recordings = regex_get_all(link, '"id"', 'is_deleted"')
    for r in recordings:
        STname = regex_from_to(r, 'stream_name":"', '",').replace("\/", "/")
        
        p_id = regex_from_to(r, 'id":"', '",')
        p_name = regex_from_to(r, 'title":"', '",')
        description = regex_from_to(r, 'description":"', '",')
        channel_id = regex_from_to(r, 'channel_id":"', '",')
        logo = 'https://static.filmon.com/couch/channels/%s/extra_big_logo.png' % str(channel_id)
        start = regex_from_to(r, 'time_start":"', '",')
        start_time = datetime.datetime.fromtimestamp(int(regex_from_to(r, 'time_start":"', '",')))
        duration = regex_from_to(r, 'duration":"', '",')
        status = regex_from_to(r, 'status":"', '",')
        try:
            download_link = regex_from_to(r, 'download_link":"', '"').replace("\/", "/")#'http://s2.dvr.gv.filmon.com/' + STname
        except:
            download_link = "error"
        STurl = regex_from_to(r, 'stream_url":"', '",').replace("\/", "/") + " playpath=" + "mp4:" + STname + " swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf pageUrl=http://www.filmon.com/my/recordings"
        text = "[COLOR gold]%s[/COLOR] %s (%s)" % (p_name, start_time.strftime('%d %b %H:%M'), status)
        addLink(text,download_link,logo,description,status,download_link, p_id, start,p_name)
        setView('episodes', 'episodes-view')

def download_rec(name, url, iconimage):
    WAITING_TIME = 5
    directory=DOWNLOAD_PATH
    filename = "%s.%s" % (name, url[len(url)-3:])
    data_path = os.path.join(directory, filename)
    dlThread = DownloadThread(name, url, data_path)
    if directory == "notset" or directory == "":
        xbmcgui.Dialog().ok('Download directory not set', 'Set your download path in settings first')
        ADDON.openSettings()
    else:
        dlThread.start()
        wait_dl_only(WAITING_TIME, "Starting Download")
        if os.path.exists(data_path):
            notification('F.T.V - Download started', name.upper(), '5000', iconart)
        else:
            notification('F.T.V - Download failed', name.upper(), '5000', iconart)
       

class DownloadThread(Thread):
    def __init__(self, name, url, data_path):
        self.data = url
        self.path = data_path
        Thread.__init__(self)

    def run(self):
        path = str(self.path)
        data = self.data
        urllib.urlretrieve(data, path)
        notification('F.T.V - Download finished', name.upper(), '5000', iconart)
        xbmc.executebuiltin(notify)	
		
def on_demand()	:
    url = "http://www.filmon.com/vod/documentary"
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)#id,vid,title,slug,pos,ccount
    match=re.compile('{"id":"(.+?)","vendorka_id":"(.+?)","name":"(.+?)","slug":"(.+?)","position":"(.+?)","content_count":"(.+?)","updated_at":"').findall(link)
    for id,vid,title,slug,pos,ccount in match:
        url = slug + '<>0'
        thumb = "http://static.filmon.com/couch/genres/%s/image.png" % slug
        addDir(title,url,201,thumb, '','')
        setView('episodes', 'episodes-view')

def on_demand_list(url):
    urlsplit=url.split('<>')
    genre = urlsplit[0]
    startindex=urlsplit[1]
    nextindex=int(startindex) + 16
    if startindex == '0':
        featuredurl = 'http://www.filmon.com/api/vod/search?genre=%s&is_featured=1&max_results=8&start_index=0' % genre
        link = net.http_GET(featuredurl).content.encode("utf-8").rstrip()
        all_videos = regex_get_all(link, '"id":', 'is_synchronized')
        for a in all_videos:
            title = regex_from_to(a, 'title":"', '"')
            id = regex_from_to(a, 'id":', ',"')
            thumb = 'http://static.filmon.com/couch/vod_content/%s/thumb_220px.png' % id
            plot = regex_from_to(a, 'description":"', '"')
            slug = regex_from_to(a, 'slug":"', '"')
            url = "%s<>%s" % (id,slug)
            if ' Series' in title:
                addDir(title,url,202,thumb, '',plot)
            else:
                addDirPlayable(title,url,203,thumb,"",plot, "", "od")
	
    url = 'http://www.filmon.com/api/vod/search?genre=%s&max_results=16&noepisode=1&start_index=%s' % (genre,startindex)
    np_url = "%s<>%s" % (genre, nextindex)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    all_videos = regex_get_all(link, '"id":', 'is_synchronized')
    for a in all_videos:
        title = regex_from_to(a, 'title":"', '"')
        id = regex_from_to(a, 'id":', ',"')
        thumb = 'http://static.filmon.com/couch/vod_content/%s/thumb_220px.png' % id
        plot = regex_from_to(a, 'description":"', '"')
        slug = regex_from_to(a, 'slug":"', '"')
        url = "%s<>%s" % (id,slug)
        if ' Series' in title:
            addDir(title,url,202,thumb, '',plot)
        else:
            addDirPlayable(title,url,203,thumb,"",plot, "", "od")
    addDir("[COLOR gold]>> Next Page[/COLOR]",np_url,201,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'next.png')), '','')
    setView('episodes', 'episodes-view')
	
def on_demand_series_list(name,url,iconimage):
    playlist = []
    id = url.split('<>')[0]
    slug = url.split('<>')[1]
    url = 'http://www.filmon.com/api/vod/movie?id=%s' % slug
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    eplink = regex_from_to(link, 'episodes":', ',"type').replace('"','').replace('[','').replace(']','')
    url = "http://www.filmon.com/api/vod/movies?ids=%s" % eplink
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    all_s = regex_get_all(link, '"id', '}')
    for s in all_s:
        plot = regex_from_to(s, '"description":"', '",')
        title = regex_from_to(s, '"title":"', '",')
        id = regex_from_to(s, 'id":', ',"')
        slug = regex_from_to(s, '"slug":"', '",')
        url = "%s<>%s" % (id,slug)
        thumb = thumb = 'http://static.filmon.com/couch/vod_content/%s/thumb_220px.png' % id
        addDirPlayable(title,url,203,thumb,"",plot, "", "od")
    setView('episodes', 'episodes-view')
	
def play_od(name, url, iconimage):

    playlist = []
    id = url.split('<>')[0]
    slug = url.split('<>')[1]
    url = 'http://www.filmon.com/api/vod/movie?id=%s' % id

    dp = xbmcgui.DialogProgress()
    dp.create('Opening ' + name.upper())
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    low = regex_from_to(link, '"low"', '}')
    lowurl = regex_from_to(low, '"url":"', '"').replace('\/', '/')
    high = regex_from_to(link, '"high"', 'watch-timeout')
    highurl = regex_from_to(high, '"url":"', '"').replace('\/', '/')
    try:
        timeout = regex_from_to(link, '"HD","watch-timeout":', "}")
    except:
        timeout = '86500'
    timeout = int(timeout)
	
    if FILMON_QUALITY == '480p' and (AUTO_SWITCH == False or timeout > 1800):
        STurl = highurl
    else:
        STurl = lowurl
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    handle = str(sys.argv[1])
    listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, path=STurl)
    if handle != "-1":
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(STurl,listitem)
    dp.close()
    keep_alive()	


def my_addons():
    addons = os.listdir(addon_path)
    for a in addons:
        if a.startswith('plugin.video') and a != 'plugin.video.F.T.V'  and a != 'plugin.video.adblocker' and a != 'plugin.video.gachecker' and not a.endswith('zip'):
            plugin_path = os.path.join(addon_path, a)
            iconimage = os.path.join(addon_path, a, 'icon.png')
            xml = os.path.join(addon_path, a, 'addon.xml')
            text = open(xml, 'r')
            r = text.read()
            text.close()
            try:
                id = strip_text(r, ' id="', '"')
            except:
                id = strip_text(r, " id='", "'")
            try:
                name = strip_text(r, ' name="', '"')
            except:
                name = strip_text(r, " name='", "'")

            addDirPlayable(name,a,143,iconimage,"","","","")
			
def my_addons_audio():
    addons = os.listdir(addon_path)
    for a in addons:
        if a.startswith('plugin.audio'):
            plugin_path = os.path.join(addon_path, a)
            iconimage = os.path.join(addon_path, a, 'icon.png')
            xml = os.path.join(addon_path, a, 'addon.xml')
            text = open(xml, 'r')
            r = text.read()
            text.close()
            try:
                id = strip_text(r, ' id="', '"')
            except:
                id = strip_text(r, " id='", "'")
            try:
                name = strip_text(r, ' name="', '"')
            except:
                name = strip_text(r, " name='", "'")

            addDirPlayable(name,a,143,iconimage,"","","","")

def run_addon(name, url, iconimage):
    url = "XBMC.Container.Update(plugin://%s)" % url
    xbmc.executebuiltin(url)

 
def play(name, url, iconimage):  
    link = open_url(url)
    match = re.compile('src="(.+?)" FlashVars="controlbar=over&skin=(.+?)&bufferlength=(.+?)&autostart=(.+?)&fullscreen=(.+?)&file=(.+?)&height').findall(link)
    for swf, nonswf, buffer, autostart, fullscreen, rtmp in match:
        stream_url = rtmp + ' swfUrl=' + swf + ' live=true timeout=45'
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)

def cartoons(name,url):
    addDir('Disney Junior Videos','http://www.disney.co.uk/disney-junior/content/video.jsp',301,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'disney_junior.jpg')), '', '')
    addDir('Disney Classic','http://gdata.youtube.com/feeds/api/users/UCa0h983kQj5OYa06gYhxgiw/uploads?start-index=1&max-results=50',395,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'mickey.gif')),'','')
	


def play_cartoons(name,url,iconimage):
    if 'auengine.com' in url:
        link=open_url(url)
        url=re.compile("url: '(.+?)'").findall(link)[0]
        
    if 'animeonhand.com' in url:
        html=open_url(url)
        url=re.compile("'file': '(.+?)'").findall(link)[0]
    
    handle = str(sys.argv[1])
    listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, path=url)
    if handle != "-1":	
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(url,listitem)	
        
		
def disney_jr(url):
    link = open_url(url)#.replace('\n','')
    categories = regex_get_all(link, '<li class="video_brand_promo">', '</li>')
    for c in categories:
        url = 'http://www.disney.co.uk' + regex_from_to(c, 'href="', '"')
        name = regex_from_to(c, 'data-originpromo="', '"').replace('-',' ').upper()
        thumb = 'http://www.disney.co.uk' + regex_from_to(c, 'data-hover="', '"')
        if name == 'A POEM IS HOME IN THE FASHION':
            thumb = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'disney_junior.jpg'))
        addDir(name,url,302,thumb, '','')
		
def disney_jr_links(name, url):
    link = open_url(url).replace('\t', '').replace('\n', '')
    videos = regex_get_all(link, 'div class="promo" style', 'img src="/cms_res/disney-junior/images/promo')
    for v in videos:
        url = 'http://www.disney.co.uk' + regex_from_to(v, 'href="', '"')
        name = regex_from_to(v, 'data-itemName="', '"').replace('-',' ').upper()
        thumb = 'http://www.disney.co.uk' + regex_from_to(v, 'img src="', '"')
        addDirPlayable(name,url,310,thumb,'', '', '', 'djr')
	
def disney_play(name, url, iconimage):
    urlid = url.replace('http://www.disney.co.uk/disney-junior/content/video.jsp?v=','')
    link = open_url(url)
    stream = regex_from_to(link, urlid, 'progressive')
    server = regex_from_to(stream,'server":"', '"')
    strm = regex_from_to(stream, 'program":"', '"')
    url = server + strm + ' swfVfy=1'
    title = regex_from_to(stream, 'pageTitle":"', '"').replace('Disney Junior | Videos - ', '')
    liz=xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty("IsPlayable","true")
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()
    pl.add(url, liz)
    xbmc.Player().play(pl)
	
def disney_playlist(name, url, iconimage):
    dp = xbmcgui.DialogProgress()
    dp.create("F.T.V",'Creating Playlist')
    playlist = []
    link = open_url(url)
    stream = regex_get_all(link, 'analyticsAssetName', 'progressive')
    nItem = len(stream)
    for s in stream:
        server = regex_from_to(s,'server":"', '"')
        strm = regex_from_to(s, 'program":"', '"')
        url = server + strm + ' swfVfy=1'
        title = regex_from_to(s, 'pageTitle":"', '"').replace('Disney Junior | Videos - ', '')
        liz=xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": title} )
        liz.setProperty("IsPlayable","true")
        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        pl.clear()
        playlist.append((url, liz))
        progress = len(playlist) / float(nItem) * 100  
        dp.update(int(progress), 'Adding to Your Playlist',title)

        if dp.iscanceled():
            return
    dp.close()
    for blob ,liz in playlist:
        try:
            if blob:
                pl.add(blob,liz)
        except:
            pass
    if not xbmc.Player().isPlayingVideo():
        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(pl)
		
def youtube_videos(name,url,iconimage):
    find_url=url.find('?')+1
    keep_url=url[:find_url]
    
    iconimage=""
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(link,"<entry>(.*?)</entry>")
    
    for entry in matches:
        
        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>").replace("&amp;","&")
        plot = plugintools.find_single_match(entry,"<media\:descriptio[^>]+>([^<]+)</media\:description>")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        video_id = plugintools.find_single_match(entry,"http\://www.youtube.com/watch\?v\=([^\&]+)\&").replace("&amp;","&")
        play_url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+video_id

        plugintools.add_item( action="play" , title=title , plot=plot , url=play_url ,thumbnail=thumbnail , folder=True )
    
    # Calculates next page URL from actual URL
    start_index = int( plugintools.find_single_match( link ,"start-index=(\d+)") )
    max_results = int( plugintools.find_single_match( link ,"max-results=(\d+)") )
    next_page_url = keep_url+"start-index=%d&max-results=%d" % ( start_index+max_results , max_results)

    addDir(">> Next page",next_page_url,395,"",'','')

		
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
		
def list_favourites(name, url, iconimage):
    if  'Movies' in name:
        dir = FAV_MOV
    else:
        dir = FAV_CHAN
    if os.path.isfile(dir):
        s = read_from_file(dir)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                url1 = list1[2]
                thumb = urllib.unquote(list1[1])
                url = urllib.unquote(regex_from_to(url1, 'url=', 'mode').replace('&', ''))
                mode = regex_from_to(url1, 'mode=', 'iconimage').replace('&', '')
                try:
                    start = regex_from_to(url1, 'channel/', 'mode').replace('&', '')
                except:
                    start = ''
                if dir == FAV_CHAN:
                    ch_id = url1[url1.find('ch_fanart='):]
                    ch_id = ch_id.replace('ch_fanart=','')#channel/
                else:
                    ch_id = ''
                addDirPlayable(title,url,mode,thumb,ch_id,'', start, 'favlist')
                #addLink(title,url,thumb,list,'','', '', '', '')

def add_favourite(name, url, iconimage, ch_id, dir,text):
    ch_name = name
    name = urllib.quote(str(name))
    url = urllib.quote(str(url))
    iconimage = urllib.quote(str(iconimage))
    ch_id = urllib.quote(str(ch_id))
    if 'rtmp' in url:
        url = sys.argv[0] + '?name=%s&url=%s&mode=111&iconimage=%s' % (name, url, iconimage)
    else:
        url = sys.argv[0] + '?name=%s&url=%s&mode=125&iconimage=%s&ch_fanart=%s' % (name, url, iconimage,ch_id)
    data = "%s<>%s<>%s" % (ch_name, iconimage, url)
    add_to_list(data, dir)
    notification(ch_name, "[COLOR lime]" + text + "[/COLOR]", '5000', iconimage)
	
def add_favourite_movie(name, url, iconimage, ch_id, dir,text):#play_ng(name,url,iconimage)
    ch_name = name
    name = urllib.quote(str(name))
    url = urllib.quote(str(url))
    iconimage = urllib.quote(str(iconimage))
    url = sys.argv[0] + '?name=%s&url=%s&mode=111&iconimage=%s' % (name, url, iconimage)
    data = "%s<>%s<>%s" % (ch_name, iconimage, url)
    add_to_list(data, dir)
    notification(ch_name, "[COLOR lime]" + text + "[/COLOR]", '5000', iconimage)
	
def remove_favourite(name, url, iconimage, ch_fanart,text):
    ch_name = name
    name = urllib.quote(str(name))
    url = urllib.quote(str(url))
    iconimage = urllib.quote(str(iconimage))
    ch_id = urllib.quote(str(ch_fanart))
    if ch_fanart == '':
        dir = FAV_MOV
        url = sys.argv[0] + '?name=%s&url=%s&mode=111&iconimage=%s' % (name, url, iconimage)
    else:
        dir = FAV_CHAN
        url = sys.argv[0] + '?name=%s&url=%s&mode=125&iconimage=%s&ch_fanart=%s' % (name, url, iconimage,ch_id)
    data = "%s<>%s<>%s" % (ch_name, iconimage, url)
    remove_from_list(data, dir)
    notification(ch_name, "[COLOR lime]" + text + "[/COLOR]", '5000', urllib.unquote(iconimage))
	
def add_to_file(path, content, append=True, silent=False):
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
		
def create_all_strm_file(name, url, mode, dir_path, iconimage):
    listname=url
    try:
        url = 'http://gappcenter.com/app/cartoon/mapi.php?action=getlistcontent&cate=%s&pageindex=0&pagesize=1000&os=newiosfull&version=2.1&deviceid=&token=&time=&device=iphone' % url
        link = open_url(url)
        if not 'Link' in link:
            list = read_from_file(cartoonlinks)
            link = regex_from_to(list, name + '<<', '>>')
    except:
        list = read_from_file(cartoonlinks)
        link = regex_from_to(list, name + '<<', '>>')
    match = re.compile('"Name":"(.+?)","Type":"(.+?)","Link":"(.+?)","Image":"(.+?)"').findall(link)
    for title,type,url,iconimage in match:
        if listname=='picasa_disneycollection':
            title=title[5:]
        url=url.replace('\/', '/')
        iconimage=iconimage.replace('\/', '/')
        create_strm_file(title, url, '396', dir_path, iconimage)
    xbmc.sleep(1000)
    scan_library()
		
def create_strm_file(name, url, mode, dir_path, iconimage):
    strm_string = create_url(name, mode, url=url, iconimage=iconimage)
    #name1 = re.sub(r'\[[^]]*\]', '', name1)
    filename = clean_file_name("%s.strm" % name)
    path = os.path.join(dir_path, filename)
    if not os.path.exists(path):
        stream_file = open(path, 'w')
        stream_file.write(strm_string)
        stream_file.close()
        scan_library()
    #except:
        #xbmc.log("[F.T.V] Error while creating strm file for : " + name)
		
def create_url(name, mode, url, iconimage):
    name = urllib.quote(str(name))
    url = urllib.quote(str(url))
    iconimage = urllib.quote(str(iconimage))
    mode = str(mode)
    url = sys.argv[0] + '?name=%s&url=%s&mode=%s&iconimage=%s' % (name, url, mode, iconimage)
    return url
	
def download_only(name,url,iconimage,dir_path):
    filename = name + '.mp4'
    WAITING_TIME = 5
    directory=dir_path
    data_path = os.path.join(directory, filename)
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
        urllib.urlretrieve(data, path)

        notification('Download finished', name, '5000', iconart)
		
    def _dlhook(self, numblocks, blocksize, filesize, dt, start_time, path, waiting):
        raise StopDownloading('Stopped Downloading')
        callEndOfDirectory = False
		
class StopDownloading(Exception): 
    def __init__(self, value): 
        self.value = value 
    def __str__(self): 
        return repr(self.value)
		
def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
		
def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
		
def scan_library():
    if xbmc.getCondVisibility('Library.IsScanningVideo') == False:           
        xbmc.executebuiltin('UpdateLibrary(video)')
		
link = open_url(session_url)
session_key = regex_from_to(link, 'session_key":"', '"')
   

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

def addLink(name,url,iconimage,description,status,download_link, p_id, start, p_name):
        ok=True
        contextMenuItems = []
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        if p_id != "":
            contextMenuItems.append(("Delete Recording",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=133&iconimage=%s)'%(sys.argv[0],p_name,str(p_id),iconimage)))
            if status == "Recorded" and download_link != "error":
                contextMenuItems.append(("Download Recording",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=139&iconimage=%s)'%(sys.argv[0],p_name,str(download_link),iconimage)))
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok


def addDir(name,url,mode,iconimage,ch_fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        contextMenuItems = []
        contextMenuItems.append(('Hide Channel Group', 'XBMC.RunPlugin(%s?mode=10&url=%s)'% (sys.argv[0],str(name))))
        if url == 'picasa_topmovie' or url == 'picasa_topcartoon' or url == 'picasa_disneycollection':
            contextMenuItems.append(("Add ALL to XBMC Library",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=402&iconimage=%s)'%(sys.argv[0],urllib.quote(name), urllib.quote(url),urllib.quote(iconimage))))	
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.addContextMenuItems(contextMenuItems, False)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
	
def addDirPlayable(name,url,mode,iconimage,ch_fanart, description, start, function):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&start="+str(start)+"&ch_fanart="+str(ch_fanart)
        ok=True
        contextMenuItems = []
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        if function != 'od' and function != 'gb'and function != 'djr' and function != 'ng' and function != '' and function != 'favlist':
            contextMenuItems.append(("TV Guide",'XBMC.Container.Update(%s?name=%s&url=%s&mode=127&iconimage=%s)'%(sys.argv[0],ch_fanart, start,iconimage)))
            contextMenuItems.append(("Toggle My Channels",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=135&iconimage=%s)'%(sys.argv[0],name,ch_fanart,iconimage)))
            contextMenuItems.append(("Add to FTV Favourites",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=410&iconimage=%s&ch_fanart=%s)'%(sys.argv[0],urllib.quote(name),urllib.quote(url),urllib.quote(iconimage),ch_fanart)))
        if function == 'favlist':
            contextMenuItems.append(("Remove from FTV Favourites",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=416&iconimage=%s&ch_fanart=%s)'%(sys.argv[0],urllib.quote(name),urllib.quote(url),urllib.quote(iconimage),ch_fanart)))
        if function == 'djr':
            contextMenuItems.append(("Play All Videos",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=303&iconimage=%s)'%(sys.argv[0],urllib.quote(name), urllib.quote(url),iconimage)))
        if function == 'ng':
            contextMenuItems.append(("Add Channel to Group",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=112&iconimage=%s)'%(sys.argv[0],urllib.quote(start), str(ch_fanart),str(description))))
            contextMenuItems.append(("Add to FTV Favourites",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=410&iconimage=%s&ch_fanart=%s)'%(sys.argv[0],urllib.quote(name),urllib.quote(url),urllib.quote(iconimage),ch_fanart)))
        if ch_fanart == 'picasa_topmovie' or ch_fanart == 'picasa_topcartoon' or ch_fanart == 'picasa_disneycollection':
            contextMenuItems.append(("Add to XBMC Library",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=401&iconimage=%s)'%(sys.argv[0],urllib.quote(name), urllib.quote(url),urllib.quote(iconimage))))
            contextMenuItems.append(("Download",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=403&iconimage=%s)'%(sys.argv[0],urllib.quote(name), urllib.quote(url),urllib.quote(iconimage))))
            contextMenuItems.append(("Add to FTV Favourites",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=411&iconimage=%s&ch_fanart=%s)'%(sys.argv[0],urllib.quote(name),urllib.quote(url),urllib.quote(iconimage),ch_fanart)))			
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
        ch_fanart=urllib.unquote_plus(params["ch_fanart"])
except:
        pass


if mode==None or url==None or len(url)<1:
        CATEGORIES()
        
       
elif mode==121:
        other_menu()
		
elif mode==122:
        favourites()
		
elif mode==110:
        non_geo()
		
elif mode==151:
        featured()
		
elif mode==15:
        play(name, url, iconimage)
		
elif mode==2:
        other()
		
elif mode == 10:
        print "MODE " + url
        add_to_list(url, HIDDEN_FILE)
		
elif mode==123:
        group_channels(url, name)
		
elif mode==125:
        login()
        play_filmon(name, url, iconimage, ch_fanart)
		
elif mode == 111:
        play_ng(name,url,iconimage)
		
elif mode == 112:
        add_ng(name, url, iconimage)
		
elif mode==126:
        login()
        play_filmon_gb(name, url, iconimage)
		
elif mode==127:
        tv_guide(name, url, iconimage)
		
elif mode == 129:
        record_programme(name,url,ch_fanart,start)

elif mode == 131:
        recordings(url)
		
elif mode == 133:
        delete_recording(name,url,iconimage)
        recordings(url)
		
elif mode == 135:
        add_fav(name, url, iconimage)
		
elif mode == 137:
        delete_fav(name, url, iconimage)
		
elif mode == 139:
        download_rec(name, url, iconimage)

elif mode == 141:
        my_addons()

elif mode == 145:
        my_addons_audio()		

elif mode == 143:
        run_addon(name, url, iconimage)	

elif mode == 199:
        on_demand()

elif mode == 201:
        on_demand_list(url)
		
elif mode == 202:
        on_demand_series_list(name,url,iconimage)

elif mode == 203:
        play_od(name, url, iconimage)
		
elif mode == 399:
        cartoons(name,url)
		
	
elif mode == 396:
        play_cartoons(name,url,iconimage)
		
elif mode == 395:
        youtube_videos(name,url,iconimage)
		
elif mode == 301:
        disney_jr(url)	

elif mode == 302:
        disney_jr_links(name, url)
		
elif mode == 303:
        disney_playlist(name, url, iconimage)

elif mode == 310:
        disney_play(name, url, iconimage)

elif mode==401:
        create_strm_file(name, url, '396', MOVIE_DIR, iconimage)

elif mode==402:
        create_all_strm_file(name, url, '396', MOVIE_DIR, iconimage)

elif mode==403:
        download_only(name, url, iconimage,MOVIE_DIR)

elif mode == 410:
    add_favourite(name, url, iconimage, ch_fanart, FAV_CHAN,"Added to Favourites")

elif mode == 411:
    add_favourite_movie(name, url, iconimage, "", FAV_MOV,"Added to Favourites")
	
elif mode == 416:
    remove_favourite(name, url, iconimage, ch_fanart,"Removed from Favourites")

elif mode == 415:
    list_favourites(name, url, iconimage)

elif mode == 417:
    play_favourites(name, url, iconimage)	

xbmcplugin.endOfDirectory(int(sys.argv[1]))

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
net = Net()


ADDON = settings.addon()
FILMON_KEEP = settings.keep_session_flag()
FILMON_ACCOUNT = settings.filmon_account()
FILMON_USER = settings.filmon_user()
FILMON_QUALITY = settings.filmon_quality()
AUTO_SWITCH = settings.auto_switch()
FILMON_PASS = md5(settings.filmon_pass()).hexdigest()
FILMON_PASSWORD = settings.filmon_pass()
MY_VIDEOS = settings.my_videos()
MY_AUDIO = settings.my_audio()
OTHER_MENU = settings.other_menu()
DOWNLOAD_PATH = settings.download_path()
cookie_jar = settings.cookie_jar()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'fanart.jpg'))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'icon.png'))
channel_list = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V/helpers', 'channel.list'))
base_url = 'http://www.filmon.com/'
disneyjrurl = 'http://www.disney.co.uk/disney-junior/content/video.jsp?b='


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

    currentWindow = xbmcgui.getCurrentWindowId()
    if currentWindow == 10000:
        url = 'http://www.filmon.com/user/logout'
        net.set_cookies(cookie_jar)
        net.http_GET(url)
        session_id = xbmcgui.Window(10000).getProperty("session_id")
        lourl = "http://www.filmon.com/api/logout?session_key=%s" % (session_id)
        open_url(lourl)
        xbmcgui.Window(10000).clearProperty("session_id")
        print 'F.T.V..........logged out of Filmon'
        return
    url = "http://www.filmon.com/ajax/keepAlive"
    net.set_cookies(cookie_jar)
    net.http_GET(url)
    net.save_cookies(cookie_jar)
    #if xbmcgui.Window(10000).getProperty("session_id"):
        #session_id = xbmcgui.Window(10000).getProperty("session_id")
        #url = "http://www.filmon.com/api/keep-alive?session_key=%s" % (session_id)
        #open_url(url)
    #print 'F.T.V..........Filmon session kept alive'
    tloop = Timer(60.0, keep_alive)
    tloop.start()
	
def CATEGORIES():
    login()
    if MY_VIDEOS:
        addDir('My Video Addons','url',141,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'video_addons.jpg')), '', '')
    if MY_AUDIO:
        addDir('My Audio Addons','url',145,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'audio_addons.jpg')), '', '')
    #if OTHER_MENU:
        #addDir('Other Video Links','url',121,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'other_video.png')), '', '')
    addDir('Disney Junior Videos','http://www.disney.co.uk/disney-junior/content/video.jsp',301,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'disney_junior.jpg')), '', '')
    addDir('FilmOn Demand ','url',199,'http://www.filmon.com/tv/themes/filmontv/img/mobile/filmon-logo-stb.png', '', '')
    addDir('My Channels','url',122,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'my_channels.jpg')), '', '')
    addDir('My Recordings','url',131,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'f_record.jpg')), '', '')
    net.set_cookies(cookie_jar)
    url = 'http://www.filmon.com/groups'
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    all_groups = regex_get_all(link, '<li class="group-item">', '</li>')
    for groups in all_groups:
        group_id = regex_from_to(groups, 'http://static.filmon.com/couch/groups/','/big_logo.png')
        title = regex_from_to(groups, 'title="', '"')
        thumb = 'http://static.filmon.com/couch/groups/%s/big_logo.png'	% group_id
        url = base_url + regex_from_to(groups, '<a href="/', '">')
        addDir(title,url,123,thumb, '','')
        setView('episodes', 'episodes-view')
    if not FILMON_USER in link:
        notification('Not logged in at Filmon', 'Check settings', '5000', iconart)
    else:
        notification('Logged in at Filmon', FILMON_USER, '5000', iconart)

		
def group_channels(url, title):
    gt = title
    name_lst = []
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()

    channels = regex_get_all(link, '<li class="channel', '</li>')
    for channel in channels:
        alias = regex_from_to(channel, 'alias="', '" channel_id')
        channel_id = regex_from_to(channel, 'id="', '" alias')
        title = regex_from_to(channel, 'channel_title">', '</')
        name_lst.append(title)
        description = clean_file_name(regex_from_to(channel, '<p>', '</p>'), use_blanks=False)
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
            try:
                st_url = list1[3]
            except:
                st_url = "blank"
            par = "%s<>%s" % (st_id, st_url)
            thumb = 'http://static.filmon.com/couch/channels/%s/extra_big_logo.png' % str(st_id).rstrip()
            if st_grp == gt and st_name not in name_lst:
                addDirPlayable(st_name,gt,125,thumb,par,"", "", "grp")

    if gt == 'UK LIVE TV':
        addDirPlayable('Chelsea TV','http://www.watchfeed.co/watch/44-1/chelsea-tv.html',15,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'chelsea.jpg')), '', '', '', "")
    setView('episodes', 'episodes-view')
		
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
    tvg_list = regex_from_to(link, 'channel_tvguide =', 'current_channel_id')
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
                url = base_url + 'channel/' + str(channel_id)
                addDirPlayable('[COLOR cyan]' + title + '[/COLOR]',url,125,thumb,"",description, start, "gd")
            else:
                if allow_dvr == "true":
                    addDirPlayable(title,channel_id,129,thumb,p_id,description, start, "gd")
                else:
                    addDirPlayable(title + "  [COLOR red](not recordable)[/COLOR]",channel_id,"",thumb,p_id,description, start, "gd")
            setView('episodes', 'epg')

		
def play_filmon(name,url,iconimage,ch_id):
    print url, ch_id
    grpurl = url
    if url == "LOCAL TV" or url == "UK LIVE TV":
        parsplit = ch_id.split('<>')
        swap_ch = parsplit[0]
        swap_url = parsplit[1]
    else:
        swap_ch = ch_id


    if url == "LOCAL TV":
        url = 'http://www.filmon.com/channel/live'
        ch_id = '689'
    if url == "UK LIVE TV":
        url = 'http://www.filmon.com/channel/channel-5'
        ch_id = '22'

    pp = url.replace('channel', 'tv')
    streamerlink = net.http_GET(url).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    swfplay = 'http://www.filmon.com' + regex_from_to(streamerlink, '"streamer":"', '",').replace("\/", "/")
    #slink = open_url('http://www.filmon.com/api/init/')
    #smatch= re.compile('"session_key":"(.+?)"').findall(slink)
    #session_id=smatch[0]
    #xbmcgui.Window(10000).setProperty("session_id", session_id)
    #keep_alive()
    name = name.replace('[COLOR cyan]','').replace('[/COLOR]','')
    dp = xbmcgui.DialogProgress()
    dp.create('Opening ' + name.upper())
    utc_now = datetime.datetime.now()
    channel_name=name
    cl= 23 + len(ch_id)
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
		
    url = regex_from_to(link, "serverURL': u'", "',")
    url2 = url.split('/')
    url2 = url2[2]
    name = regex_from_to(link, "streamName': u'", "',")
    name = name.replace('.l.stream', '.low.stream').replace('.lo.stream', '.low.stream')
    if grpurl == "UK LIVE TV":
        name = name.replace('22', swap_ch)
        url = url.replace(url2, swap_url)
    if grpurl == "LOCAL TV":
        name = name.replace('689', swap_ch)
        url = url.replace(url2, swap_url)

    try:
        timeout = regex_from_to(link, "expire_timeout': u'", "',")
    except:
        timeout = '86500'
    if FILMON_QUALITY == "480p":
        name = name.replace('low', 'high')
    if name.endswith('m4v'):
        app = 'vodlast'
    else:
        appfind = url[7:].split('/')
        app = 'live/' + appfind[2]
		
    if url.endswith('/'):
        STurl = str(url) + ' playpath=' + name + ' swfUrl=' + swfplay + ' pageUrl=' + pp + ' live=1 timeout=10 swfVfy=1'
        STurl2 = str(url)  + name + ' playpath=' + name + ' swfUrl=' + swfplay + ' pageUrl=' + pp + ' live=1 timeout=10 swfVfy=1' 
    else:
        STurl = str(url) + ' playpath=' + name + ' swfUrl=' + swfplay + ' pageUrl=' + pp + ' live=1 timeout=10 swfVfy=1'
        STurl2 = str(url) + '/' + name + ' playpath=' + name + ' swfUrl=' + swfplay + ' pageUrl=' + pp + ' live=1 timeout=10 swfVfy=1'	
		
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    handle = str(sys.argv[1])
    try:
        if ch_id == '857' or 'http' not in grpurl:
            listitem = xbmcgui.ListItem(channel_name, iconImage=iconimage, thumbnailImage=iconimage, path=STurl2)
        else:
            listitem = xbmcgui.ListItem(p_name + ' ' + n_p_name, iconImage=iconimage, thumbnailImage=iconimage, path=STurl2)
        if handle != "-1":	
            listitem.setProperty("IsPlayable", "true")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        else:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(STurl2,listitem)
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
    match = re.compile('window.user_storage = {"total":(.+?),"available":(.+?),"recorded":(.+?)}').findall(link)
    for t, a, r in match:
        acc_status = "Allowed: %shrs - Recorded: %shrs - Available %shrs" % (t, r, a)
    addLink('[COLOR cyan]'+acc_status+'[/COLOR]',"","","","","", "", "", "")
    recordings = regex_get_all(link, 'stream_url', 'isSoftDeleted')
    for r in recordings:
        STname = regex_from_to(r, 'stream_name":"', '",').replace("\/", "/")
        STurl = regex_from_to(r, 'stream_url":"', '",').replace("\/", "/") + " playpath=" + "mp4:" + STname + " swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf pageUrl=http://www.filmon.com/my/recordings"
        p_id = regex_from_to(r, 'id":"', '",')
        p_name = regex_from_to(r, 'title":"', '",')
        description = regex_from_to(r, 'description":"', '",')
        channel_id = regex_from_to(r, 'channel_id":"', '",')
        logo = 'https://static.filmon.com/couch/channels/%s/extra_big_logo.png' % str(channel_id)
        start = regex_from_to(r, 'start_timestamp":"', '",')
        start_time = datetime.datetime.fromtimestamp(int(regex_from_to(r, 'start_timestamp":"', '",')))
        duration = regex_from_to(r, 'duration":"', '",')
        status = regex_from_to(r, 'status":"', '",')
        try:
            download_link = 'http://s2.dvr.gv.filmon.com/' + STname
        except:
            download_link = "error"
        text = "[COLOR gold]%s[/COLOR] %s (%s)" % (p_name, start_time.strftime('%d %b %H:%M'), status)
        addLink(text,STurl,logo,description,status,download_link, p_id, start,p_name)
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
    url = "http://demand.filmon.com"
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    all_cat = regex_from_to(link, '<div class="categories-list', '</div>')
    categories = regex_get_all(all_cat, '<a', '</a>')
    for c in categories:
        title = regex_from_to(c, '>', '</').strip()
        url = "http://demand.filmon.com/" + regex_from_to(c, 'href="', '"')
        addDir(title,url,201,'http://www.filmon.com/tv/themes/filmontv/img/mobile/filmon-logo-stb.png', '','')
        setView('episodes', 'episodes-view')

def on_demand_list(url):
    if "page=" in url:
        np_url = url[:len(url)-1] + str(int(url[len(url)-1:]) + 1)
    else:
        np_url = url + "?page=1"
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    all_videos = regex_get_all(link, '<div class="product-item col', '<div class="popover-content-bottom">')
    for video in all_videos:
        title = regex_from_to(video, 'popover-title">', '</span>')
        url = "http://demand.filmon.com" + regex_from_to(video, 'product-item-info" href="', '"')
        thumb = regex_from_to(video, 'img src="', '"')
        try:
            description = regex_from_to(video, '<p>', '</p>')
        except:
            description = ""
        addDirPlayable(title,url,203,thumb,"",description, "", "od")
    addDir("[COLOR gold]>> Next Page[/COLOR]",np_url,201,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'next.png')), '','')
    setView('episodes', 'episodes-view')
	
def play_od(name, url, iconimage):
    dp = xbmcgui.DialogProgress()
    dp.create('Opening ' + name.upper())
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    swf = "%s%s" % ('http://demand.filmon.com/sites/all/modules/demand/flash/FilmonPlayer.swf?', 'mvfu3k')
    stream = re.compile('livehttp":{(.+?),"url":"(.+?)","name":"(.+?)"}').findall(link)
    for vast, stUrl, playpath in stream:
        RTurl = stUrl.replace("\\/", "/").replace("\/", "/")
    STurl = RTurl
    handle = str(sys.argv[1])
    listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, path=STurl)
    if handle != "-1":	
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(STurl,listitem)
    dp.close()


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

def addLink(name,url,iconimage,description,status,download_link, p_id, start, p_name):
        ok=True
        contextMenuItems = []
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
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
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
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
        if function != 'od' and function != 'gb'and function != 'djr':
            contextMenuItems.append(("TV Guide",'XBMC.Container.Update(%s?name=%s&url=%s&mode=127&iconimage=%s)'%(sys.argv[0],ch_fanart, start,iconimage)))
            contextMenuItems.append(("Toggle My Channels",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=135&iconimage=%s)'%(sys.argv[0],name,ch_fanart,iconimage)))
        if function == 'djr':
            contextMenuItems.append(("Play All Videos",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=303&iconimage=%s)'%(sys.argv[0],urllib.quote(name), urllib.quote(url),iconimage)))
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
		
elif mode==151:
        featured()
		
elif mode==15:
        play(name, url, iconimage)
		
elif mode==2:
        other()
		
elif mode==123:
        group_channels(url, name)
		
elif mode==125:
        login()
        play_filmon(name, url, iconimage, ch_fanart)
		
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

elif mode == 203:
        play_od(name, url, iconimage)

elif mode == 301:
        disney_jr(url)	

elif mode == 302:
        disney_jr_links(name, url)
		
elif mode == 303:
        disney_playlist(name, url, iconimage)

elif mode == 310:
        disney_play(name, url, iconimage)		

xbmcplugin.endOfDirectory(int(sys.argv[1]))

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

ADDON = settings.addon()
FILMON_KEEP = settings.keep_session_flag()
FILMON_ACCOUNT = settings.filmon_account()
FILMON_USER = settings.filmon_user()
FILMON_QUALITY = settings.filmon_quality()
AUTO_SWITCH = settings.auto_switch()
FILMON_PASS = md5(settings.filmon_pass()).hexdigest()
MY_VIDEOS = settings.my_videos()
MY_AUDIO = settings.my_audio()
OTHER_MENU = settings.other_menu()
DOWNLOAD_PATH = settings.download_path()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'fanart.jpg'))
session_url = 'http://www.filmon.com/api/init/'
base_url = 'http://www.filmon.com/'
grp_art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art'))

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
def keep_session():
    currentWindow = xbmcgui.getCurrentWindowId()
    if currentWindow == 10000:
        session_id = xbmcgui.Window(10000).getProperty("session_id")
        lourl = "http://www.filmon.com/api/logout?session_key=%s" % (session_id)
        print lourl
        open_url(lourl)
        xbmcgui.Window(10000).clearProperty("session_id")
        print 'F.T.V..........logged out of Filmon'
        return
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url = "http://www.filmon.com/api/keep-alive?session_key=%s" % (session_id)
    open_url(url)
    print 'F.T.V..........Filmon session kept alive'
    tloop = Timer(60.0, keep_session)
    tloop.start()

if not xbmcgui.Window(10000).getProperty("session_id"):
    link = open_url(session_url)
    match= re.compile('"session_key":"(.+?)"').findall(link)
    session_id=match[0]
    if FILMON_ACCOUNT:
        login_url = "%s%s%s%s%s%s" % ("http://www.filmon.com/api/login?session_key=", session_id, "&login=", FILMON_USER, "&password=", FILMON_PASS)
        login = open_url(login_url)
        print "F.T.V......Not logged in"
        xbmcgui.Window(10000).setProperty("session_id", session_id)
        keep_session()
    else:
        print "F.T.V......Not logged in"
        xbmcgui.Window(10000).setProperty("session_id", session_id)
        keep_session()
            
session_id = xbmcgui.Window(10000).getProperty("session_id")

def CATEGORIES():
    if MY_VIDEOS:
        addDir('My Video Addons','url',141,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'video_addons.jpg')), '', '')
    if MY_AUDIO:
        addDir('My Audio Addons','url',145,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'audio_addons.jpg')), '', '')
    if OTHER_MENU:
        addDir('Other Video Links','url',121,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'other_video.png')), '', '')
    addDir('My Channels','url',122,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'my_channels.jpg')), '', '')
    addDir('My Recordings','url',131,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'f_record.jpg')), '', '')
    addDir('Most Watched','url',151,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'featured.png')), '', '')
    url = "%s%s%s" % (base_url,'/tv/api/groups?session_key=', (session_id))
    link = open_url(url)
    all_groups = regex_get_all(link, '{', 'channels_count')
    for groups in all_groups:
        group_id = regex_from_to(groups, 'group_id":"', '",')
        title = regex_from_to(groups, 'title":"', '",')
        thumb = regex_from_to(groups, 'logo_148x148_uri":"', '",').replace('\\', '')
        url = regex_from_to(groups, 'group_id":"', '",')
        addDir(title,group_id,123,thumb, '','')
        setView('episodes', 'episodes-view')

def other_menu():
    addDirPlayable('Chelsea TV','http://www.watchfeed.co/watch/44-1/chelsea-tv.html',15,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'chelsea.jpg')), '', '', '', "")
		
def group_channels(url, title):
    url = "%s%s%s%s%s" % (base_url, 'api/group/', url, '?session_key=', session_id)
    link = open_url(url)
    all_channels = regex_from_to(link, 'channels":', 'channels_count')
    channels = regex_get_all(all_channels, '{"id"', '}}')
    for channel in channels:
        ch_type = regex_from_to(channel,'type":"', '",')
        channel_id = regex_from_to(channel, '"id":"', '",')
        title = regex_from_to(channel, 'title":"', '",').encode("utf-8")
        description = clean_file_name(regex_from_to(channel, 'description":"', '",'), use_blanks=False)
        thumb = regex_from_to(channel, 'size":"300x300","url":"', '"}').replace("\/", "/")
        favourite = regex_from_to(channel, 'isFavorited":', ',"')
        try:
            ch_fanart = regex_from_to(channel, 'size":"854x480","url":"', '"}').replace('\/', '/')
        except:
            ch_fanart = regex_from_to(channel, 'screenshots":[{"size":"original","url":"', '"}').replace('\/', '/')
        addDirPlayable(title,channel_id,125,thumb,ch_fanart,description, "", "grp")
        setView('episodes', 'episodes-view')
		
def favourites():
    fav = []
    session_id = renew_session()
    url='http://www.filmon.com/api/favorites?session_key=%s&run=get' % (session_id)
    link = open_url(url)
    print link
    channels = regex_get_all(link, '{', '}')
    for c in channels:
        channel_id = regex_from_to(c, '"channel_id":"', '",')
        fav.append(channel_id)
    all_ch(fav)
 
def all_ch(fav):		
    all_c_url = 'http://www.filmon.com/tv/api/channels?session_key=%s' % (session_id)
    all_link = open_url(all_c_url)
    for f in fav:
        print f
        fstring = '"id":"%s"' % (f)
        channel = regex_from_to(all_link, fstring, 'is_favorite')
        title = regex_from_to(channel, 'title":"', '",').encode("utf-8")
        description = ""
        thumb = regex_from_to(channel, 'extra_big_logo":"', '",').replace("\/", "/")
        try:
            ch_fanart = regex_from_to(channel, 'size":"854x480","url":"', '"}').replace('\/', '/')
        except:
            ch_fanart = "" 
        addDirPlayable(title,f,125,thumb,ch_fanart,description, "", "fav")
        setView('episodes', 'episodes-view')
		
def featured():
    url='http://www.filmon.com/api/featured?session_key=%s&run=get'% (session_id)
    link = open_url(url)
    channel_ids = regex_get_all(link, '{', '}')
    for id in channel_ids:
        channel_id = regex_from_to(id, 'id":"', '",')
        title = regex_from_to(id, 'title":"', '",').encode("utf-8")
        thumb = 'https://static.filmon.com/couch/channels/%s/extra_big_logo.png' % str(channel_id)
        ch_fanart = "" 
        addDirPlayable(title,channel_id,125,thumb,ch_fanart,"", "", "grp")
        setView('episodes', 'episodes-view')
		
def add_fav(name, ch_id, iconimage):
    dialog = xbmcgui.Dialog()
    url = 'http://www.filmon.com/api/favorites?session_key=%s&channel_id=%s&run=add'%(session_id,ch_id)
    link = open_url(url)
    text = regex_from_to(link, 'reason":"', '",').replace('"',' ')
    dialog.ok("Add Favourite",name.upper(),text.upper())  

def delete_fav(name, ch_id, iconimage):
    dialog = xbmcgui.Dialog()
    url = 'http://www.filmon.com/api/favorites?session_key=%s&channel_id=%s&run=remove'%(session_id,ch_id)
    link = open_url(url)
    text = regex_from_to(link, 'reason":"', '",').replace('"',' ')
    dialog.ok("Remove Favourite",name.upper(),text.upper())
    xbmc.executebuiltin("Container.Refresh")
		
def tv_guide(name, url, iconimage):
    url='http://www.filmon.com/tv/api/tvguide/%s?session_key=%s' % (url, session_id)
    link = open_url(url)
    programmes = regex_get_all(link, '{', 'vendor_id')
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
                addDirPlayable('[COLOR cyan]' + title + '[/COLOR]',channel_id,125,thumb,"",description, start, "gd")
            else:
                if allow_dvr == "true":
                    addDirPlayable(title,channel_id,129,thumb,p_id,description, start, "gd")
                else:
                    addDirPlayable(title + "  [COLOR red](not recordable)[/COLOR]",channel_id,"",thumb,p_id,description, start, "gd")
            setView('episodes', 'episodes-view')

		
def play_filmon(name,url,iconimage):
    session_id = renew_session()
    dp = xbmcgui.DialogProgress()
    dp.create('Opening ' + name.upper())
    url = "%s%s%s%s%s" % (base_url, 'api/channel/', url, '?session_key=', session_id)
    utc_now = datetime.datetime.now()
    channel_name=name.upper()
    link = open_url(url)
    nowplaying = regex_from_to(link, 'tvguide":', 'upnp_enabled')
    pr_list = regex_get_all(nowplaying, '{"programme', '}')
    for p in pr_list:
        programme_name = regex_from_to(p, 'programme_name":"', '",')
        try:
            start_time = datetime.datetime.fromtimestamp(int(regex_from_to(p, 'startdatetime":"', '",')))
            end_time = datetime.datetime.fromtimestamp(int(regex_from_to(p, 'enddatetime":"', '",')))
            if start_time < utc_now and end_time > utc_now:
                npet = regex_from_to(p, 'enddatetime":"', '",')
                programme_name = regex_from_to(p, 'programme_name":"', '",').replace("\/", "/")
                description = regex_from_to(nowplaying, 'programme_description":"', '",').replace('\u2019', "'").replace('\u2013', "-")
                start_t = start_time.strftime('%H:%M')
                end_t = end_time.strftime('%H:%M')
                p_name = "%s (%s-%s)" % (programme_name, start_t, end_t)
                dp.update(50, p_name)
                try:
                    next = regex_from_to(nowplaying, 'startdatetime":"' +npet, '}')
                    n_start_time = datetime.datetime.fromtimestamp(int(npet))
                    n_end_time = datetime.datetime.fromtimestamp(int(regex_from_to(next, 'enddatetime":"', '",')))
                    n_programme_name = regex_from_to(next, 'programme_name":"', '",').replace("\/", "/")
                    n_start_t = n_start_time.strftime('%H:%M')
                    n_end_t = n_end_time.strftime('%H:%M')
                    n_p_name = "[COLOR cyan]Next: %s (%s-%s)[/COLOR]" % (n_programme_name, n_start_t, n_end_t)
                except:
                    n_p_name = ""
        except:
            p_name = programme_name
            n_p_name = ""
    
    streams = regex_from_to(link, 'streams":', 'logo')
    hl_streams = regex_get_all(streams, '{', '}')
    for stream in hl_streams:
        timeout = regex_from_to(stream, 'watch-timeout":', '}')
        if len(timeout) < 5 and AUTO_SWITCH:
            quality = 'donotplay'
        else:
            quality = regex_from_to(stream, 'quality":"', '",')
        url = regex_from_to(stream, 'url":"', '",').replace("\/", "/")
        name = regex_from_to(stream, 'name":"', '",')
        if name.endswith('m4v'):
            app = 'vodlast'
        else:
            appfind = url[7:].split('/')
            app = 'live/' + appfind[2]
        if quality == FILMON_QUALITY or (quality == 'low' and AUTO_SWITCH):
            STurl = str(url) + ' playpath=' + name + ' app=' + app + ' swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=26'+' tcUrl='+ str(url) + ' pageUrl=http://www.filmon.com/' + ' live=1 timeout=45 swfVfy=1'
            STurl2 = str(url) + '/' + name + ' playpath=' + name + ' app=' + app + ' swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=26' + ' tcUrl='+ str(url) + ' pageUrl=http://www.filmon.com/' + ' live=1 timeout=45 swfVfy=1'

    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    handle = str(sys.argv[1])
    try:
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

def record_programme(name,ch_id,p_id,start):
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Record Programme?", '', name.upper()):
        rec_url ='http://filmon.com/api/dvr-add?session_key=%s&channel_id=%s&programme_id=%s&start_time=%s' % (session_id,ch_id,p_id,start)
        link = open_url(rec_url)
        text = regex_from_to(link, 'reason":"', '"}').replace('"',' ')
        dialog = xbmcgui.Dialog()
        dialog.ok("Record Programme",name.upper(),text.upper())
		
def delete_recording(name,start,iconimage):
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Recording?", '', name.upper()):
        rec_url ='http://filmon.com/api/dvr-remove?session_key=%s&recording_id=%s' % (session_id, start)
        link = open_url(rec_url)
        text = regex_from_to(link, 'reason":"', '"}').replace('"',' ')
        dialog = xbmcgui.Dialog()
        dialog.ok("Delete Recording",name.upper(),text.upper())
        xbmc.executebuiltin("Container.Refresh")

	
def recordings(url):
    recs_url='http://www.filmon.com/api/dvr-list?session_key=%s'%(session_id)
    link = open_url(recs_url)
    match = re.compile('total_time":(.+?),"available_time":(.+?),"recorded_time":(.+?)}').findall(link)
    for t, a, r in match:
        acc_status = "Allowed: %shrs - Recorded: %.2fhrs - Available %.2fhrs" % (int(t)/3600, float(r)/3600, float(a)/3600)
    addLink('[COLOR cyan]'+acc_status+'[/COLOR]',"","","","","", "", "", "")
    recordings = regex_get_all(link, 'stream_url', 'isSoftDeleted')
    for r in recordings:
        STurl = regex_from_to(r, 'stream_url":"', '",').replace("\/", "/")
        STname = regex_from_to(r, 'stream_name":"', '",').replace("\/", "/")
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
        print download_link
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
            notify = "%s,%s,%s" % ('XBMC.Notification(F.T.V - Download started',name,'4000)')
            xbmc.executebuiltin(notify)
        else:
            xbmcgui.Dialog().ok('F.T.V - Download failed', name)
       

class DownloadThread(Thread):
    def __init__(self, name, url, data_path):
        self.data = url
        self.path = data_path
        Thread.__init__(self)

    def run(self):
        path = str(self.path)
        data = self.data
        urllib.urlretrieve(data, path)
        notify = "%s,%s,%s" % ('XBMC.Notification(F.T.V - Download finished',clean_file_name(name, use_blanks=False),'4000)')
        xbmc.executebuiltin(notify)	
		
def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

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
		
def renew_session():
    link = open_url(session_url)
    match= re.compile('"session_key":"(.+?)"').findall(link)
    session_id=match[0]
    if FILMON_ACCOUNT:
        login_url = "%s%s%s%s%s%s" % ("http://www.filmon.com/api/login?session_key=", session_id, "&login=", FILMON_USER, "&password=", FILMON_PASS)
        login = open_url(login_url)
        print "F.T.V......Logged in"
        xbmcgui.Window(10000).setProperty("session_id", session_id)
    else:
        print "F.T.V......Not logged in"
        xbmcgui.Window(10000).setProperty("session_id", session_id)
            
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    return session_id
          
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
        contextMenuItems.append(("TV Guide",'XBMC.Container.Update(%s?name=None&url=%s&mode=127&iconimage=%s)'%(sys.argv[0],url,iconimage)))
        if function=="grp":
            contextMenuItems.append(("Add to My Channels",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=135&iconimage=%s)'%(sys.argv[0],name,url,iconimage)))
        if function=="fav":
            contextMenuItems.append(("Remove from My Channels",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=137&iconimage=%s)'%(sys.argv[0],name,url,iconimage)))
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
        play_filmon(name, url, iconimage)
		
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

xbmcplugin.endOfDirectory(int(sys.argv[1]))

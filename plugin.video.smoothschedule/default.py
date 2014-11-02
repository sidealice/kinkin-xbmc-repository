import urllib,urllib2,re,xbmcplugin,xbmcgui,os,xbmcaddon,extract
import time,datetime
from datetime import date, timedelta
import settings
import json
from t0mm0.common.net import Net
net = Net()
import cookielib
local=xbmcaddon.Addon(id='plugin.video.smoothschedule')
SMOOTHSTREAMSADDON = xbmcaddon.Addon(id='plugin.video.mystreamstv.beta')
SS_quality=SMOOTHSTREAMSADDON.getSetting('high_def')
SS_server_type=SMOOTHSTREAMSADDON.getSetting('server_type')
SS_server=SMOOTHSTREAMSADDON.getSetting('server')
SS_service=SMOOTHSTREAMSADDON.getSetting('service')
SS_Suname=SMOOTHSTREAMSADDON.getSetting('SUserN')
SS_Spwd=SMOOTHSTREAMSADDON.getSetting('SPassW')
ENABLE_SUBS = settings.enable_subscriptions()
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.smoothschedule', 'fanart.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.smoothschedule/art', ''))
cookie_jar = settings.cookie_jar()
USER = settings.username()
PW = settings.user_password()
SS_library=xbmc.translatePath(os.path.join('special://home/addons/plugin.video.mystreamstv.beta', 'default.py'))
xml_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.smoothschedule'), 'smooth_epg.xml')
xml_url='http://cdn.smoothstreams.tv/schedule/feed.xml'
m3u_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.smoothschedule'), 'smooth.m3u')
logo_archive = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.smoothschedule/art', 'pvrlogos.zip'))
logo_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.smoothschedule'), '')

TIMEZONE = settings.timezone()

i = datetime.datetime.now()
t0 = i.strftime('%Y-%m-%d')
t0time = i.strftime('%H:%M')
t1 = (i + timedelta(days=1)).strftime('%Y-%m-%d')
t2 = (i + timedelta(days=2)).strftime('%Y-%m-%d')
t3 = (i + timedelta(days=3)).strftime('%Y-%m-%d')
t4 = (i + timedelta(days=4)).strftime('%Y-%m-%d')
t5 = (i + timedelta(days=5)).strftime('%Y-%m-%d')

if not os.path.exists(os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.smoothschedule'), 'pvrlogos')): extract.all(logo_archive,logo_path)

def GET_URL(url):
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Host'] = 'smoothstreams.tv'
    header_dict['Referer'] = 'http://starstreams.tv/'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0'
    net.set_cookies(cookie_jar)
    req = net.http_GET(url, headers=header_dict).content.rstrip()
    net.save_cookies(cookie_jar)
    return req

def login():
    header_dict = {}
    header_dict['Accept'] = '	text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Host'] = 'starstreams.tv'
    header_dict['Referer'] = 'http://starstreams.tv/wp-login.php?loggedout=true'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Connection'] = 'keep-alive'
    form_data = ({'username': USER, 'password': PW,'remember_me': '1','protect_login': 'Log+in'})	
    net.set_cookies(cookie_jar)
    login = net.http_POST('http://starstreams.tv/wp-login.php?loggedout=true', form_data=form_data, headers=header_dict).content
    if USER in login and USER !='':
        notification('Smooth Schedule', 'Logged in to Smoothstreams', '3000', xbmc.translatePath(os.path.join('special://home/addons/plugin.video.smoothschedule', 'icon.png')))
    net.save_cookies(cookie_jar)

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def main_menu():
    addDir('Create m3u playlist for IPTV Simple PVR','0',50,"")
    addDir('PVR Help','0',51,"")
    addDir('Channels','http://smoothstreams.tv/schedule/?cat=0&js=1&timezone=%s&hours=6' % TIMEZONE,5,xbmc.translatePath(os.path.join(art, 'channels.png')))
    addDir('All','0',3,xbmc.translatePath(os.path.join(art, 'allsports.png')))
    addDir('Football','24',3,xbmc.translatePath(os.path.join(art, 'football.png')))
    addDir('American Football','13',3,xbmc.translatePath(os.path.join(art, 'americanfootball.png')))
    addDir('-NCAAF','57',3,xbmc.translatePath(os.path.join(art, 'americanfootball.png')))
    addDir('-NFL','56',3,xbmc.translatePath(os.path.join(art, 'americanfootball.png')))
    addDir('Baseball','41',3,xbmc.translatePath(os.path.join(art, 'baseball.png')))
    addDir('Basketball','15',3,xbmc.translatePath(os.path.join(art, 'basketball.png')))
    addDir('-NBA','26',3,xbmc.translatePath(os.path.join(art, 'basketball.png')))
    addDir('-NCAAB','37',3,xbmc.translatePath(os.path.join(art, 'basketball.png')))
    addDir('Boxing & MMA','28',3,xbmc.translatePath(os.path.join(art, 'boxing_mma.png')))
    addDir('Cricket','42',3,xbmc.translatePath(os.path.join(art, 'cricket.png')))
    addDir('Golf','18',3,xbmc.translatePath(os.path.join(art, 'golf.png')))
    addDir('Ice Hockey','40',3,xbmc.translatePath(os.path.join(art, 'icehockey.png')))
    addDir('Motor Sports','46',3,xbmc.translatePath(os.path.join(art, 'motorsports.png')))
    addDir('-Formula 1','47',3,xbmc.translatePath(os.path.join(art, 'motorsports.png')))
    addDir('-Nascar','48',3,xbmc.translatePath(os.path.join(art, 'motorsports.png')))
    addDir('Olympics','21',3,xbmc.translatePath(os.path.join(art, 'olympics.png')))
    addDir('Other Sports','43',3,xbmc.translatePath(os.path.join(art, 'othersports.png')))
    addDir('Rugby','38',3,xbmc.translatePath(os.path.join(art, 'rugby.png')))
    addDir('Tennis','44',3,xbmc.translatePath(os.path.join(art, 'tennis.png')))
    addDir('TV Shows','45',3,xbmc.translatePath(os.path.join(art, 'tvshows.png')))
    addDir('-General TV','58',3,xbmc.translatePath(os.path.join(art, 'tvshows.png')))
    addDir('Wrestling','39',3,xbmc.translatePath(os.path.join(art, 'wrestling.gif')))
	
def channels(name,url,iconimage):
    link =GET_URL(url).encode('utf-8','ignore').replace("'", '"').replace("|", '<>')
    all_ch = regex_get_all(link, '<ul class="row">', '</ul>')
    for a in all_ch:
        all_li = regex_get_all(a, '<li', '</li>')
        ch_id = regex_from_to(all_li[0], '<span>', '</span>')
        iconimage = 'http://smoothstreams.tv/schedule/' + regex_from_to(all_li[0], '<img src="', '"')
        alt = regex_from_to(all_li[0], 'alt="', '"')
        if 'background' in all_li[1]:
            title = regex_from_to(all_li[1], 'data-name="', '"')
        else:
            title = ""
        url = str("plugin://plugin.video.mystreamstv.beta/?path=/root/channels/&action=play_channel&chan=%s" % (ch_id))
        name = "%s [COLOR gold]%s[/COLOR]" % (alt, title)
        addDirPlayable(name,url,2,iconimage)

def CATEGORIES(name,url,iconimage):
    addDir(t0,'http://smoothstreams.tv/schedule/list.php?cat=%s&js=1&timezone=%s&day=%s&auto=null' % (url,TIMEZONE, t0),1,iconimage)
    addDir(t1,'http://smoothstreams.tv/schedule/list.php?cat=%s&js=1&timezone=%s&day=%s&auto=null' % (url,TIMEZONE, t1),1,iconimage)
    addDir(t2,'http://smoothstreams.tv/schedule/list.php?cat=%s&js=1&timezone=%s&day=%s&auto=null' % (url,TIMEZONE, t2),1,iconimage)
    addDir(t3,'http://smoothstreams.tv/schedule/list.php?cat=%s&js=1&timezone=%s&day=%s&auto=null' % (url,TIMEZONE, t3),1,iconimage)
    addDir(t4,'http://smoothstreams.tv/schedule/list.php?cat=%s&js=1&timezone=%s&day=%s&auto=null' % (url,TIMEZONE, t4),1,iconimage)
    addDir(t5,'http://smoothstreams.tv/schedule/list.php?cat=%s&js=1&timezone=%s&day=%s&auto=null' % (url,TIMEZONE, t5),1,iconimage)
		
def listings(name, url):
    link =GET_URL(url).encode('utf-8','ignore').replace("'", '"').replace("|", '<>')
    match = re.compile('<li class=(.+?) style="color:(.+?)">(.+?) <> <i>(.+?)</i> <> (.+?)</li>').findall(link)
    for cl,color,dttime,channel,title in match:
        endtime = dttime[11:]
        starttime = dttime[5:10]
        if not '<i>' in title:
            chan = channel.replace('#','').replace('|','')
            title = "%s | [COLOR gold]%s[/COLOR] | [COLOR cyan]%s[/COLOR]" % (dttime[5:], chan, title)
            chan = channel.replace('#','').replace('|','')
            url = str("plugin://plugin.video.mystreamstv.beta/?path=/root/channels/&action=play_channel&chan=%s" % (chan))
            if name != t0 or(name == t0 and (endtime > t0time or endtime < starttime)):
                addDirPlayable(title,url,2,iconimage)
        if '<i>' in title:
            ch = regex_from_to(title, '<i>', '</i>')
            title1 = title.split('<i>')[0]
            all_ch = ch.split(' ; ')
            for a in all_ch:
                chan = a.replace('(','')[:2]
                if a[:1] == '(':
                    a = a[1:]
                title = "%s | [COLOR gold]%s[/COLOR] | [COLOR cyan]%s[/COLOR]" % (dttime[5:], a.replace('#','').replace('))',')'), title1)
                url = str("plugin://plugin.video.mystreamstv.beta/?path=/root/channels/&action=play_channel&chan=%s" % (chan))
                if name != t0 or(name == t0 and (endtime > t0time or endtime < starttime)):
                    addDirPlayable(title,url,2,iconimage)

def write():
    mystreams=read_from_file(SS_library)
    pl_name=regex_from_to(mystreams,'plugin = "', '"')
    pl_version=regex_from_to(mystreams,'version = "', '"')
    ua='|User-Agent=SmoothStreams.tv+Beta-' + pl_version

    if SS_server=='0':
        server="dEU.SmoothStreams.tv"
    elif SS_server=='1':
        server="d88.SmoothStreams.tv"
    elif SS_server=='2':
        server="d11.SmoothStreams.tv"
    elif SS_server=='3':
        server="dNAE.SmoothStreams.tv"
    elif SS_server=='4':
        server="dNAW.SmoothStreams.tv"
    elif SS_server=='5':
        server="dNA.SmoothStreams.tv"
    elif SS_server=='6':
        server="dSG.SmoothStreams.tv"
	
    if SS_quality == "true":
        quality = "q1"
    else:
        quality = "q2"
    if SS_server_type == "0":
        if SS_service == "1":
            stream_port = "2935"
        elif SS_service in ["0"]:
            stream_port = "29350"
        elif SS_service == "2":
            stream_port = "3935"
        elif SS_service == "3":
            stream_port = "5540"
    else:
        if SS_service == "1":
            stream_port = "12935"
        elif SS_service in ["0"]:
            stream_port = "29355"
        elif SS_service == "2":
            stream_port = "39355"
        elif SS_service == "3":
            stream_port = "5545"

    urllib.urlretrieve(xml_url, xml_path)
    #Write M3U
    write_to_file(m3u_path, '#EXTM3U tvg-shift=3\n', False)
    link=read_from_file(xml_path)
    all_ch = regex_get_all(link, '<channel', '</channel>')
    for a in all_ch:
        ch_id = regex_from_to(a, 'id="', '"')
        ch_name = regex_from_to(a, 'display-name>', '</display-name>')
        ch_num=ch_name.split(' - ')[0]
        ch_title=ch_name.split(' - ')[1]
        if SS_server_type == "0":
            write_to_file(m3u_path, '#EXTINF:-1 tvg-id="%s" tvg-name="%s" tvg-logo="%s.png" group-title="Smoothstreams",%s\nrtmp://%s:%s/view?u=%s&p=%s/ch%s%s.stream\n' % (ch_id,ch_name,ch_name,ch_title,server,stream_port,SS_Suname,SS_Spwd,ch_num,quality), True)
        else:
            write_to_file(m3u_path, '#EXTINF:-1 tvg-id="%s" tvg-name="%s" tvg-logo="%s.png" group-title="Smoothstreams",%s\nhttp://%s:%s/view/ch%s%s.stream/playlist.m3u8?u=%s&p=%s%s\n' % (ch_id,ch_name,ch_name,ch_title,server,stream_port,ch_num,quality,SS_Suname,SS_Spwd,ua), True)
    local.setSetting('service_time', str(datetime.datetime.now() + timedelta(hours=2)).split('.')[0])
	
def help(text): header="[B][COLOR red]"+text+"[/B][/COLOR]"; msg=os.path.join(local.getAddonInfo('path'),'resources','textbox','help.txt'); TextBoxes(header,msg)

def TextBoxes(heading,anounce):
        class TextBox():
            """Thanks to BSTRDMKR for this code:)"""
            WINDOW=10147; CONTROL_LABEL=1; CONTROL_TEXTBOX=5 # constants
            def __init__(self,*args,**kwargs):
                xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW,)) # activate the text viewer window
                self.win=xbmcgui.Window(self.WINDOW) # get window
                xbmc.sleep(500) # give window time to initialize
                self.setControls()
            def setControls(self):
                self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
                try: f=open(anounce); text=f.read()
                except: text=anounce
                self.win.getControl(self.CONTROL_TEXTBOX).setText(text); return
        TextBox()
		
def write_to_file(path, content, append, silent=False):
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
		
def run_smooth(name, url, iconimage):
    print "URL IS " + url
    xbmc.Player().play(url)
	
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
    r = re.search("(?i)" + f + "(<i>\S\s</i>+?)" + t, r).group(1)
    return r
    

	
def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
		
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


def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', audio_fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirPlayable(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
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
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
    try:
        login()
    except:
        pass
    main_menu()
       
elif mode==1:
    listings(name, url)
	
elif mode == 2:
    run_smooth(name, url, iconimage)
	
elif mode==3:
    CATEGORIES(name,url,iconimage)
	
elif mode==5:
    channels(name,url,iconimage)
	
elif mode==50:
    write()
	
elif mode==51:
    help(name)
		

		

xbmcplugin.endOfDirectory(int(sys.argv[1]))

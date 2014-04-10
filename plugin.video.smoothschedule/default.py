import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import time,datetime
from datetime import date, timedelta
import settings
import json

fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.smoothschedule', 'fanart.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.smoothschedule/art', ''))


TIMEZONE = settings.timezone()

i = datetime.datetime.now()
t0 = i.strftime('%Y-%m-%d')
t0time = i.strftime('%H:%M')
t1 = (i + timedelta(days=1)).strftime('%Y-%m-%d')
t2 = (i + timedelta(days=2)).strftime('%Y-%m-%d')
t3 = (i + timedelta(days=3)).strftime('%Y-%m-%d')
t4 = (i + timedelta(days=4)).strftime('%Y-%m-%d')
t5 = (i + timedelta(days=5)).strftime('%Y-%m-%d')


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def main_menu():
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
    link =open_url(url).replace("'", '"').replace("|", '<>')
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
'''
        endtime = dttime[11:]
        starttime = dttime[5:10]
        if not '<i>' in title:
            chan = channel.replace('#','').replace('|','')
            title = "[COLOR gold]%s[/COLOR] | [COLOR cyan]%s[/COLOR] | %s" % (chan, title, dttime[5:])
            chan = channel.replace('#','').replace('|','')
            url = str("plugin://plugin.video.mystreamstv.beta/?path=/root/channels/&action=play_channel&chan=%s" % (chan))
            if (endtime > t0time or endtime < starttime) and starttime < t0time:
                addDirPlayable(title,url,2,iconimage)
            else:
                addDirPlayable(channel,url,2,iconimage)
        if '<i>' in title:
            ch = regex_from_to(title, '<i>', '</i>')
            title1 = title.split('<i>')[0]
            all_ch = ch.split(' ; ')
            for a in all_ch:
                chan = a.replace('(','')[:2]
                if a[:1] == '(':
                    a = a[1:]
                title = "[COLOR gold]%s[/COLOR] | [COLOR cyan]%s[/COLOR] | %s" % (a.replace('#','').replace('))',')'), title1, dttime[5:])
                url = str("plugin://plugin.video.mystreamstv.beta/?path=/root/channels/&action=play_channel&chan=%s" % (chan))
                if (endtime > t0time or endtime < starttime) and starttime < t0time:
                    addDirPlayable(title,url,2,iconimage)
                else:
                    addDirPlayable(channel,url,2,iconimage)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
'''
def CATEGORIES(name,url,iconimage):
    addDir(t0,'http://smoothstreams.tv/schedule/list.php?cat=%s&js=1&timezone=%s&day=%s&auto=null' % (url,TIMEZONE, t0),1,iconimage)
    addDir(t1,'http://smoothstreams.tv/schedule/list.php?cat=%s&js=1&timezone=%s&day=%s&auto=null' % (url,TIMEZONE, t1),1,iconimage)
    addDir(t2,'http://smoothstreams.tv/schedule/list.php?cat=%s&js=1&timezone=%s&day=%s&auto=null' % (url,TIMEZONE, t2),1,iconimage)
    addDir(t3,'http://smoothstreams.tv/schedule/list.php?cat=%s&js=1&timezone=%s&day=%s&auto=null' % (url,TIMEZONE, t3),1,iconimage)
    addDir(t4,'http://smoothstreams.tv/schedule/list.php?cat=%s&js=1&timezone=%s&day=%s&auto=null' % (url,TIMEZONE, t4),1,iconimage)
    addDir(t5,'http://smoothstreams.tv/schedule/list.php?cat=%s&js=1&timezone=%s&day=%s&auto=null' % (url,TIMEZONE, t5),1,iconimage)
		
def listings(name, url):
    link =open_url(url).replace("'", '"').replace("|", '<>')
    print link
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
    main_menu()
       
elif mode==1:
    listings(name, url)
	
elif mode == 2:
    run_smooth(name, url, iconimage)
	
elif mode==3:
    CATEGORIES(name,url,iconimage)
	
elif mode==5:
    channels(name,url,iconimage)
		

		

xbmcplugin.endOfDirectory(int(sys.argv[1]))

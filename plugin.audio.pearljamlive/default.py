import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import plugintools

pearljam_url = 'http://www.pearljamlive.com/'
pjbootlegs_url = 'http://www.pearljambootlegs.org/modules/jinzora2/'
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.pearljamlive', 'fanart.jpg'))
pjbootleg_logo = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.pearljamlive/art', 'pjbootleglogo.gif'))
pjbootleg_fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.pearljamlive/art', 'fanart2.jpg'))
audio_fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.pearljamlive/art', 'fanart1.jpg'))
radiothumb = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.pearljamlive/art', 'pjradio.jpg'))
radiofanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.pearljamlive/art', 'radiofanart.jpg'))

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
def CATEGORIES():
        addDir('Pearl Jam Live',pearljam_url,1,'http://www.pearljamlive.com/images/polaroid_home.jpg')
        addDir( 'Pearl Jam Bootlegs','url',4,pjbootleg_logo)
        addDir( 'Pearl Jam Official YouTube','http://gdata.youtube.com/feeds/api/users/PearlJamOfficial/uploads?start-index=1&max-results=20',12,pjbootleg_logo)
        addDirAudio('Pearl Jam Radio','http://radio.nugs.net:8080/',13,radiothumb)#http://tunein.com/radio/Pearl-Jam-Radio-s124658/

#########################  PEARL JAM	#################################################	
def LISTEN_YEAR(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" target="content">(.+?)</a>').findall(link)
        for url,year in match:
            thumb = 'http://www.pearljamlive.com/images/polaroid_%s.jpg' % year# pearljam_url + 'images/pic_' + str(year) + '.jpg'
            if len(year)==4:
                addDir(year + ' Bootlegs',pearljam_url+url,2,thumb)
				
def CONCERT_LIST(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=re.sub('\s+',' ',response.read())
        response.close()
        thumb = pearljam_url + regex_from_to(link, '<img border="0" src="', '"')
        all_shows = regex_from_to(link,'<table border="0" cellpadding="5" cellspacing="0"', '</table>')
        all_td = regex_get_all(all_shows, '<tr>', '</tr>')
        for a in all_td:
            td = regex_get_all(a, '<td', '</td>')
            showdate = regex_from_to(td[0], '">', '<')
            title = regex_from_to(td[1], '>', '<')
            urldata = regex_from_to(td[3], 'data-item="', '"')
            url1 = pearljam_url + 'playlists/' + urldata + '.xml'
            print url1
            name = "%s - %s" % (showdate,title)
            addDir(name,url1,3,thumb)

def AUDIOLINKS(url,name,clear):
        iconimage=""
        dialog = xbmcgui.Dialog()
        show_name=name
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('path="(.+?)" title="(.+?)"').findall(link)
        playlist=[]
        nItem=len(match)
        year = url[38:42]
        if dialog.yesno("Pearl Jam Live", 'Browse songs or play full album?', '', '', 'Play Now','Browse'):
            pl = get_XBMCPlaylist(clear)
            for url,name in match:
                url1=pearljam_url + str(url)
                thumb = pearljam_url + 'images/pic_' + str(year) + '.jpg'
                addLink(name,url1,thumb)
                liz=xbmcgui.ListItem(show_name, iconImage=thumb, thumbnailImage=iconimage)
                liz.setInfo('music', {'Title':name, 'Artist':'Pearl Jam ' + str(year), 'Album':show_name})
                liz.setProperty('mimetype', 'audio/mpeg')
                liz.setProperty('fanart_image', fanart)
                liz.setThumbnailImage(thumb)
                playlist.append((url1, liz))
                
        else:
            dp = xbmcgui.DialogProgress()
            dp.create("Pearl Jam Live",'Creating Your Playlist')
            dp.update(0)
            pl = get_XBMCPlaylist(clear)
            for url,name in match:
                url1=pearljam_url + str(url)
                thumb = pearljam_url + 'images/pic_' + str(year) + '.jpg'
                addLink(name,url1,thumb)
                liz=xbmcgui.ListItem(show_name, iconImage=thumb, thumbnailImage=iconimage)
                liz.setInfo('music', {'Title':name, 'Artist':'Pearl Jam ' + str(year), 'Album':show_name})
                liz.setProperty('mimetype', 'audio/mpeg')
                liz.setThumbnailImage(thumb)
                liz.setProperty('fanart_image', fanart)
                playlist.append((url1, liz))

                progress = len(playlist) / float(nItem) * 100               
                dp.update(int(progress), 'Adding to Your Playlist',show_name)
                if dp.iscanceled():
                    return

            print 'THIS IS PLAYLIST====   '+str(playlist)
    
            for blob ,liz in playlist:
                try:
                    if blob:
                        pl.add(blob,liz)
                except:
                    pass
            if clear or (not xbmc.Player().isPlayingAudio()):
                xbmc.Player().play(pl)
################################Peal Jam Bootlegs#####################################				

def PJB_MAIN(url):
        addDir( 'New Shows',pjbootlegs_url,5,pjbootleg_logo)
        addDir( 'Top Downloaded Shows',pjbootlegs_url,6,pjbootleg_logo)
        addDir( 'Top Played Shows',pjbootlegs_url,7,pjbootleg_logo)
        addDir( 'Shows by Year',pjbootlegs_url,8,pjbootleg_logo)

def PJB_NEW(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('"openPopup(.+?)</td>').findall(link)
        show=re.compile('openMediaPlayer(.+?)title="(.+?)" alt=(.+?)href="(.+?)">').findall(match[0])
        for dummy,title,info,pjb_url in show:
            addDir(title,pjbootlegs_url+pjb_url,9,pjbootleg_logo)

def PJB_TOP_DL(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('"openPopup(.+?)</td>').findall(link)
        show=re.compile('openMediaPlayer(.+?)title="(.+?)" alt=(.+?)href="(.+?)">').findall(match[1])
        for dummy,title,info,pjb_url in show:
            addDir(title,pjbootlegs_url+pjb_url,9,pjbootleg_logo)

def PJB_TOP_PL(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('"openPopup(.+?)</td>').findall(link)
        show=re.compile('openMediaPlayer(.+?)title="(.+?)" alt=(.+?)href="(.+?)">').findall(match[2])
        for dummy,title,info,pjb_url in show:
            addDir(title,pjbootlegs_url+pjb_url,9,pjbootleg_logo)
			
def PJB_YEAR(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" title="Browse: (.+?)"').findall(link)
        for year_url,name in match:
            addDir(name,pjbootlegs_url+year_url,11,pjbootleg_logo)
			
def PJB_YEAR_SHOWS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" title="Browse: (.+?)"').findall(link)
        for show_url,name in match:
            addDir(name,pjbootlegs_url+show_url,9,pjbootleg_logo)

def PJB_AUDIOLINKS(url,name,clear):
        iconimage=""
        dialog = xbmcgui.Dialog()
        show_name=name
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #match=re.compile('title="Download: (.+?)" href="(.+?)"><img src="style/cms-theme/download.gif" border=0 alt="Download"').findall(link)
        match=re.compile('Download: (.+?)" href="(.+?)"><img src="style/cms-theme/download.gif" border=0 alt="Download" title="Download">').findall(link)
        playlist=[]
        nItem=len(match)
        if dialog.yesno("Pearl Jam Live", 'Browse songs or play full album?', '', '', 'Play Now','Browse'):
            pl = get_XBMCPlaylist(clear)
            for name,url in match:
                url1=pjbootlegs_url + str(url)
                thumb = pjbootleg_logo
                addDirAudio(name,url1,10,thumb)
                liz=xbmcgui.ListItem(show_name, iconImage=thumb, thumbnailImage=iconimage)
                liz.setInfo('music', {'Title':name, 'Artist':'Pearl Jam', 'Album':show_name})
                liz.setProperty('mimetype', 'audio/mpeg')
                liz.setThumbnailImage(thumb)
                liz.setProperty('fanart_image', audio_fanart)
                playlist.append((url1, liz))
                
        else:
            dp = xbmcgui.DialogProgress()
            dp.create("Pearl Jam Live",'Creating Your Playlist')
            dp.update(0)
            pl = get_XBMCPlaylist(clear)
            for name,url in match:
                url1=pjbootlegs_url + str(url)
                thumb = pjbootleg_logo
                addDirAudio(name,url1,10,thumb)
                liz=xbmcgui.ListItem(show_name, iconImage=thumb, thumbnailImage=iconimage)
                liz.setInfo('music', {'Title':name, 'Artist':'Pearl Jam', 'Album':show_name})
                liz.setProperty('mimetype', 'audio/mpeg')
                liz.setThumbnailImage(thumb)
                liz.setProperty('fanart_image', audio_fanart)
                playlist.append((url1, liz))

                progress = len(playlist) / float(nItem) * 100               
                dp.update(int(progress), 'Adding to Your Playlist',show_name)
                if dp.iscanceled():
                    return

            print 'THIS IS PLAYLIST====   '+str(playlist)
    
            for blob ,liz in playlist:
                try:
                    if blob:
                        pl.add(blob,liz)
                except:
                    pass
            if clear or (not xbmc.Player().isPlayingAudio()):
                xbmc.Player().play(pl)

def PJB_SINGLELINKS(url,name,clear):
        iconimage=""
        dialog = xbmcgui.Dialog()
        show_name=name
        playlist=[]
        pl = get_XBMCPlaylist(clear)
        #pl=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        url1=str(url)
        thumb = ''
        liz=xbmcgui.ListItem(show_name, iconImage=thumb, thumbnailImage=iconimage)
        liz.setInfo('music', {'Title':name, 'Artist':'Pearl Jam', 'Album':show_name})
        liz.setProperty('mimetype', 'audio/mpeg')
        liz.setThumbnailImage(thumb)
        liz.setProperty('fanart_image', fanart)
        #pl.clear()
        playlist.append((url1, liz))
        for blob ,liz in playlist:
            try:
                if blob:
                    pl.add(blob,liz)
            except:
                pass
        if clear or (not xbmc.Player().isPlayingAudio()):
            xbmc.Player().play(pl)

def YOUTUBE_CHANNELS(url):
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

    addDir(">> Next page",next_page_url,12,"")

def pj_radio(url):
    iconimage = radiothumb
    playlist = []
    pl = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    pl.clear()
    link = open_url(url)
    liz=xbmcgui.ListItem('Pearl Jam Radio', iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo('music', {'Title':'Pearl Jam Radio', 'Artist':'Pearl Jam', 'Album':'Continuous stream'})
    liz.setProperty('mimetype', 'audio/mpeg')
    liz.setThumbnailImage(iconimage)
    liz.setProperty('fanart_image', radiofanart)
    playlist.append((url, liz))
    for blob ,liz in playlist:
        try:
            if blob:
                pl.add(blob,liz)
        except:
            pass
    xbmc.Player().play(pl)	

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

############################################################################################
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


def get_XBMCPlaylist(clear):
    pl=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    if clear:
        pl.clear()
    return pl

    dialog = xbmcgui.Dialog()
    if dialog.yesno("Pearl Jam Live", 'Queue album or play now?', '', '', 'Play Now','Queue') == 0:
        pl.clear()
    return pl

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', audio_fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        if mode>3:
            liz.setProperty('fanart_image', pjbootleg_fanart)
        else:
            liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirAudio(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        if mode==13:
            liz.setProperty('fanart_image', radiofanart)
        else:
            liz.setProperty('fanart_image', audio_fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

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

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        LISTEN_YEAR(url)
		
elif mode==2:
        print ""+url
        CONCERT_LIST(url)
        
elif mode==3:
        print ""+url
        AUDIOLINKS(url,name,True)
		
elif mode==4:
        print ""+url
        PJB_MAIN(url)
		
elif mode==5:
        print ""+url
        PJB_NEW(url)

elif mode==6:
        print ""+url
        PJB_TOP_DL(url)
		
elif mode==7:
        print ""+url
        PJB_TOP_PL(url)
		
elif mode==8:
        print ""+url
        PJB_YEAR(url)
	
elif mode==9:
        print ""+url
        PJB_AUDIOLINKS(url,name,True)
		
elif mode==10:
        print ""+url
        PJB_SINGLELINKS(url,name,True)
		
elif mode==11:
        print ""+url
        PJB_YEAR_SHOWS(url)
		
elif mode==12:
        YOUTUBE_CHANNELS(url)
		
elif mode==13:
        pj_radio(url)
		

xbmcplugin.endOfDirectory(int(sys.argv[1]))

import urllib,urllib2,re,xbmcplugin,xbmcgui,os

pearljam_url = 'http://www.pearljamlive.com/'
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.pearljamlive', 'fanart.jpg'))

def CATEGORIES():
        addDir('Pearl Jam Live',pearljam_url,1,'http://www.pearljamlive.com/images/pic_home.jpg')
        addDir( '','',1,'')

#########################  PEARL JAM	#################################################	
def LISTEN_YEAR(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('href="loading(.+?)" title="(.+?)"').findall(link)
        for url,name in match:
            year=name.replace(' Pearl Jam Bootlegs', '')
            thumb = pearljam_url + 'images/pic_' + str(year) + '.jpg'
            if name.endswith("Bootlegs"):
                addDir(name,pearljam_url+'interior'+url,2,thumb)
				
def CONCERT_LIST(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=re.sub('\s+',' ',response.read())
        response.close()
        match=re.compile('<td width="100">(.+?)</td> <td width="350">(.+?)</td>').findall(link)
        year=re.compile('src="images/pic_(.+?).jpg"').findall(link)
        year=str(year).replace("['","").replace("']","")
        dp = xbmcgui.DialogProgress()
        dp.create("Pearl Jam Live",'Fetching concerts')
        dp.update(0)
        nItem=len(match)
        for url,name in match:
            url1 = pearljam_url + 'playlists/' + year + url.replace('January ', '01').replace('January ', '01').replace('February ', '02').replace('March ', '03').replace('April ', '04').replace('May ', '05').replace('June ', '06').replace('July ', '07').replace('August ', '08').replace('September ', '09').replace('October ', '10').replace('November ', '11').replace('December ', '12') + '.xml'
            thumb = pearljam_url + 'images/pic_' + str(year) + '.jpg'
            progress = len(url1) / float(nItem) * 100               
            dp.update(int(progress), 'Grabbing shows',str(year))
            if dp.iscanceled():
                return
            addDir(url + ' - ' + name,url1,3,thumb)

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
########################################################################################				
  


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
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
		

xbmcplugin.endOfDirectory(int(sys.argv[1]))

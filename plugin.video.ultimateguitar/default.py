import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys,datetime
import plugintools
import settings

DATA_PATH = settings.data_path()
ADDON = settings.addon()
WATCHED_FILE = settings.watched_lessons_file()
FAVOURITES_FILE = settings.favourite_songs_file()

justin_url = 'http://www.justinguitar.com/'
youtube_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s'
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.ultimateguitar', 'fanart.jpg'))
pjbootleg_logo = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.ultimateguitar/art', 'pjbootleglogo.gif'))
pjbootleg_fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.ultimateguitar', 'fanart.jpg'))
audio_fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.ultimateguitar', 'fanart.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.ultimateguitar/art', ''))

if ADDON.getSetting('visitor_ga')=='':
    from random import randint
    ADDON.setSetting('visitor_ga',str(randint(0, 0x7fffffff)))
    
PATH = "XBMC_ULTIMATEGUITAR"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK = "UA-39563241-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.0" #<---- PLUGIN VERSION

###....................G.A...............................................###


def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


def checkGA():

    secsInHour = 60 * 60
    threshold  = 2 * secsInHour

    now   = datetime.datetime.today()
    prev  = parseDate(ADDON.getSetting('ga_time'))
    delta = now - prev
    nDays = delta.days
    nSecs = delta.seconds

    doUpdate = (nDays > 0) or (nSecs > threshold)
    if not doUpdate:
        return

    ADDON.setSetting('ga_time', str(now).split('.')[0])
    APP_LAUNCH()    
    
                    
def send_request_to_google_analytics(utm_url):
    ua='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':ua}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = ADDON.getSetting('visitor_ga')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if not group=="None":
                    utm_track = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmt=" + "event" + \
                            "&utme="+ quote("5("+PATH+"*"+group+"*"+name+")")+\
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
                    try:
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
            if name=="None":
                    utm_url = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
            else:
                if group=="None":
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                else:
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
def APP_LAUNCH():
        versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
        if versionNumber < 12:
            if xbmc.getCondVisibility('system.platform.osx'):
                if xbmc.getCondVisibility('system.platform.atv2'):
                    log_path = '/var/mobile/Library/Preferences'
                else:
                    log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
            elif xbmc.getCondVisibility('system.platform.ios'):
                log_path = '/var/mobile/Library/Preferences'
            elif xbmc.getCondVisibility('system.platform.windows'):
                log_path = xbmc.translatePath('special://home')
                log = os.path.join(log_path, 'xbmc.log')
                logfile = open(log, 'r').read()
            elif xbmc.getCondVisibility('system.platform.linux'):
                log_path = xbmc.translatePath('special://home/temp')
            else:
                log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        elif versionNumber > 11:
            print '======================= more than ===================='
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        else:
            logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        print '==========================   '+PATH+' '+VERSION+'  =========================='
        try:
            from hashlib import md5
        except:
            from md5 import md5
        from random import randint
        import time
        from urllib import unquote, quote
        from os import environ
        from hashlib import sha1
        import platform
        VISITOR = ADDON.getSetting('visitor_ga')
        for build, PLATFORM in match:
            if re.search('12',build[0:2],re.IGNORECASE): 
                build="Frodo" 
            if re.search('11',build[0:2],re.IGNORECASE): 
                build="Eden" 
            if re.search('13',build[0:2],re.IGNORECASE): 
                build="Gotham" 
            print build
            print PLATFORM
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + VERSION + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+build+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 
checkGA()

###..................end G>A.............................................###

def CATEGORIES():
        addDir('Lessons - JustinGuitar','url',11,art + 'lessons.png')
        addDir('Songs etc. - JustinGuitar','url',12,art + 'songs.png')
        addDir('YouTube Channels','url',15,art + 'youtubemain.png')
        addDir('Favourites','url',14,art + 'favourites.png')

		
def YOUTUBE_LIST():
        channel="justinsandercoesongs"
        addDir("Justin Sandercoe",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art + 'youtubejs.png')
        channel="martyzsongs"
        addDir("Marty Schwartz",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art + 'youtubems.png')
        channel="rockongoodpeople"
        addDir("Next Level Guitar",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art + 'youtubenlg.png')
        channel="youcanlearnguitar"
        addDir("You Can Learn Guitar",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art + 'youtubeyclg.png')
        channel="guitarings"
        addDir("Guitarings",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art + 'youtubegr.png')
        channel="GaragebandandBeyond"
        addDir("GarageBand & Beyond",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art + 'youtubegb.png')
        channel="wickedwkd"
        addDir("Pearl Jam covers by wickedwkd",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art + 'pjcovers.png')

		
def LESSON_DIR():
        addDir('Beginners Course',justin_url + 'en/BC-000-BeginnersCourse.php',1,art + 'jsbeginners.png')
        addDir('Intermediate Course',justin_url + 'en/IM-000-IntermediateMethod.php',1,art + 'jsintermediate.png')
        addDir('The Basics',justin_url + 'en/TB-000-TheBasics.php',1,art + 'jsbasics.png')
        addDir('Practice',justin_url + 'en/PC-000-Practice.php',1,art + 'jspractice.png')
        addDir('Technique',justin_url + 'en/TE-000-Technique.php',1,art + 'jstechnique.png')
        addDir('Chords',justin_url + 'en/CH-000-Chords.php',1,art + 'jschords.png')
        addDir('Rhythm Guitar',justin_url + 'en/RH-000-RhythmGuitar.php',1,art + 'jsrhythm.png')
        addDir('Scales',justin_url + 'en/SC-000-Scales.php',1,art + 'jsscales.png')
        addDir('Arpeggios',justin_url + 'en/AR-000-Arpeggios.php',1,art + 'jsarpeggios.png')
        addDir('Aural Training',justin_url + 'en/AU-000-AuralTraining.php',1,art + 'jsaural.png')
        addDir('Gear and Reviews',justin_url + 'en/GG-000-GuitarGear.php',1,art + 'jsgear.png')
        #addDir('Recording Techniques',justin_url + 'en/RT-000-RecordingTechniques.php',1,art + 'jsbeginners.png')
        #addDir('Masterclasses',justin_url + 'en/MA-000-Masterclasses.php',1,art + 'jsbeginners.png')
		
def SONG_DIR():
        addDir('Beginners Songs',justin_url + 'en//BS-000-BeginnersSongbook.php',1,art + 'jsbeginners.png')
        addDir('Intermediate Songs',justin_url + 'en/SB-000-GuitarSongBook.php',1,art + 'jsintermediate.png')
        addDir('Other Songs',justin_url + 'en/ST-000-SongsTAB.php',1,art + 'jsother.png')
        addDir('Awesome Riffs',justin_url + 'en/RF-000-GuitarRiffs.php',1,art + 'jsriffs.png')
        addDir('Awesome Licks',justin_url + 'en/LK-000-GuitarLicks.php',1,art + 'jslicks.png')
        addDir('Classic Solos',justin_url + 'en/CS-000-ClassicGuitarSolos.php',1,art + 'jssolos.png')
        addDir('Transcribing',justin_url + 'en/TR-000-Transcribing.php',1,art + 'jstranscribing.png')
        addDir('Blues (Lead and Rhythm)',justin_url + 'en/BL-000-Blues.php',1,art + 'jsblues.png')
        addDir('Folk (Fingerstyle)',justin_url + 'en/FO-000-Folk.php',1,art + 'jsfolk.png')
        addDir('Rock and Metal',justin_url + 'en/RO-000-RockMetal.php',1,art + 'jsrock.png')
        addDir('Jazz',justin_url + 'en/JA-000-Jazz.php',1,art + 'jsjazz.png')

#########################  PEARL JAM	#################################################	
def LESSON_LIST(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)">(.+?)</a><br />').findall(link)
        for url,name in match:
            if name.find('Songs')>0:
                name='[COLOR cyan]' + name + ' (see Songs section)' + '[/COLOR]'
            name=name.replace("&amp;","&").replace("&quot;","'")
            prefix=u'\u2714'.encode('utf-8')#U+2714
            url='en/' + (url.replace('http://justinguitar.com/en','').replace('" target="_blank',''))
            thumb = art + 'ugdefault.png'
            addDirVideo(prefix, name,justin_url+url,2,thumb)
				
def PLAY_VIDEO(url,name):
        iconimage=""
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('name="movie" value="http://www.youtube.com/v/(.+?)&rel').findall(link)
        if len(match)==0:
            if name.find('Songs')>0:
                dialog = xbmcgui.Dialog()
                dialog.ok("Ultimate Guitar", "Available in the Songs section")
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok("Ultimate Guitar", "This is a text lesson", "Please visit www.justinguitar.com to view")
        else:
            playlist=[]
            for video_id in match:
                url='plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
                thumb = ''
            xbmc.Player().play(url)
            GA("Viewed", name)	
			
def FAVOURITES():
    if os.path.isfile(FAVOURITES_FILE):
        s = read_from_file(FAVOURITES_FILE)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('|')
                name = list[0]
                url = list[1]
                prefix = ''
                addDirVideo(prefix, name,url,2,art + 'ugdefault.png')


################################Youtube Channels#####################################				
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

    addDir(">> Next page",next_page_url,13,"")

	
	
	
	
	
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


def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirVideo(prefix,name,url,mode,iconimage):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        nameurl="%s|%s" % (name,url)
        if watched_index(url) < 0:
            contextMenuItems.append(('Mark as Watched', 'XBMC.RunPlugin(%s?mode=101&url=%s)'% (sys.argv[0], url)))
        else:
            name = '[COLOR cyan]' + "<< " + '[/COLOR]' + name
            contextMenuItems.append(('Remove from Watched List', 'XBMC.RunPlugin(%s?mode=102&url=%s)'% (sys.argv[0], url)))
        if favourites_index(nameurl) < 0:
            contextMenuItems.append(('Save to Favourites', 'XBMC.RunPlugin(%s?mode=103&url=%s)'% (sys.argv[0], urllib.quote_plus(nameurl))))
        else:
            name = '[COLOR gold]' + "+  " + '[/COLOR]' + name
            contextMenuItems.append(('Remove from Favourites', 'XBMC.RunPlugin(%s?mode=104&url=%s)'% (sys.argv[0], urllib.quote_plus(nameurl))))
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, True)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

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
		
def watched_index(url):
    try:
        content = read_from_file(WATCHED_FILE)
        line = str(url)
        lines = content.split('\n')
        index = lines.index(line)
        return index
    except:
        return -1 #Not subscribed
		
def favourites_index(url):
    try:
        content = read_from_file(FAVOURITES_FILE)
        line = str(url)
        lines = content.split('\n')
        index = lines.index(line)
        return index
    except:
        return -1

def watched(url,filename):
    if filename==WATCHED_FILE:
        index = watched_index(url)
    else:
        index = favourites_index(url)
    if index >= 0:
        return
    content = str(url) + '\n'
    write_to_file(filename, content, append=True)
    xbmc.executebuiltin("Container.Refresh")
    
def unwatched(url,filename):
    if filename==WATCHED_FILE:
        index = watched_index(url)
    else:
        index = favourites_index(url)
    if index >= 0:
        content = read_from_file(filename)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        
        if len(s) == 0:
            os.remove(filename)
        else:
            write_to_file(filename, s)
        xbmc.executebuiltin("Container.Refresh")

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
        LESSON_LIST(url)
        
elif mode==2:
        print ""+url
        PLAY_VIDEO(url,name)
		
elif mode==11:
        print ""+url
        LESSON_DIR()
        GA("None", "Lessons")	
		
elif mode==12:
        print ""+url
        SONG_DIR()
        GA("None", "Songs")	
	
elif mode==13:
        print ""+url
        YOUTUBE_CHANNELS(url)
        GA("None", "YouTube")	

elif mode==14:
        FAVOURITES()
		
elif mode==15:
        print ""+url
        YOUTUBE_LIST()
		
elif mode==101:
        watched(url,filename=WATCHED_FILE)
		
elif mode==102:
        unwatched(url,filename=WATCHED_FILE)
		
elif mode==103:
        watched(url,filename=FAVOURITES_FILE)
		
elif mode==104:
        unwatched(url,filename=FAVOURITES_FILE)
		

xbmcplugin.endOfDirectory(int(sys.argv[1]))

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
audio_fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.ultimateguitar', 'fanart.jpg'))
art1 = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.ultimateguitar/art1', ''))


def CATEGORIES():
        addDir('Lessons - JustinGuitar','url',11,art1 + 'lessons.png')
        addDir('Songs etc. - JustinGuitar','url',12,art1 + 'songs.png')
        addDir('YouTube Channels','url',15,art1 + 'youtubemain.png')
        addDir('Favourites','url',14,art1 + 'favourites.png')

		
def YOUTUBE_LIST():
        channel="justinsandercoesongs"
        addDir("Justin Sandercoe",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art1 + 'youtubejs.png')
        channel="martyzsongs"
        addDir("Marty Schwartz",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art1 + 'youtubems.png')
        channel="rockongoodpeople"
        addDir("Next Level Guitar",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art1 + 'youtubenlg.png')
        channel="youcanlearnguitar"
        addDir("You Can Learn Guitar",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art1 + 'youtubeyclg.png')
        channel="guitarings"
        addDir("Guitarings",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art1 + 'youtubegr.png')
        channel="GaragebandandBeyond"
        addDir("GarageBand & Beyond",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art1 + 'youtubegb.png')
        channel="wickedwkd"
        addDir("Pearl Jam covers by wickedwkd",'http://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?start-index=1&max-results=20',13,art1 + 'pjcovers.png')

		
def LESSON_DIR():
        addDir('Beginners Course',justin_url + 'en/BC-000-BeginnersCourse.php',1,art1 + 'jsbeginners.png')
        addDir('Intermediate Course',justin_url + 'en/IM-000-IntermediateMethod.php',1,art1 + 'jsintermediate.png')
        addDir('Quick Tips',justin_url + 'en/QT-000-GuitarQuickTips.php',1,art1 + 'jsintermediate.png')
        addDir('Skills',justin_url + 'en/ES-000-EssentialSkills.php',1,art1 + 'jsbasics.png')
        addDir('Practice',justin_url + 'en/PC-000-Practice.php',1,art1 + 'jspractice.png')
        addDir('Technique',justin_url + 'en/TE-000-Technique.php',1,art1 + 'jstechnique.png')
        addDir('Chords',justin_url + 'en/CH-000-Chords.php',1,art1 + 'jschords.png')
        addDir('Rhythm Guitar',justin_url + 'en/RH-000-RhythmGuitar.php',1,art1 + 'jsrhythm.png')
        addDir('Scales',justin_url + 'en/SC-000-Scales.php',1,art1 + 'jsscales.png')
        addDir('Arpeggios',justin_url + 'en/AR-000-Arpeggios.php',1,art1 + 'jsarpeggios.png')
        addDir('Aural Training',justin_url + 'en/AU-000-AuralTraining.php',1,art1 + 'jsaural.png')
        addDir('Gear and Reviews',justin_url + 'en/GG-000-GuitarGear.php',1,art1 + 'jsgear.png')
        #addDir('Recording Techniques',justin_url + 'en/RT-000-RecordingTechniques.php',1,art1 + 'jsbeginners.png')
        #addDir('Masterclasses',justin_url + 'en/MA-000-Masterclasses.php',1,art1 + 'jsbeginners.png')
		
def SONG_DIR():
        addDir('Beginners Songs',justin_url + 'en//BS-000-BeginnersSongbook.php',1,art1 + 'jsbeginners.png')
        addDir('Intermediate Songs',justin_url + 'en/SB-000-GuitarSongBook.php',1,art1 + 'jsintermediate.png')
        addDir('Other Songs',justin_url + 'en/ST-000-SongsTAB.php',1,art1 + 'jsother.png')
        addDir('Awesome Riffs',justin_url + 'en/RF-000-GuitarRiffs.php',1,art1 + 'jsriffs.png')
        addDir('Awesome Licks',justin_url + 'en/LK-000-GuitarLicks.php',1,art1 + 'jslicks.png')
        addDir('Classic Solos',justin_url + 'en/CS-000-ClassicGuitarSolos.php',1,art1 + 'jssolos.png')
        addDir('Transcribing',justin_url + 'en/TR-000-Transcribing.php',1,art1 + 'jstranscribing.png')
        addDir('Blues (Lead and Rhythm)',justin_url + 'en/BL-000-Blues.php',1,art1 + 'jsblues.png')
        addDir('Folk (Fingerstyle)',justin_url + 'en/FO-000-Folk.php',1,art1 + 'jsfolk.png')
        addDir('Rock and Metal',justin_url + 'en/RO-000-RockMetal.php',1,art1 + 'jsrock.png')
        addDir('Jazz',justin_url + 'en/JA-000-Jazz.php',1,art1 + 'jsjazz.png')

#########################  PEARL JAM	#################################################	
def LESSON_LIST(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)">(.+?)</a><br').findall(link)
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
        link = link.strip(' \t\n\r')
        response.close()
        match = re.compile('video_url": (.+?)"').findall(link)
        for vurl in match:
            vurl = vurl.replace('"http://www.youtube.com/watch?v=', '')
        if len(match)==0:
            if name.find('Songs')>0:
                dialog = xbmcgui.Dialog()
                dialog.ok("Ultimate Guitar", "Available in the Songs section")
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok("Ultimate Guitar", "This is a text lesson", "Please visit www.justinguitar.com to view")
        else:
            playlist=[]
            url='plugin://plugin.video.youtube/?action=play_video&videoid=%s' % vurl
            thumb = ''
            xbmc.Player().play(url)

			
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
		
elif mode==12:
        print ""+url
        SONG_DIR()
	
elif mode==13:
        print ""+url
        YOUTUBE_CHANNELS(url)

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

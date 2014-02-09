import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import cookielib
import settings, time
from t0mm0.common.net import Net
from threading import Thread
cookie_jar = settings.cookie_jar()
net = Net()
ADDON = settings.addon()
ARTIST_ART = settings.artist_icons()
FAV_ARTIST = settings.favourites_file_artist()
FAV_ALBUM = settings.favourites_file_album()
FAV_SONG = settings.favourites_file_songs()
PLAYLIST_FILE = settings.playlist_file()
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.mp3streams',  'fanart.jpg'))
urllist = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.mp3streams',  'lists', 'mp3url.list'))
audio_fanart = ""
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.mp3streams',  'icon.png'))


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
def GET_url(url):
    header_dict = {}
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    header_dict['Host'] = 'musicmp3.ru'
    header_dict['Referer'] = 'http://musicmp3.ru/'
    header_dict['Connection'] = 'keep-alive'
    net.set_cookies(cookie_jar)
    link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    return link
	
def get_cookie():
    header_dict = {}
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    header_dict['Connection'] = 'keep-alive'
    net.set_cookies(cookie_jar)
    link = net.http_GET('http://musicmp3.ru/', headers=header_dict).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)

	
def CATEGORIES():
    addDir('Artists','http://musicmp3.ru/artists.html',21,iconart,'')
    addDir('Top Albums','http://musicmp3.ru/genres.html',12,iconart,'')
    addDir('New Albums','http://musicmp3.ru/new_albums.html',12,iconart,'')
    addDir('Billboard Charts','url',101,iconart,'')
    addDir('Search Artists','url',24,iconart,'')
    addDir('Search Albums','url',24,iconart,'')
    addDir('Search Songs','url',24,iconart,'')
    addDir('Favourite Artists','url',63,iconart,'')
    addDir('Favourite Albums','url',66,iconart,'')
    addDir('Favourite Songs','url',69,iconart,'')
    addDirAudio('Instant Mix (Shuffle and play your favourite songs)','url',99,iconart,'','','')
    addDirAudio('Clear Playlist','url',100,iconart,'','','')
	
def charts():
    addDir('UK Album Chart','http://www1.billboard.com/charts/united-kingdom-albums',102,iconart,'')
    addDir('BillBoard 200','http://www1.billboard.com/charts/billboard-200',102,iconart,'')
    addDir('Hot 100 Singles','http://www1.billboard.com/charts/hot-100',102,iconart,'')
    addDir('Country Albums','http://www1.billboard.com/charts/country-albums',102,iconart,'')
    addDir('HeatSeeker Albums','http://www1.billboard.com/charts/heatseekers-albums',102,iconart,'')
    addDir('Independent Albums','http://www1.billboard.com/charts/independent-albums',102,iconart,'')
    addDir('Catalogue Albums','http://www1.billboard.com/charts/catalog-albums',102,iconart,'')
    addDir('Folk Albums','http://www1.billboard.com/charts/folk-albums',102,iconart,'')
    addDir('Blues Albums','http://www1.billboard.com/charts/blues-albums',102,iconart,'')
    addDir('Tastemaker Albums','http://www1.billboard.com/charts/tastemaker-albums',102,iconart,'')
    addDir('Rock Albums','http://www1.billboard.com/charts/rock-albums',102,iconart,'')
    addDir('Alternative Albums','http://www1.billboard.com/charts/alternative-albums',102,iconart,'')
    addDir('Hard Rock Albums','http://www1.billboard.com/charts/hard-rock-albums',102,iconart,'')
    addDir('Digital Albums','http://www1.billboard.com/charts/digital-albums',102,iconart,'')
    addDir('R&B Albums','http://www1.billboard.com/charts/r-b-hip-hop-albums',102,iconart,'')
    addDir('Top R&B/Hip-Hop Albums','http://www1.billboard.com/charts/r-and-b-albums',102,iconart,'')
    addDir('Dance Electronic Albums','http://www1.billboard.com/charts/dance-electronic-albums',102,iconart,'')
	
def chart_lists(name, url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    if "ukofficial menu" in url:
        all_list = regex_get_all(link, '<div class="previewwindow">', '</div>')
        for list in all_list:
            icon = regex_from_to(list, 'src="', '" />')
            artist = clean_file_name(regex_from_to(list, '<h3>', '</h3>')).replace('&#039;',"'")
            title = clean_file_name(regex_from_to(list, '<h4>', '</h4>')).replace('&#039;',"'")
            addDir(artist + ' ' + title.replace('&amp;', '&'),'http://musicmp3.ru' + url1,5,thumb,'')
    elif "billboard" in url:
        match = re.compile('"title" : "(.+?)"\r\n.+?"artist" : "(.+?)"\r\n.+?image" : "(.+?)"\r\n.+?"entityId" : ".+?"\r\n.+?"entityUrl" : "(.+?)"').findall(link)
        for title, artist, iconimage, url1 in match:
            text = "%s %s" % (artist, title)
            url='http://www1.billboard.com'+url1+'#'+url1
            if re.search('.gif',iconimage):
                iconimage=""
            if not 'Single' in name:
                addDir(artist.replace('&amp;', '&') + ' - ' + title.replace('&amp;', '&'),'url',25,iconimage,'')
            else:
                addDir(artist.replace('&amp;', '&') + ' - ' + title.replace('&amp;', '&'),'url',26,iconimage,'')
	
def artists(url):
    link = GET_url(url)
    addDir('All Artists','http://musicmp3.ru/main_artists.html?type=artist&page=1',31,iconart,'')
    sub_dir = re.compile('<li class="menu_sub__item"><a class="menu_sub__link" href="(.+?)">(.+?)</a></li>').findall(link)
    for url1, title in sub_dir:
        iconimage = 'http://musicmp3.ru/i' + url1.replace('.html', '.jpg').replace('artists', 'genres').replace('tracks', 'track')
        addDir(title.replace('&amp;', '&'),'http://musicmp3.ru' + url1,41,iconimage,'')
	
def all_artists(name, url):
    link = GET_url(url)
    all_artists = re.compile('<li class="small_list__item"><a class="small_list__link" href="(.+?)">(.+?)</a></li>').findall(link)
    for url1, title in all_artists:
        icon_path = os.path.join(ARTIST_ART, title + '.jpg')
        if os.path.exists(icon_path):
            iconimage = icon_path
        else:
            iconimage = iconart
        addDir(title.replace('&amp;', '&'),'http://musicmp3.ru' + url1,22,iconimage,'artists')
    pgnumf = url.find('page=') + 5
    pgnum = int(url[pgnumf:]) + 1
    nxtpgurl = url[:pgnumf]
    nxtpgurl = "%s%s" % (nxtpgurl, pgnum)
    addDir('>> Next page',nxtpgurl,31,xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.mp3streams', 'art', 'next.png')),'')
    setView('movies', 'default')
    
		
def sub_dir(name, url):
    link = GET_url(url)
    addDir('All ' + name + ' Artists',url + '?page=1',31,'http://www.pearljamlive.com/images/pic_home.jpg','')
    sub_dir = re.compile('<li class="menu_sub__item"><a class="menu_sub__link" href="(.+?)">(.+?)</a></li>').findall(link)
    for url, title in sub_dir:
        iconimage = 'http://musicmp3.ru/i' + url.replace('.html', '.jpg').replace('artists', 'genres').replace('tracks', 'track')
        addDir(title.replace('&amp;', '&'),'http://musicmp3.ru' + url + '?page=1',31,iconimage,'')
		
def genres(name,url):
    link = GET_url(url)
    if name == 'Top Albums':
        addDir('Top Albums','http://musicmp3.ru/main_albums.html?gnr_id=&sort=top&type=album&page=1',15,'http://www.pearljamlive.com/images/pic_home.jpg','')
    else:
        addDir('New Albums',url + '?page=1',15,'http://www.pearljamlive.com/images/pic_home.jpg','')
    sub_dir = re.compile('<li class="menu_sub__item"><a class="menu_sub__link" href="(.+?)">(.+?)</a></li>').findall(link)
    for url1, title in sub_dir:
        iconimage = 'http://musicmp3.ru/i' + url1.replace('.html', '.jpg').replace('tracks', 'track')
        addDir(title.replace('&amp;', '&'),'http://musicmp3.ru' + url1,14,iconimage,'')
		
def all_genres(name, url):
    nxtpgnum = int(url.replace('http://musicmp3.ru/main_albums.html?gnr_id=2&sort=top&type=album&page=', '')) + 1
    nxtpgurl = "%s%s" % ('http://musicmp3.ru/main_albums.html?gnr_id=2&sort=top&type=album&page=', str(nxtpgnum))
    link = GET_url(url)
    all_genres = re.compile('<li class="small_list__item"><a class="small_list__link" href="(.+?)">(.+?)</a></li>').findall(link)
    for url1, title in all_genres:
        addDir(title.replace('&amp;', '&'),'http://musicmp3.ru' + url1,22,'http://www.pearljamlive.com/images/pic_home.jpg','')
    addDir('>> Next page',nxtpgurl,13,xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.mp3streams', 'art', 'next.png')))
    
		
def genre_sub_dir(name, url):#gnr_id=491&amp;sort
    link = GET_url(url)
    addDir('Top ' + name + ' Albums',url + '?page=1',15,'http://www.pearljamlive.com/images/pic_home.jpg','')
    sub_dir = re.compile('<li class="menu_sub__item"><a class="menu_sub__link" href="(.+?)">(.+?)</a></li>').findall(link)
    for url, title in sub_dir:
        iconimage = 'http://musicmp3.ru/i' + url.replace('.html', '.jpg').replace('tracks', 'track')
        addDir(title.replace('&amp;', '&'),'http://musicmp3.ru' + url + '?page=1',15,iconimage,'')
		
def genre_sub_dir2(name, url):#gnr_id=491&amp;sort
    link = GET_url(url)
    addDir('Top ' + name + ' Albums',url,15,'http://www.pearljamlive.com/images/pic_home.jpg','')
    sub_dir = re.compile('<li class="menu_sub__item"><a class="menu_sub__link" href="(.+?)">(.+?)</a></li>').findall(link)
    for url, title in sub_dir:
        iconimage = 'http://musicmp3.ru/i' + url.replace('.html', '.jpg').replace('tracks', 'track')
        addDir(title.replace('&amp;', '&'),'http://musicmp3.ru' + url + '?page=1',15,iconimage,'')
		
def search(name, url):
    keyboard = xbmc.Keyboard('', name, False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            if name == 'Search Artists':
                search_artists(query)
            elif name == 'Search Albums':
                search_albums(query)
            elif name == 'Search Songs':
                search_songs(query)
				
def search_artists(query):
    url = 'http://musicmp3.ru/search.html?text=%s&all=artists' % urllib.quote_plus(query)
    link = GET_url(url)
    all_artists = re.compile('<a class="artist_preview__title" href="(.+?)">(.+?)</a>').findall(link)
    for url1, title in all_artists:
        icon_path = os.path.join(ARTIST_ART, title + '.jpg')
        if os.path.exists(icon_path):
            iconimage = icon_path
        else:
            iconimage = iconart
        addDir(title.replace('&amp;', '&'),'http://musicmp3.ru' + url1,22,iconimage,'artists')
		
def search_albums(query):
    url = 'http://musicmp3.ru/search.html?text=%s&all=albums' % urllib.quote_plus(query.replace(' - ', ' ').replace('-', ' '))
    link = GET_url(url)
    all_albums = re.compile('<a class="album_report__link" href="(.+?)"><img class="album_report__image" src="(.+?)" /><span class="album_report__name">(.+?)</span></a>(.+?)album_report__artist" href="(.+?)">(.+?)</a>, <span class="album_report__date">(.+?)</span>').findall(link)
    for url1,thumb,album,plot,artisturl,artist,year in all_albums:
        title = "%s - %s (%s)" % (artist, album, year)
        thumb = thumb.replace('al', 'alm').replace('covers', 'mcovers')
        addDir(title.replace('&amp;', '&'),'http://musicmp3.ru' + url1,5,thumb,'albums')
    setView('movies', 'album')
		
def search_songs(query):
    playlist = []
    url = 'http://musicmp3.ru/search.html?text=%s&all=songs' % urllib.quote_plus(query.replace(' - ', ' ').replace('-', ' '))
    link = GET_url(url)
    match = re.compile('<tr class="song"><td class="song__play_button"><a class="player__play_btn js_play_btn" href="#" rel="(.+?)" title="Play track" /></td><td class="song__name song__name--search"><a class="song__link" href="(.+?)">(.+?)</a>(.+?)song__link" href="(.+?)">(.+?)</a>(.+?)<a class="song__link" href="(.+?)">(.+?)</a>').findall(link)
    for id,songurl,song,d1,artisturl,artist,d2,albumurl,album in match:
        iconimage = ""
        url = 'http://listen.musicmp3.ru/2f99f4bf4ce7b171/' + id
        title = "%s - %s - %s" % (artist.replace('&amp;','&'), song.replace('&amp;','&'), album.replace('&amp;','&'))
        addDirAudio(title,url,10,iconimage,song,artist,album)
        liz=xbmcgui.ListItem(song, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo('music', {'Title':song, 'Artist':artist, 'Album':album})
        liz.setProperty('mimetype', 'audio/mpeg')
        liz.setThumbnailImage(iconimage)
        liz.setProperty('fanart_image', audio_fanart)
        playlist.append((url, liz))
    setView('music', 'song')
		
def album_list(name, url): 
    link = GET_url(url)
    try:
        artist_url = regex_from_to(link, 'class="art_wrap__img" src="', '"')
        get_artist_icon(name,artist_url)
    except:
        pass
    all_albums = re.compile('<a class="album_report__link" href="(.+?)"><img alt="(.+?)" class="album_report__image" src="(.+?)" /><span class="album_report__name">(.+?)</span>(.+?)"album_report__artist" href="(.+?)">(.+?)</a>, <span class="album_report__date">(.+?)</span>').findall(link)
    for url1,d1,thumb,album,plot,artisturl,artist,year in all_albums:
        title = "%s - %s - %s" % (artist, album, year)
        thumb = thumb.replace('al', 'alm').replace('covers', 'mcovers')
        addDir(title.replace('&amp;', '&'),'http://musicmp3.ru' + url1,5,thumb,'albums')
    pgnumf = url.find('page=') + 5
    pgnum = int(url[pgnumf:]) + 1
    nxtpgurl = url[:pgnumf]
    nxtpgurl = "%s%s" % (nxtpgurl, pgnum)
    addDir('>> Next page',nxtpgurl,15,xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.mp3streams', 'art', 'next.png')),'')
    setView('movies', 'album')

    
		
def albums(name, url):
    duplicate = []
    link = GET_url(url)
    try:
        artist_url = regex_from_to(link, 'class="art_wrap__img" src="', '"')
        get_artist_icon(name,artist_url)
    except:
        pass
    all_albums = re.compile('<div class="album_report"><h5 class="album_report__heading"><a class="album_report__link" href="(.+?)"><img alt="(.+?)" class="album_report__image" src="(.+?)" /><span class="album_report__name">(.+?)</span>(.+?)<span class="album_report__date">(.+?)</span>').findall(link)
    for url1,d1,thumb,album,plot,year in all_albums:
        title = "%s - %s - %s" % (name, album, year)
        if title not in duplicate:
            duplicate.append(title)
            thumb = thumb.replace('al', 'alm').replace('covers', 'mcovers')
            addDir(title.replace('&amp;', '&'),'http://musicmp3.ru' + url1,5,thumb,'albums')
    setView('movies', 'album')
		
def find_url(id):
    s = read_from_file(urllist)
    if id + '-' in s:
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                urlstart = list.split('-')
                urlid = urlstart[0]
                url = urlstart[1]
                if urlid == id:
                    return url
    else:
        return 'http://listen.musicmp3.ru/6b5ee4f8422b6e8d/'
			

def play_album(name, url, iconimage,clear,mix):
    browse=False
    playlist=[]
    dialog = xbmcgui.Dialog()
    if mode != 6 and mix != 'mix':
        if dialog.yesno("MP3 Streams", 'Browse songs or play full album?', '', '', 'Play Now','Browse'):
            browse=True
    if browse == True:
        link = GET_url(url)
        match = re.compile('<tr class="song" id="(.+?)" itemprop="tracks" itemscope="itemscope" itemtype="http://schema.org/MusicRecording"><td class="song__play_button"><a class="player__play_btn js_play_btn" href="#" rel="(.+?)" title="Play track" /></td><td class="song__name"><div class="title_td_wrap"><meta content="(.+?)" itemprop="url" /><meta content="(.+?)" itemprop="duration"(.+?)<meta content="(.+?)" itemprop="inAlbum" /><meta content="(.+?)" itemprop="byArtist" /><span itemprop="name">(.+?)</span><div class="jp-seek-bar" data-time="(.+?)"><div class="jp-play-bar"></div></div></div></td><td class="song__service song__service--ringtone').findall(link)
        for track,id,songurl,meta, d1,album,artist,songname,dur in match:
            trn = track.replace('track','')
            url = find_url(trn) + id
            title = "%s. %s" % (track.replace('track',''), songname.replace('&amp;', '&'))
            addDirAudio(title,url,10,iconimage,songname,artist,album)
            liz=xbmcgui.ListItem(songname, iconImage=iconimage, thumbnailImage=iconimage)
            liz.setInfo('music', {'Title':songname, 'Artist':artist, 'Album':album, 'duration':dur })
            liz.setProperty('mimetype', 'audio/mpeg')
            liz.setProperty("IsPlayable","true")
            liz.setThumbnailImage(iconimage)
            liz.setProperty('fanart_image', fanart)
            playlist.append((url, liz))
				
    else:
        dp = xbmcgui.DialogProgress()
        dp.create("MP3 Streams",'Creating Your Playlist')
        dp.update(0)
        pl = get_XBMCPlaylist(clear)
        link = GET_url(url)
        match = re.compile('<tr class="song" id="(.+?)" itemprop="tracks" itemscope="itemscope" itemtype="http://schema.org/MusicRecording"><td class="song__play_button"><a class="player__play_btn js_play_btn" href="#" rel="(.+?)" title="Play track" /></td><td class="song__name"><div class="title_td_wrap"><meta content="(.+?)" itemprop="url" /><meta content="(.+?)" itemprop="duration"(.+?)<meta content="(.+?)" itemprop="inAlbum" /><meta content="(.+?)" itemprop="byArtist" /><span itemprop="name">(.+?)</span><div class="jp-seek-bar" data-time="(.+?)"><div class="jp-play-bar"></div></div></div></td><td class="song__service song__service--ringtone').findall(link)
        nItem=len(match)
        for track,id,songurl,meta, d1,album,artist,songname,dur in match:
            trn = track.replace('track','')
            url = find_url(trn) + id
            title = "%s. %s" % (track.replace('track',''), songname.replace('&amp;', '&'))
            addDirAudio(title,url,10,iconimage,songname,artist,album)
            liz=xbmcgui.ListItem(songname, iconImage=iconimage, thumbnailImage=iconimage)
            liz.setInfo('music', {'Title':songname, 'Artist':artist, 'Album':album, 'duration':dur})
            liz.setProperty('mimetype', 'audio/mpeg')
            liz.setProperty("IsPlayable","true")
            liz.setThumbnailImage(iconimage)
            liz.setProperty('fanart_image', fanart)
            playlist.append((url, liz))

            progress = len(playlist) / float(nItem) * 100               
            dp.update(int(progress), 'Adding to Your Playlist',title)
            if dp.iscanceled():
                return

  
        for blob ,liz in playlist:
            try:
                if blob:
                    pl.add(blob,liz)
            except:
                pass
        if clear or (not xbmc.Player().isPlayingAudio()):
           xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
			
			
def play_song(url,name,songname,artist,album,iconimage,clear):
    dialog = xbmcgui.Dialog()
    show_name=name
    playlist=[]
    pl = get_XBMCPlaylist(clear)
    url1=str(url)
    liz=xbmcgui.ListItem(show_name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo('music', {'Title':songname, 'Artist':artist, 'Album':album})
    liz.setProperty('mimetype', 'audio/mpeg')
    liz.setThumbnailImage(iconimage)
    liz.setProperty('fanart_image', fanart)
    playlist.append((url1, liz))
    for blob ,liz in playlist:
        try:
            if blob:
                pl.add(blob,liz)
        except:
            pass
    if clear or (not xbmc.Player().isPlayingAudio()):
        xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)	

def get_artist_icon(name,url):
    data_path = os.path.join(ARTIST_ART, name + '.jpg')
    if not os.path.exists(data_path):
        dlThread = DownloadIconThread(name, url, data_path)
        dlThread.start()
		
def instant_mix():
    playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    playlist.clear()
    if os.path.isfile(FAV_SONG):
        s = read_from_file(FAV_SONG)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                splitdata = list.split('<>')
                artist = splitdata[0]
                album = splitdata[1]
                songname = splitdata[2]
                url1 = splitdata[3]
                iconimage = splitdata[4]
                play_song(url1,songname.upper(),songname.upper(),artist.upper(),album.upper(),iconimage,False)
    playlist.shuffle()
	
class DownloadIconThread(Thread):
    def __init__(self, name, url, data_path):
        self.data = url
        self.path = data_path
        Thread.__init__(self)

    def run(self):
        path = str(self.path)
        data = self.data
        urllib.urlretrieve(data, path)
	
def favourite_artists():
    if os.path.isfile(FAV_ARTIST):
        s = read_from_file(FAV_ARTIST)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                url = list1[1]
                icon_path = os.path.join(ARTIST_ART, title + '.jpg')
                if os.path.exists(icon_path):
                    iconimage = icon_path
                else:
                    iconimage = iconart
                addDir(title.replace('&amp;', '&').upper(),url,22,iconimage,'artists')
        
				
def favourite_albums():
    if os.path.isfile(FAV_ALBUM):
        s = read_from_file(FAV_ALBUM)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                url = list1[1]
                thumb = list1[2]
                addDir(title.replace('&amp;', '&').upper(),url,5,thumb,'albums')
				
def favourite_songs():
    if os.path.isfile(FAV_SONG):
        s = read_from_file(FAV_SONG)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                artist = list1[0]
                album = list1[1]
                title = list1[2]
                url = list1[3]
                iconimage = list1[4]
                text = "%s - %s - %s" % (title, artist, album)
                addDirAudio(text.upper(),url,10,iconimage,title,artist,album)

def add_favourite(name, url, dir, text):
    splitdata = url.split('<>')
    if 'artist' in dir:
        artist = splitdata[0]
        url1 = splitdata[1]
        add_to_list(url, dir)
        notification(name.upper(), "[COLOR lime]" + text + "[/COLOR]", '5000','')
        link = GET_url(url1)
        try:
            artist_url = regex_from_to(link, 'class="art_wrap__img" src="', '"')
            get_artist_icon(artist,artist_url)
        except:
            pass
    else:
        artist = splitdata[0]
        url1 = splitdata[1]
        thumb = splitdata[2]
        add_to_list(url, dir)
        notification(name.upper(), "[COLOR lime]" + text + "[/COLOR]", '5000', thumb)
		
def add_favourite_song(name, url, dir, text):#str(artist),str(album)str(songname).lower(),url,str(iconimage)
    splitdata = url.split('<>')
    artist = splitdata[0]
    album = splitdata[1]
    songname = splitdata[2]
    url1 = splitdata[3]
    iconimage = splitdata[4]
    add_to_list(url, dir)
    notification(songname.upper(), "[COLOR lime]" + text + "[/COLOR]", '5000',iconimage)
	
def remove_from_favourites(name, url, dir, text):
    splitdata = url.split('<>')
    artist = splitdata[0]
    url1 = splitdata[1]
    thumb = splitdata[2]
    remove_from_list(url, dir)
    notification(name.upper(), "[COLOR orange]" + text + "[/COLOR]", '5000', thumb)

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
    if not 'song' in file:
        xbmc.executebuiltin("Container.Refresh")
    
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


def get_XBMCPlaylist(clear):
    pl=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    if clear:
        pl.clear()
    return pl
	
def clear_playlist():
    pl=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    pl.clear()
    notification('Playlist', 'Cleared', '2000', iconart)

	
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
	
def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r
	
def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', audio_fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage,type):
        suffix = ""
        if type == "artists":
            list = "%s<>%s" % (str(name).lower(),url)
        else:
            list = "%s<>%s<>%s" % (str(name).lower(),url,str(iconimage))
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&list="+str(list)
        ok=True
        contextMenuItems = []
        if type == "artists":
            if find_list(list, FAV_ARTIST) < 0:
                suffix = ""
                contextMenuItems.append(("[COLOR lime]Add to Favourite Artists[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=61)'%(sys.argv[0], name, str(list))))
            else:
                suffix = ' [COLOR lime]+[/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from Favourite Artists[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=62)'%(sys.argv[0], name, str(list))))
        if type == "albums":
            queue_music = '%s?name=%s&url=%s&iconimage=%s&mode=6' % (sys.argv[0], urllib.quote(name), url, iconimage)  
            contextMenuItems.append(('[COLOR cyan]Queue Album[/COLOR]', 'XBMC.RunPlugin(%s)' % queue_music))
            if find_list(list.lower(), FAV_ALBUM) < 0:
                suffix = ""
                contextMenuItems.append(("[COLOR lime]Add to Favourite Albums[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=64)'%(sys.argv[0], name, str(list))))
            else:
                suffix = ' [COLOR lime]+[/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from Favourite Albums[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=65)'%(sys.argv[0], name, str(list))))
        liz=xbmcgui.ListItem(name + suffix, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirAudio(name,url,mode,iconimage,songname,artist,album):
        suffix = ""
        list = "%s<>%s<>%s<>%s<>%s" % (str(artist),str(album),str(songname).lower(),url,str(iconimage))
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&songname="+urllib.quote_plus(songname)+"&artist="+urllib.quote_plus(artist)+"&album="+urllib.quote_plus(album)
        ok=True
        queue_song = '%s?name=%s&url=%s&iconimage=%s&songname=%s&artist=%s&album=%s&mode=11' % (sys.argv[0], urllib.quote(songname), url, iconimage,songname,artist,album)  
        contextMenuItems.append(('[COLOR cyan]Queue Song[/COLOR]', 'XBMC.RunPlugin(%s)' % queue_song))
        if find_list(list.lower(), FAV_SONG) < 0:
            suffix = ""
            contextMenuItems.append(("[COLOR lime]Add to Favourite Songs[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=67)'%(sys.argv[0], name, str(list))))
        else:
            suffix = ' [COLOR lime]+[/COLOR]'
            contextMenuItems.append(("[COLOR orange]Remove from Favourite Songs[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=68)'%(sys.argv[0], name, str(list))))
        liz=xbmcgui.ListItem(name + suffix, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
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
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        songname=urllib.unquote_plus(params["songname"])
except:
        pass
try:
        artist=urllib.unquote_plus(params["artist"])
except:
        pass
try:
        album=urllib.unquote_plus(params["album"])
except:
        pass
try:
        list=str(params["list"])
except:
        pass


if mode==None or url==None or len(url)<1:
    CATEGORIES()
    #get_cookie()
       
elif mode==4:
     charts()
		
		
elif mode==1:
    audio_result(name, url)
	
elif mode ==5:
    play_album(name, url, iconimage, True,'')
	
elif mode ==6:
    play_album(name, url, iconimage, False,'')
	
elif mode ==8:
    ADDON.openSettings()
	
elif mode == 10:
    play_song(url,name,songname,artist,album,iconimage,True)
	
elif mode == 11:
    play_song(url,name,songname,artist,album,iconimage,False)
	
elif mode == 21:
    artists(url)
	
elif mode == 31:
    all_artists(name, url)
	
elif mode == 41:
    sub_dir(name, url)
	
elif mode == 22:
    albums(name,url)

elif mode == 12:
    genres(name,url)
	
elif mode == 13:
    all_genres(name, url)
	
elif mode == 14:
    genre_sub_dir(name, url)

elif mode == 16:
    genre_sub_dir2(name, url)
	
elif mode == 15:
    album_list(name, url)
	
elif mode == 24:
    search(name, url)
	
elif mode == 25:
    search_albums(name)
	
elif mode == 26:
    search_songs(name)
	
elif mode == 61:
    add_favourite(name, url,  FAV_ARTIST, "Added to Favourites")
		
elif mode == 62:
    remove_from_favourites(name, url, FAV_ARTIST, "Removed from Favourites")
		
elif mode == 63:
    favourite_artists()
	
elif mode == 64:
    add_favourite(name, url,  FAV_ALBUM, "Added to Favourites")
		
elif mode == 65:
    remove_from_favourites(name, url, FAV_ALBUM, "Removed from Favourites")
	
elif mode == 67:
    add_favourite_song(name, url, FAV_SONG, 'Added to Favourites')
	
elif mode == 69:
    favourite_songs()
	
elif mode == 68:
    remove_from_favourites(name, url, FAV_SONG, "Removed from Favourites")
	
elif mode == 66:
    favourite_albums()
	
elif mode == 99:
    instant_mix()
	
elif mode == 100:
    clear_playlist()
	
elif mode == 101:
    charts()
	
elif mode == 102:
    chart_lists(name, url)
		

xbmcplugin.endOfDirectory(int(sys.argv[1]))

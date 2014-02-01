import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import settings, glob
import time,datetime
from common import regex_get_all, regex_from_to, create_directory, write_to_file, read_from_file, clean_file_name
from datetime import date
from meta import TheTVDBInfo
USERDATA = xbmc.translatePath(os.path.join('special://home/userdata', 'addon_data'))
check_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
dummy_file = os.path.join(xbmc.translatePath('special://home/addons/plugin.video.mysubscriptions'), 'dummyclip.mp4')
fanart = ''
ADDON = settings.addon()
SUB_FILE = settings.subscription_file()
SUB_IMDB_FILE = settings.subs_imdb_file()
TV_SHOWS_PATH = settings.tv_directory()

def CATEGORIES():
    addDir( 'Refresh Subscriptions','url',1,'')
    addDir( 'Settings','url',2,'')
    addDir( 'Help','url',4,'')
		
def open_settings():
    ADDON.openSettings()

def find_shows(name,url):
    plugins = os.listdir(USERDATA)
    for addons in plugins:
        addon_path = os.path.join(USERDATA, addons)
        subdirpath = os.listdir(addon_path)
        for s in subdirpath:
            if 'show' in s.lower():
                show_path = os.path.join(addon_path, s)
                subshowpath = os.listdir(show_path)
                for s in subshowpath:
                    season_path = os.path.join(show_path, s)
                    text = s
                    add_to_list(text, SUB_FILE)
    subscription_imdb()
    get_subscriptions()
    time.sleep(1)
    xbmc.executebuiltin('UpdateLibrary(video)')


def subscription_imdb():
    if os.path.isfile(SUB_FILE):
        s = read_from_file(SUB_FILE)
        show_list = s.split('\n')
        for show in show_list:
            if show != '':
                try:
                    imdb_id = get_imdb(show)
                    text = "%s<>%s" % (show, imdb_id)
                    add_to_list(text, SUB_IMDB_FILE)
                except:
                    pass

				
def get_subscriptions():
    content = read_from_file(SUB_IMDB_FILE)
    lines = content.split('\n')
        
    for line in lines:
        data = line.split('<>')
        if len(data) == 2:
            tv_show_name = clean_file_name(data[0])
            tv_show_imdb = data[1]
            tv_show_mode = "3"
            create_tv_show_strm_files(tv_show_name, tv_show_imdb, tv_show_mode, TV_SHOWS_PATH)
				
def get_imdb(show):
    params = {}
    params["title"] = show
    params["view"] = "simple"
    params["count"] = "1"
    params["title_type"] = "tv_series,mini_series,tv_special"
    url = "%s%s" % ("http://m.imdb.com/search/title?", urllib.urlencode(params))
    imdb_id = search_imdb(url)
    return imdb_id

def search_imdb(url):
    body = open_url(url)
 	
    first_show = regex_from_to(body, '<tr class=', '</tr>')
    all_td = regex_get_all(first_show, '<td', '</td>')
    imdb_id = regex_from_to(all_td[1], '/title/', '/')
    return imdb_id

def create_tv_show_strm_files(name, imdb_id, mode, dir_path):
    info = TheTVDBInfo(imdb_id)
    episodes = info.episodes()
    tv_show_path = create_directory(dir_path, name)
    for episode in episodes:
        first_aired = episode.FirstAired()
        if len(first_aired) > 0:
            d = first_aired.split('-')
            episode_date = date(int(d[0]), int(d[1]), int(d[2]))
            if date.today() > episode_date:
                season_number = int(episode.SeasonNumber())
                if season_number > 0:
                    episode_number = int(episode.EpisodeNumber())
                    episode_name = episode.EpisodeName()
                    display = "S%.2dE%.2d %s" % (season_number, episode_number, episode_name)
                    data = '%s<|>%s<|>%d<|>%d' % (name, episode_name, season_number, episode_number)
                    season_path = create_directory(tv_show_path, str(season_number))
                    create_strm_file(display, data, imdb_id, mode, season_path)
					
def stream_episode(name, data):
    dialog = xbmcgui.Dialog()
    menu_texts = []
    menu_data = []
    menu_path = []
    splitdata = data.split('<|>')
    showname = splitdata[0]
    showseason = splitdata[2]
    showepisode = splitdata[3]
    plugins = os.listdir(USERDATA)
    for addons in plugins:
        addon_path = os.path.join(USERDATA, addons)
        subdirpath = os.listdir(addon_path)
        for s in subdirpath:
            if 'show' in s.lower():
                show_path = os.path.join(addon_path, s)
                subshowpath = os.listdir(show_path)
                for s in subshowpath:
                    season_path = os.path.join(show_path, s)
                    if s == showname:
                        season_path = os.path.join(show_path, s)
                        seasonpath = os.listdir(season_path)
                        for se in seasonpath:
                            snum = se.replace('Season ', '').replace('season ', '').replace('season 0', '').replace('Season 0', '').replace('S', '').replace('S0', '')
                            if snum == showseason:
                                episode_path = os.path.join(season_path, se)
                                all_episodes = os.listdir(episode_path)
                                for episode in all_episodes:
                                    epnum1 = episode.replace(showname + ' ', '').replace(showname, '').replace(showname + ' ', '').replace('.strm', '').replace('[', '').replace(']', '')
                                    if ' ' in epnum1:
                                        epnum1 = epnum1.split(' ')[0]
                                    if 'E' in epnum1:
                                        epnum1 = epnum1.split('E')[1]
                                    if 'x' in epnum1:
                                        epnum1 = epnum1.split('x')[1]
                                    if epnum1.startswith('0'):
                                        epnum1 = epnum1.replace('0', '')
                                    if epnum1 == showepisode:
                                        ep_path = os.path.join(episode_path, episode)
                                        addon_name = addons.replace('plugin.video.', '').upper()
                                        s = read_from_file(ep_path)
                                        ep_list = s.split('\n')
                                        for ep_url in ep_list:
                                            if ep_url != '':
                                                menu_texts.append(addon_name)
                                                menu_data.append(ep_url)
                                                menu_path.append(ep_path)
												
    if len(menu_texts) == 1:
         menu_id = 0	
    else:
        menu_id = dialog.select('Select Addon', menu_texts)
        if(menu_id < 0):
            return (None, None)
            dialog.close()
    url_id = str(menu_path[menu_id])
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    playlist.add(dummy_file)
    playlist.add(url_id)
    xbmc.Player().play(playlist)

def help():
    msg = os.path.join(ADDON.getAddonInfo('path'),'resources', 'messages', 'help.txt')
    TextBoxes("[B][COLOR red]My Subscriptions[/B][/COLOR]",msg)

def TextBoxes(heading,anounce):
        class TextBox():
            """Thanks to BSTRDMKR for this code:)"""
                # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()


            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                        f = open(anounce)
                        text = f.read()
                except:
                        text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()
		
def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	

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
	
def create_strm_file(name, data, imdb_id, mode, dir_path):
    strm_string = create_url(name, mode, data, imdb_id)
    filename = clean_file_name("%s.strm" % name)
    path = os.path.join(dir_path, filename)
    stream_file = open(path, 'w')
    stream_file.write(strm_string)
    stream_file.close()


		
def create_url(name, mode, data, imdb_id):
    name = urllib.quote(str(name))
    data = urllib.quote(str(data))
    mode = str(mode)
    url = sys.argv[0] + '?name=%s&url=%s&mode=%s&iconimage=%s' % (name, data, mode, imdb_id)
    return url

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
		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

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
        data=urllib.unquote_plus(params["data"])
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
        print ""
        CATEGORIES()
		
elif mode ==1:
    find_shows(name,url)
	
elif mode == 2:
    open_settings()
	
elif mode == 3:
    stream_episode(name, url)
	
elif mode == 4:
    help()


xbmcplugin.endOfDirectory(int(sys.argv[1]))

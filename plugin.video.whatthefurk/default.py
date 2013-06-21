'''
Created on 6 feb 2012

@author: Batch, kinkin
'''

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, gzip
import settings
from common import notification, get_url, regex_get_all, regex_from_to, create_directory, write_to_file, read_from_file, clean_file_name, get_file_size, wait, wait_dl_only
from datetime import date, timedelta
import urllib, os, sys, re, urllib2
import shutil, glob
from furk import FurkAPI
from mediahandler import play, download, download_and_play, set_resolved_url
from meta import TheTVDBInfo, set_movie_meta, download_movie_meta, set_tv_show_meta, download_tv_show_meta, meta_exist
from threading import Thread
import time
import datetime

ADDON = settings.addon()


DATA_PATH = settings.data_path()
CACHE_PATH = settings.cache_path()
COOKIE_JAR = settings.cookie_jar()
SUBSCRIPTION_FILE = settings.subscription_file()
IMDB_SEARCH_FILE = settings.imdb_search_file()
IMDB_ACTOR_FILE = settings.imdb_actor_file()
FURK_SEARCH_FILE = settings.furk_search_file()
DUMMY_PATH = settings.dummy_path()
DOWNLOAD_PATH = settings.download_path()
META_PATH = settings.meta_path()
FURK_MODERATED = settings.furk_moderated()
#FURK_SHOW_FILE_SIZE = settings.furk_file_size()
#FURK_FILE_SIZE_UNIT = settings.furk_file_size_unit()
IMDB_TITLE_SEARCH = settings.imdb_search_url()
IMDB_ACTOR_SEARCH = settings.imdb_actors_url()
COUNT = settings.imdb_filter_count()
PRODUCTION_STATUS = settings.imdb_filter_status()
VIEW = settings.imdb_filter_view()
RELEASE_DATE = settings.imdb_filter_release()
USER_RATING = settings.imdb_filter_rating()
NUM_VOTES = settings.imdb_filter_votes()
IMDB_RESULTS = settings.imdb_results()
FURK_ACCOUNT = settings.furk_account()
FURK_USER = settings.furk_user()
FURK_PASS = settings.furk_pass()
SUBSCRIPTIONS_ACTIVATED = settings.subscription_update()
UNICODE_INDICATORS = settings.use_unicode()
DOWNLOAD_META = settings.download_meta()
MOVIES_PATH = settings.movies_directory()
TV_SHOWS_PATH = settings.tv_show_directory()
FIRST_TIME_STARTUP = settings.first_time_startup()
PLAY_MODE = settings.play_mode()
FURK = FurkAPI(COOKIE_JAR)
SORT_TOP_MOV = settings.top_movies_sort()
SORT_MOV_GEN = settings.movie_genre_sort()
SORT_MOV_GRP = settings.movie_group_sort()
SORT_MOV_STU = settings.movie_studio_sort()
SORT_MOV_NEW = settings.new_movies_sort()
SORT_BLU_RAY = settings.blu_ray_sort()
SORT_TOP_TV = settings.top_tv_sort()
SORT_TV_GEN = settings.tv_genre_sort()
SORT_TV_GRP = settings.tv_group_sort()
SORT_TV_ACT = settings.tv_active_sort()
SORT_IMDB_SEARCH = settings.imdb_search_sort()
XBMC_SORT = settings.xbmc_sort()
NEWMOVIE_DAYS = settings.newmovie_days()
CUSTOMQUALITY = settings.custom_quality()
TVCUSTOMQUALITY = settings.tvcustom_quality()
FURK_SORT = settings.furk_sort()
FURK_RESULTS = settings.furk_results()
IMDB_WATCHLIST = settings.imdb_watchlist_url()
IMDB_CUSTOMLIST_URL = settings.imdb_list_url()
UNAIRED = settings.show_unaired()
IMDB_LIST1 = settings.imdb_list1()
IMDB_LIST2 = settings.imdb_list2()
IMDB_LIST3 = settings.imdb_list3()
IMDB_LIST4 = settings.imdb_list4()
IMDB_LIST5 = settings.imdb_list5()
IMDB_LIST6 = settings.imdb_list6()
IMDB_LIST7 = settings.imdb_list7()
IMDB_LIST8 = settings.imdb_list8()
IMDB_LIST9 = settings.imdb_list9()
IMDB_LIST10 = settings.imdb_list10()
IMDB_LISTNAME1 = settings.imdb_listname1()
IMDB_LISTNAME2 = settings.imdb_listname2()
IMDB_LISTNAME3 = settings.imdb_listname3()
IMDB_LISTNAME4 = settings.imdb_listname4()
IMDB_LISTNAME5 = settings.imdb_listname5()
IMDB_LISTNAME6 = settings.imdb_listname6()
IMDB_LISTNAME7 = settings.imdb_listname7()
IMDB_LISTNAME8 = settings.imdb_listname8()
IMDB_LISTNAME9 = settings.imdb_listname9()
IMDB_LISTNAME10 = settings.imdb_listname10()
NZBMOVIE_URL = settings.nzvmovie_url()
FURK_LIM_FS = settings.furk_limit_file_size()
FURK_LIM_FS_NUM = settings.furk_limit_fs_num()
FURK_LIM_FS_MIN = settings.furk_limit_fs_min()
FURK_LIM_FS_TV = settings.furk_limit_file_size_tv()
FURK_LIM_FS_NUM_TV = settings.furk_limit_fs_num_tv()
FURK_PLAYLISTS = settings.furk_playlists()
FURK_FORMAT = settings.furk_format()
FURK_LIMIT = settings.furk_limit_result()
META_QUALITY = settings.meta_quality()
FURK_SEARCH_MF = settings.furk_search_myfiles()
ONECLICK_SEARCH = settings.oneclick_search()
QUALITYSTYLE = settings.qualitystyle()
DOWNLOAD_MOV = settings.movies_download_directory()
DOWNLOAD_TV = settings.tv_download_directory()
DOWNLOAD_SUB = settings.download_subtitles()
ACTIVE_DOWNLOADS = settings.downloads_file()
ACTIVE_DOWNLOADS_TV = settings.downloads_file_tv()
LIBRARY_FORMAT = settings.lib_format()
WISHLIST = settings.wishlist()
WISHLIST_FINISHED = settings.wishlist_finished()
PEOPLE_LIST = settings.people_list()
TRAILER_RESTRICT = settings.restrict_trailer()
TRAILER_QUALITY = settings.trailer_quality()
TRAILER_ONECLICK = settings.trailer_one_click()


fanart = os.path.join(ADDON.getAddonInfo('path'),'art','fanart.png')

######################## DEV MESSAGE ###########################################################################################
def dev_message():
    if ADDON.getSetting('dev_message')!="skip1.4.2":
        dialog = xbmcgui.Dialog()
        #if dialog.yesno("What the Furk....xbmchub.com", "Current meta data (runtime) is calculated incorrectly", "This is now fixed, but existing meta text files should be deleted", "Posters and fanart will NOT be deleted", "Don't do anything", "Delete meta files"):
            #deletemetafiles()
        #else:
            #dialog.ok("What the Furk....xbmchub.com","No problem","You can run at any time from the maintenance menu")
        dialog.ok("Changes in this version:","Added option [Furk tab] to check My Files on all searches","My files results returned at the top (gold)", "Applies to Library, WTF browse and Furk Search options")
        dialog.ok("Changes in this version continued:", "Added 'Other Addon' search to bottom of search results","Applies only to searches from xbmc library", "Use the context menu within the addon")
        dialog.ok("Changes in this version continued:", "Fixed 'Search latest torrents' option", "Option now added to results using library search")
        dialog.ok("Changes in this version continued:", "Added more options to 'New Movie Days' setting", "Now search up to 360 days")
        ADDON.setSetting('dev_message', value='skip1.4.2') 

######################## DEV MESSAGE ###########################################################################################

def toggle_one_click():
    if ONECLICK_SEARCH:
        ADDON.setSetting('oneclick_search', value='false')
        notification("WTF - One-Click Search", "TURNED OFF")
    else:
        ADDON.setSetting('oneclick_search', value='true')
        notification("WTF - One-Click Search", "TURNED ON")
    if mode != "mainenance menu":
        xbmc.executebuiltin('xbmc.activatewindow(0)')
		
def login_at_furk():
    if FURK_ACCOUNT:
        if FURK.login(FURK_USER, FURK_PASS):
            return True
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("Login failed", "The addon failed to login at Furk.net.", "Make sure you have confirmed your email and your", "login information is entered correctly in addon-settings")
            return False
    else:
        return False

def account_info():
    if not login_at_furk():
        return []
	
    try:	
        accinfo = FURK.account_info()
        text = []
        info = str(accinfo).replace("'","QTE")
	
        acctype = regex_from_to(info, 'nameQTE: uQTE', 'QTE, ')
     
        limit_mth = float(regex_from_to(info, 'bw_limit_monthQTE: uQTE', 'QTE, '))/1073741824
        used_bw_mth = float(regex_from_to(info, 'bw_used_monthQTE: uQTE', 'QTE, '))/1073741824
        rem_bw_mth = limit_mth - used_bw_mth
        multi_mth = regex_from_to(info, 'is_not_last_monthQTE: uQTE', 'QTE, ')
        if multi_mth == '1':
            text = "resets"
        else:
            text = "expires"
	
        bw_days_left = float(regex_from_to(info, 'bw_month_time_leftQTE: uQTE', 'QTE, '))/60/60/24
        rem_days = "%.1f" % bw_days_left
		


        dialog = xbmcgui.Dialog()
        dialog.ok(("Account Type: " + acctype) + " - " + ("%.0fGB" % limit_mth) + " pm", ("Current Month: " + '[COLOR red]' + ("%.1fGB" % used_bw_mth) + '[/COLOR]' + " / " + '[COLOR green]' + ("%.1fGB" % rem_bw_mth) + '[/COLOR]' + " / " + ("%.1fGB" % limit_mth)), "", ("Bandwidth limit " + text + " in " + str(rem_days) + " days"))

    except:
        accinfo = FURK.account_info()
        info = regex_from_to(str(accinfo).replace("'","QTE"), 'QTEbw_statsQTE', ']}') 
		
        
        all_bytes = regex_get_all(info, 'uQTEbytesQTE: u', ', uQTE')

        day1 = regex_from_to(all_bytes[0], 'QTE: uQTE', 'QTE, u')
        day2 = regex_from_to(all_bytes[1], 'QTE: uQTE', 'QTE, u')
        day3 = regex_from_to(all_bytes[2], 'QTE: uQTE', 'QTE, u')
        day4 = regex_from_to(all_bytes[3], 'QTE: uQTE', 'QTE, u')
        day5 = regex_from_to(all_bytes[4], 'QTE: uQTE', 'QTE, u') 
        day6 = regex_from_to(all_bytes[5], 'QTE: uQTE', 'QTE, u')
        day7 = regex_from_to(all_bytes[6], 'QTE: uQTE', 'QTE, u')
		
        if float(day1) > 1073741824:
            day1_tot =  float(day1)/1073741824
            day1_text = "%.2fGB" % day1_tot
        else:
            day1_tot = float(day1)/1048576
            day1_text = "%.1fMB" % day1_tot
			
        week_tot = int(day1) + int(day2) + int(day3) + int(day4) + int(day5) + int(day6) + int(day7)
        if float(week_tot) > 1073741824:
            week_total =  float(week_tot)/1073741824
            week_text = "%.2fGB" % week_total
        else:
            week_total =  float(week_tot)/1048576
            week_text = "%.1fMB" % week_total
        
        dialog = xbmcgui.Dialog()		
        dialog.ok("Account Type: Free", "Used Today: " + str(day1_text), "Last 7 Days: " + str(week_text))

def download_play(name, url, type):
    WAITING_TIME = 7
    if type == "tv":
        data_path = os.path.join(DOWNLOAD_TV, clean_file_name(name, use_blanks=False))
        dlThread = DownloadFileThreadTV(name, url, data_path)
        download_list = ACTIVE_DOWNLOADS_TV
    else:
        data_path = os.path.join(DOWNLOAD_MOV, clean_file_name(name, use_blanks=False))
        dlThread = DownloadFileThread(name, url, data_path)
        download_list = ACTIVE_DOWNLOADS
    dlThread.start()
    wait(WAITING_TIME, "Starting Download")
    if os.path.exists(data_path):
        scan_library()
        notify = "%s,%s,%s" % ('XBMC.Notification(Added to Library',name,'4000)')
        xbmc.executebuiltin(notify)
        size = get_file_size(url)
        list_data = "%s<|>%s<|>%s" % (name, data_path, size)
        add_search_query(list_data, download_list)
        xbmc.Player().play(data_path)
    else:
        xbmcgui.Dialog().ok('Download failed', name)
	
def download_only(name, url, type):

    WAITING_TIME = 5
    if type == "tv":
        data_path = os.path.join(DOWNLOAD_TV, clean_file_name(name, use_blanks=False))
        dlThread = DownloadFileThreadTV(name, url, data_path)
        download_list = ACTIVE_DOWNLOADS_TV
    else:
        data_path = os.path.join(DOWNLOAD_MOV, clean_file_name(name, use_blanks=False))
        dlThread = DownloadFileThread(name, url, data_path)
        download_list = ACTIVE_DOWNLOADS
    dlThread.start()
    if not name.endswith("srt"):
        if mode != "wishlist search":
            wait_dl_only(WAITING_TIME, "Starting Download")
            if os.path.exists(data_path):
                notify = "%s,%s,%s" % ('XBMC.Notification(Download started',name,'4000)')
                xbmc.executebuiltin(notify)
                scan_library()
                notify = 'XBMC.Notification(Added to Library,You can play from library now,4000)'
                xbmc.executebuiltin(notify)
                size = get_file_size(url)
                list_data = "%s<|>%s<|>%s" % (name, data_path, size)
                add_search_query(list_data, download_list)

            else:
                xbmcgui.Dialog().ok('Download failed', name)
        else:
            time.sleep(6)
            if os.path.exists(data_path):
                size = get_file_size(url)
                list_data = "%s<|>%s<|>%s" % (name, data_path, size)
                add_search_query(list_data, download_list)

def download_kat(queryname, episode):
    menu_texts = []
    menu_data = []
    menu_url = []
    menu_page_url = []
    dialog = xbmcgui.Dialog()
    episode1 = episode.replace("dummy", "")
    list_name = queryname
    queryname = queryname.replace(" any", "")

    data_url = "http://kickass.to/hourlydump.txt.gz"
    data_path = os.path.join(DOWNLOAD_PATH, "kat.gz")
    if not os.path.exists(data_path):
        print "[What the Furk...XBMCHUB.COM].........daily torrent file does not exist, downloading"
        urllib.urlretrieve(data_url, data_path)
    else:
        currenttime = time.time()
        filetime = os.path.getmtime(data_path)
        diff = currenttime - filetime
        if diff > 3600:
            print "[What the Furk...XBMCHUB.COM].........over 1 hour since last torrent file, downloading"
            urllib.urlretrieve(data_url, data_path)
        else:
            print "[What the Furk...XBMCHUB.COM].........less than 1 hour since last torrent file, use current file"
    kat_list = gzip.open(data_path)
    kat_list = kat_list.read()
    search_list = kat_list.split('\n')
    for list in search_list:
        if list != '':
            list = list.split('|')
            info_hash = list[0]
            name = list[1]
            type = list[2]
            page_url = list[3]
            url_dl = list[4]
            if queryname.find(" ")>0:
                filename = queryname.lower().split(" ")
                if  filename[0] in name.lower() and filename[1] in name.lower() and episode1.lower() in name.lower() and (type == "Movies" or type == "TV"):#  and queryname[1] in name.lower() and queryepisode in name.lower()
                    menu_texts.append(name)
                    menu_data.append(info_hash)
                    menu_url.append(url_dl)
                    menu_page_url.append(page_url)
            else:
                filename = queryname.lower()
                if  filename in name.lower() and episode1.lower() in name.lower() and (type == "Movies" or type == "TV"):
                    menu_texts.append(name)
                    menu_data.append(info_hash)
                    menu_url.append(url_dl)
                    menu_page_url.append(page_url)
			
    if len(menu_data) == 0:
        if mode != "wishlist search":
            dialog = xbmcgui.Dialog()
            dialog.ok("No torrents found", "The search was unable to find any torrents", "%s %s" % (queryname, episode1))
            return (None, None)
    else:
        if mode == "wishlist search":
            if len(menu_data) == 0:
                return (None, None)
            else:
                menu_id = 0
                info_hash = str(menu_data[menu_id])
                name = str(menu_texts[menu_id])
                add_download(name, info_hash)
                action = "newtorrents"
                list_data = "%s<|>%s<|>%s" % (list_name, action, episode)
                remove_search_query(list_data, WISHLIST)
                add_search_query(list_data, WISHLIST_FINISHED)
        else:
            menu_id = dialog.select('Select Torrent', menu_texts)
            if(menu_id < 0):
                return (None, None)
                dialog.close()
            else:	
                info_hash = str(menu_data[menu_id])
                name = str(menu_texts[menu_id])
                add_download(name, info_hash)

		
def download_meta_zip():
    menu_data = ["",
                  "http://wtf.gosub.dk/low.zip",
                  "http://wtf.gosub.dk/medium.zip",
                  "http://wtf.gosub.dk/high.zip",
                  "http://wtf.gosub.dk/medium.zip"]
    menu_texts = ["Don't download",
                 "Download low quality images [123MB]",
                 "Download mid quality images [210MB]",
                 "Download high quality images [508MB]",
                 "Download maximum quality images [722MB]"]
    data_url = "http://wtf.gosub.dk/data-338438.zip"
    
    dialog = xbmcgui.Dialog() 
    menu_id = dialog.select('Select file', menu_texts)
    if menu_id < 1:
        return
    
    ADDON.setSetting('meta_quality', value=str(menu_id + 1))
    
    try:
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Searching for files')
        
        meta_url = menu_data[menu_id]
        xbmc.log("[What the Furk...XBMCHUB.COM] Downloading meta...")
        meta_path = os.path.join(DOWNLOAD_PATH, "meta.zip")
        download(meta_url, meta_path, pDialog)
        xbmc.log("[What the Furk...XBMCHUB.COM] Extracting meta...")
        xbmc.executebuiltin("XBMC.Extract(%s , %s)" % (meta_path, META_PATH))
        xbmc.log("[What the Furk...XBMCHUB.COM] ...done!")
        data_path = os.path.join(DOWNLOAD_PATH, "data.zip")
        download(data_url, data_path, pDialog)
        xbmc.executebuiltin("XBMC.Extract(%s , %s)" % (data_path, META_PATH))
        xbmc.log("[What the Furk...XBMCHUB.COM] All done!")
    except:
        dialog.ok("Setup meta data", "Unable to reach the host server.")
    
def register_account():
    keyboard = xbmc.Keyboard('', 'Username')
    keyboard.doModal()
    username = None
    if keyboard.isConfirmed():
        username = keyboard.getText()
    if username == None:
        return False

    password = None
    keyboard = xbmc.Keyboard('', 'Password')
    keyboard.doModal()
    if keyboard.isConfirmed():
        password = keyboard.getText()
    if password == None:
        return False
     
    email = None
    keyboard = xbmc.Keyboard('', 'E-mail')
    keyboard.doModal()
    if keyboard.isConfirmed():
        email = keyboard.getText()
    if email == None:
        return False
        
    dialog = xbmcgui.Dialog()
    response = FURK.reg(username, password, password, email)
    
    if response['status'] == 'ok':
        ADDON.setSetting('furk_user', value=username)
        ADDON.setSetting('furk_pass', value=password)
        dialog.ok("Registration", "Registration formula completed.", "In order to complete the registration you need to", "click the confirmation link sent to your email.")    
        return True
    else:
        errors = response['errors']
        for key in errors.keys():
            dialog.ok("Registration error", "%s: %s" % (key, errors[key]))
        return register_account()


def get_subscriptions():
    try:
        content = read_from_file(SUBSCRIPTION_FILE)
        lines = content.split('\n')
        
        for line in lines:
            data = line.split('\t')
            if len(data) == 2:
                if data[1].startswith('tt'):
                    tv_show_name = clean_file_name(data[0].split('(')[0][:-1])
                    tv_show_imdb = data[1]
                    tv_show_mode = "strm tv show dialog"
                    create_tv_show_strm_files(tv_show_name, tv_show_imdb, tv_show_mode, TV_SHOWS_PATH)
                else:
                    mode = data[1]
                    items = get_menu_items(name, mode, "", "")
                    
                    for (url, li, isFolder) in items:
                        paramstring = url.replace(sys.argv[0], '')
                        params = get_params(paramstring)
                        movie_name = urllib.unquote_plus(params["name"])
                        movie_data = urllib.unquote_plus(params["name"])
                        movie_imdb = urllib.unquote_plus(params["imdb_id"])
                        movie_mode = "strm movie dialog"
                        create_strm_file(movie_name, movie_data, movie_imdb, movie_mode, MOVIES_PATH)
        xbmc.executebuiltin('UpdateLibrary(video)')
                    
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] Failed to fetch subscription")

def subscription_index(name, mode):
    try:
        content = read_from_file(SUBSCRIPTION_FILE)
        line = str(name) + '\t' + str(mode)
        lines = content.split('\n')
        index = lines.index(line)
        return index
    except:
        return -1 #Not subscribed

def subscribe(name, mode):
    if subscription_index(name, mode) >= 0:
        return
    content = str(name) + '\t' + str(mode) + '\n'
    write_to_file(SUBSCRIPTION_FILE, content, append=True)
    
def unsubscribe(name, mode):
    index = subscription_index(name, mode)
    if index >= 0:
        content = read_from_file(SUBSCRIPTION_FILE)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        
        if len(s) == 0:
            os.remove(SUBSCRIPTION_FILE)
        else:
            write_to_file(SUBSCRIPTION_FILE, s)
    
def find_search_query(query, search_file):
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        index = lines.index(query)
        return index
    except:
        return -1 #Not found

def daily_torrents():
    search_file = os.path.join(DOWNLOAD_PATH, "hourlydump.txt")
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        #index = lines.index(query)
        return lines
    except:
        return -1
    
def add_search_query(query, search_file):
    if find_search_query(query, search_file) >= 0:
        return

    if os.path.isfile(search_file):
        content = read_from_file(search_file)
    else:
        content = ""

    lines = content.split('\n')
    s = '%s\n' % query
    for line in lines:
        if len(line) > 0:
            s = s + line + '\n'
    write_to_file(search_file, s)
    
def remove_search_query(query, search_file):
    index = find_search_query(query, search_file)
    if index >= 0:
        content = read_from_file(search_file)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        write_to_file(search_file, s)
    
def create_strm_file(name, data, imdb_id, mode, dir_path):
    try:
        strm_string = create_url(name, mode, data=data, imdb_id=imdb_id)
        filename = clean_file_name("%s.strm" % name)
        path = os.path.join(dir_path, filename)
        stream_file = open(path, 'w')
        stream_file.write(strm_string)
        stream_file.close()
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] Error while creating strm file for : " + name)

	
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
                    display = "[S%.2dE%.2d] %s" % (season_number, episode_number, episode_name)
                    data = '%s<|>%s<|>%d<|>%d' % (name, episode_name, season_number, episode_number)
                    season_path = create_directory(tv_show_path, str(season_number))
                    create_strm_file(display, data, imdb_id, mode, season_path)
					

def remove_strm_file(name, dir_path):
    try:
        filename = "%s.strm" % (clean_file_name(name, use_blanks=False))
        path = os.path.join(dir_path, filename)
        os.remove(path)
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] Was unable to remove movie: %s" % (name)) 

def remove_tv_show_strm_files(name, dir_path):
    try:
        path = os.path.join(dir_path, name)
        shutil.rmtree(path) 
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] Was unable to remove TV show: %s" % (name)) 
    
def check_sources_xml(path):
    try:
        source_path = os.path.join(xbmc.translatePath('special://profile/'), 'sources.xml')
        f = open(source_path, 'r')
        content = f.read()
        f.close()
        path = str(path).replace('\\', '\\\\')
        if re.search(path, content):
            return True
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] Could not find sources.xml!")   
    return False

def setup_sources():
    xbmc.log("[What the Furk...XBMCHUB.COM] Trying to add source paths...")
    source_path = os.path.join(xbmc.translatePath('special://profile/'), 'sources.xml')
    
    try:
        f = open(source_path, 'r')
        content = f.read()
        f.close()
        r = re.search("(?i)(<sources>[\S\s]+?<video>[\S\s]+?>)\s+?(</video>[\S\s]+?</sources>)", content)
        new_content = r.group(1)
        if not check_sources_xml(MOVIES_PATH):
            new_content += '<source><name>Movies (What the Furk...XBMCHUB.COM)</name><path pathversion="1">'
            new_content += MOVIES_PATH
            new_content += '</path></source>'
        if not check_sources_xml(TV_SHOWS_PATH):
            new_content += '<source><name>TV Shows (What the Furk...XBMCHUB.COM)</name><path pathversion="1">'
            new_content += TV_SHOWS_PATH
            new_content += '</path></source>'
        new_content += r.group(2)
        
        f = open(source_path, 'w')
        f.write(new_content)
        f.close()

        dialog = xbmcgui.Dialog()
        dialog.ok("Source folders added", "To complete the setup:", " 1) Restart XBMC.", " 2) Set the content type of added sources.")
        #if dialog.yesno("Restart now?", "Do you want to restart XBMC now?"):
            #xbmc.restart()
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] Could not edit sources.xml")

def deletecachefiles():
	# Set path to What th Furk cache files
    wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
		
    for root, dirs, files in os.walk(wtf_cache_path):
        file_count = 0
        file_count += len(files)
	
    # Count files and give option to delete
        if file_count > 0:

            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete WTF Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
			
                for f in files:
    	            os.unlink(os.path.join(root, f))
                for d in dirs:
    	            shutil.rmtree(os.path.join(root, d))
					
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("Delete WTF Cache Files", "There are no cache files to delete")
	
    # Check if platform is ATV2.....if yes count files and give option to delete	
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
		file_count = 0
        file_count += len(files)
		
        if file_count > 0:

            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
			
                for f in files:
    	            os.unlink(os.path.join(root, f))
                for d in dirs:
    	            shutil.rmtree(os.path.join(root, d))
					
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("Delete Cache Files", "There are no ATV2 'Other' cache files to delete")
			
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
		file_count = 0
        file_count += len(files)
		
        if file_count > 0:

            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
			
                for f in files:
    	            os.unlink(os.path.join(root, f))
                for d in dirs:
    	            shutil.rmtree(os.path.join(root, d))
					
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("Delete Cache Files", "There are no ATV2 'LocalAndRental' cache files", "to delete")

def deletemetazip():
	# Set path to What the Furk meta downloads
    wtf_metazip_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/download'), '')
		
    for root, dirs, files in os.walk(wtf_metazip_path):
        file_count = 0
        file_count += len(files)
	
    # Count files and give option to delete
        if file_count > 0:

            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete WTF Zip Downloads", str(file_count) + " files found", "Do you want to delete them?"):
			
                for f in files:
    	            os.unlink(os.path.join(root, f))
                for d in dirs:
    	            shutil.rmtree(os.path.join(root, d))
					
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("Delete WTF Zip Downloads", "There are no files to delete")
			
def move_meta():
    root_src_dir = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/meta'), '')
    root_dst_dir = META_PATH

    dialog = xbmcgui.Dialog()
    if dialog.yesno("Do you want to copy files to:", META_PATH, "This may take a while!"):
        try:
            for src_dir, dirs, files in os.walk(root_src_dir):
                file_count = 0
                file_count += len(files)
                dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
                if not os.path.exists(dst_dir):
                    os.mkdir(dst_dir)
                for file_ in files:
                    src_file = os.path.join(src_dir, file_)
                    dst_file = os.path.join(dst_dir, file_)
                    if os.path.exists(dst_file):
                        os.remove(dst_file)
                    shutil.move(src_file, dst_dir)
            dialog = xbmcgui.Dialog()
            dialog.ok("DONE!", root_src_dir, "is now empty")
 
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("Move meta files", "Unable to move your files", "You may need to try manually")
			
def deletepackages():
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                            
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    dialog = xbmcgui.Dialog()
                    dialog.ok("Delete Packages", "Success")
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok("Delete Packages", "Unable to delete")
			
def deletesearchlists():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete IMDB search list", "Do you want to clear the list?"):
        fo=open(IMDB_SEARCH_FILE,"wb")
		
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Furk search list", "Do you want to clear the list?"):
        fo=open(FURK_SEARCH_FILE,"wb")
		
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Furk search list", "Do you want to clear the list?"):
        fo=open(IMDB_ACTOR_FILE,"wb")
		
def deletewishlists():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Pending Wishlist", "Do you want to clear the list?"):
        fo=open(WISHLIST,"wb")
		
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Finished Wishlist", "Do you want to clear the list?"):
        fo=open(WISHLIST_FINISHED,"wb")
		
def deletemetafiles():
	# Set path to What the Furk meta files
    wtf_meta_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/meta'), '')
    for root, dirs, files in os.walk(wtf_meta_path):
        file_count = 0
        file_count += len(files)
	
    # Count files and give option to delete
        if file_count > 0:

            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete Meta Files from userdata directory", str(file_count) + " files found", "Do you want to delete them?"):
			
                for f in files:
    	            os.unlink(os.path.join(root, f))
                for d in dirs:
    	            shutil.rmtree(os.path.join(root, d))
					
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("Delete WTF Meta Files", "There are no files to delete")

def search_nzbmovie(params):
    movies = []
    count = 0
    while count < IMDB_RESULTS:
        try:
            body = nzbmovie_search(params, str(count))
            movies.extend(get_nzbmovie_search_result(body))
        except:
            xbmc.log("[What the Furk...XBMCHUB.COM] IMDB URL request timed out") 
        count = count + 250
        if len(movies) < count:
            return movies
        setView('movies', 'movies-view')    
    return movies
    setView('movies', 'movies-view')
	
def nzbmovie_search(params, start="1"):
    print params
    url = NZBMOVIE_URL + params
    print url
    body = get_url(url, cache=CACHE_PATH)
    return body
    
def get_nzbmovie_search_result(body):
    all_tr = regex_get_all(body, '<div class="release-wrapper">', '<div class="rating')
    
    movies = []
    for tr in all_tr:
        all_td = regex_get_all(tr, '<h3>', '</h3>')
        imdb_id = 'tt' + regex_from_to(all_td[0], 'NZB/', '-')
        name = regex_from_to(all_td[0], 'title">', '<').replace(':',' ')

        movies.append({'imdb_id': imdb_id, 'name': name, 'year': 'rem'})
    return movies
	

def search_imdb(params):
    movies = []
    count = 0
    while count < IMDB_RESULTS:
        try:
            body = title_search(params, str(count))
            movies.extend(get_imdb_search_result(body))
        except:
            xbmc.log("[What the Furk...XBMCHUB.COM] IMDB URL request timed out") 
        
        count = count + 250
        if len(movies) < count:
            return movies
        setView('movies', 'movies-view')    
    return movies
    setView('movies', 'movies-view')
	
def title_search(params, start="1"):
    print params
    params["view"] = VIEW
    params["start"] = start
    params["count"] = COUNT
    url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
    #print url
    body = get_url(url, cache=CACHE_PATH)
    return body
    
def get_imdb_search_result(body):
    all_tr = regex_get_all(body, '<tr class=', '</tr>')
    
    movies = []
    for tr in all_tr:
        all_td = regex_get_all(tr, '<td', '</td>')
        imdb_id = regex_from_to(all_td[1], '/title/', '/')
        name = regex_from_to(all_td[1], '/">', '</a>')
        year = regex_from_to(all_td[1], '<span class="year_type">\(', '\)')
        try:
            rating = regex_from_to(all_td[2], '<b>', '</b>')
            votes = regex_from_to(all_td[3], '\n', '\n')
        except:
            rating = ""
            votes = ""
        movies.append({'imdb_id': imdb_id, 'name': name, 'year': year, 'rating': rating, 'votes': votes})
    return movies
	
def watchlist_imdb(params):
    movies = []
    count = 0
    while count < IMDB_RESULTS:
        try:
            body = title_watchlist(params, str(count))
            movies.extend(get_imdb_watchlist_result(body))
        except:
            xbmc.log("[What the Furk...XBMCHUB.COM] IMDB URL request timed out") 
        count = count + 250
        if len(movies) < count:
            return movies
        setView('movies', 'movies-view')    
    return movies
    setView('movies', 'movies-view')
	
def title_watchlist(params, start="1"):
    print params
    params["view"] = 'compact'
    params["start"] = start
    params["count"] = COUNT
    url = "%s%s" % (IMDB_WATCHLIST, urllib.urlencode(params)) + "&sort=listorian:asc"
    print url
    body = get_url(url, cache=CACHE_PATH)
    return body
    
def get_imdb_watchlist_result(body):
    all_tr = regex_get_all(body, '<tr data-item', '</tr>')
     
    movies = []
    for tr in all_tr:
        all_td = regex_get_all(tr, '<td', 'td>')
        imdb_id = regex_from_to(all_td[1], 'title/', '/')
        name = regex_from_to(all_td[1], '/">', '</a>')
        year = regex_from_to(all_td[2], 'year">', '</td>')
        try:
            rating = regex_from_to(all_td[6], 'user_rating">', '</')
            votes = regex_from_to(all_td[7], 'num_votes">', '</')
        except:
            rating = ""
            votes = ""
        movies.append({'imdb_id': imdb_id, 'name': name, 'year': year, 'rating': rating, 'votes': votes})
    return movies
	
def customlist_imdb(list):
    movies = []
    count = 0
    while count < IMDB_RESULTS:
        try:
            body = title_customlist(list, str(count))
            movies.extend(get_customlist_result(body))
        except:
            xbmc.log("[What the Furk...XBMCHUB.COM] IMDB URL request timed out") 
        count = count + 250
        if len(movies) < count:
            return movies
        setView('movies', 'movies-view')    
    return movies
    setView('movies', 'movies-view')
	
def title_customlist(list, start="1"):
    print list
    url = IMDB_CUSTOMLIST_URL + list + "/?start=1&view=compact&sort=listorian:asc"
    print url
    body = get_url(url, cache=CACHE_PATH)
    return body
    
def get_customlist_result(body):
    all_tr = regex_get_all(body, '<td class="listorian', '</tr>')
     
    movies = []
    for tr in all_tr:
        all_td = regex_get_all(tr, '<td', 'td>')
        imdb_id = regex_from_to(all_td[1], 'title/', '/')
        name = regex_from_to(all_td[1], '/">', '</a><')
        year = regex_from_to(all_td[2], 'year">', '</')
        try:
            rating = regex_from_to(all_td[6], 'user_rating">', '</')
            votes = regex_from_to(all_td[7], 'votes">', '</')
        except:
            rating = ""
            votes = ""
        movies.append({'imdb_id': imdb_id, 'name': name, 'year': year, 'rating': rating, 'votes': votes}),
    return movies
	
def search_actors(params):
    actors = []
    body = []
    url = "%s%s" % (IMDB_ACTOR_SEARCH, urllib.urlencode(params))
    print url
    try:
        body = get_url(url, cache=CACHE_PATH)
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] IMDB URL request timed out") 
		
    all_tr = regex_get_all(body, '<tr class=', '</tr>')
    for tr in all_tr:
        all_td = regex_get_all(tr, '<td', '</td>')
        imdb_id = regex_from_to(all_td[2], 'href="/name/', '/')
        name = regex_from_to(all_td[2], '/">', '</a>')
        try:
            profession = regex_from_to(all_td[2], 'description">', ', <a href')
        except:
            profession = ""
        photo = regex_from_to(all_td[1], '<img src="', '" ')
        photo = photo.replace("54", "214").replace("74", "314").replace("CR1", "CR12")
        actors.append({'name': name, 'imdb_id': imdb_id, 'photo': photo, 'profession': profession})
    return actors

def scrape_xspf(body, id):
    all_track = regex_get_all(body, '<track>', '</track>')
    tracks = []
    for track in all_track:
        name = regex_from_to(track, '<title>', '</title>')
        location = regex_from_to(track, '<location>', '</location>')
        if (name.endswith('.mp4') or name.endswith('.avi') or name.endswith('.mkv')) and name.lower().find("sample")<0 and name.lower().find("sampz")<0:
            size = get_file_size(location)
            tracks.append({'name': "[%.2fGB] %s" % (size, name), 'location': location, 'id': id}) 
    return tracks
	
def execute_video(name, url, list_item, strm=False):
    imdb_id=list_item
    list_item = xbmcgui.ListItem(clean_file_name(name, use_blanks=False))
    poster_path = create_directory(META_PATH, META_QUALITY)
    poster_file = os.path.join(poster_path, "%s_poster.jpg" % (imdb_id))
    list_item.setThumbnailImage(poster_file)
    #list_item = set_movie_meta(list_item, imdb_id, META_PATH)
    if PLAY_MODE == 'stream':
        if mode == "strm file dialog" or strm:
            set_resolved_url(int(sys.argv[1]), name, url, imdb_id) 
        else:
            play(name, url, list_item)
    elif PLAY_MODE == 'download and play':
        if strm:
            download_and_play(name, url, play=True, handle=int(sys.argv[1]))
        else:
            download_and_play(name, url, play=True)

def get_items_in_dir(path):
    items = []
    for dirpath, dirnames, filenames in os.walk(path): 
        for subdirname in dirnames: 
            items.append(subdirname) 
        for filename in filenames:
            if filename.endswith(".strm"): 
                items.append(filename[:-5])
        
    return items

def exist_in_dir(name, path, isMovie=False):
    if isMovie:
        name = "%s.strm" % name
    item_list = os.listdir(path)
    
    for item in item_list:
        if item == name:
            return True
    return False

#Menu

def setup():
    if FIRST_TIME_STARTUP:
        dialog = xbmcgui.Dialog()
        if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.XMLbackup'):
            if dialog.yesno("What the Furk", "XML Backup addon found", "", 'Do you want to restore all settings?', "No Thanks", "Restore Settings"):
                xbmc.executebuiltin('RunPlugin(plugin://plugin.video.XMLbackup/?mode=2&url="url")')
            else:
                setup_FURK()
        else:
            setup_FURK()
			
def setup_FURK():
    dialog = xbmcgui.Dialog()
    dialog.ok("WTF BY Batch Kinkin Mikey1234","OFFICIAL FROM XBMCHUB","FOR ALL SUPPORT PLEASE JOIN US", "WWW.XBMCHUB.COM")
        
    if not FURK_ACCOUNT:
        if dialog.yesno("Setup account", "This addon requires a Furk.net account.", "What do you want to do?", '', "Use existing account", "Create new account"):
            if not register_account():
                dialog.ok("Setup account", "Account registation aborted.")
                dialog.ok("Missing information", "You need to write down your Furk.net", "login information in the addon-settings.")    
                ADDON.openSettings()
        else:
            dialog.ok("Missing information", "You need to write down your Furk.net", "login information in the addon-settings.")    
            ADDON.openSettings()     
    if dialog.yesno("Setup metadata", "This addon supports the use of metadata,", "this data can be pre-downloaded.", "Do you want to download a metadata package?"):
        download_meta_zip()
    if dialog.yesno("Setup metadata", "This addon can download metadata while you", "are browsing movie and TV show categories.", "Do you want to activate this feature?"):
        ADDON.setSetting('download_meta', value='true')
    else:
        ADDON.setSetting('download_meta', value='false')  
    if not check_sources_xml(MOVIES_PATH) or not check_sources_xml(TV_SHOWS_PATH):
        if dialog.yesno("Setup folder", "The directories used are not listed as video sources.", "Do you want to add them to sources.xml now?"):
            setup_sources()
    ADDON.setSetting('first_time_startup', value='false')


	
def main_menu():
    items = []
    items.append(create_directory_tuple('Movies', 'imdb menu'))
    items.append(create_directory_tuple('TV Shows', 'imdb tv menu'))
    items.append(create_directory_tuple('Search', 'search menu'))
    items.append(create_directory_tuple('My Files', 'my files directory menu'))
    items.append(create_directory_tuple('My People', 'people list menu'))
    items.append(create_directory_tuple('Watchlists', 'imdb list menu'))
    items.append(create_directory_tuple('Subscriptions', 'subscription menu'))
    items.append(create_directory_tuple('Account Info', 'account info'))
    items.append(create_directory_tuple('Maintenance', 'maintenance menu'))
    items.append(create_directory_tuple('[COLOR cyan]' + "View version notes" + '[/COLOR]', 'dev message'))
    return items

def imdb_similar_menu(name, data, imdb_id):
    url = "%s%s%s" % ('http://m.imdb.com/title/',imdb_id,'/similarities')
    body = get_url(url, cache=CACHE_PATH)
    body = body.replace('\n',''	).replace('(','AX').replace(')','AZ')
    all_tr = regex_from_to(body, '<section class="similarities posters">', '</section>')
    match = re.compile('<a href="/title/(.+?)/"(.+?)>(.+?)</a> AX(.+?)AZ').findall(all_tr)
    movies=[]
    movies.append({'imdb_id': imdb_id, 'name': '[COLOR cyan]' + 'IMDB USERS WHO LIKE ' + '[/COLOR]' + '[COLOR gold]' + clean_file_name(name, use_blanks=False).replace(' TV Series','').replace(' Mini-Series','') +  '[/COLOR]' + '[COLOR cyan]' + ' ALSO LIKE:' + '[/COLOR]', 'year': 'rem', 'rating': "", 'votes': "D"})
    for imdb_id,blank,name,year in match:
        movies.append({'imdb_id': imdb_id, 'name': name, 'year': year, 'rating': "", 'votes': ""})
    if data == "MOV":
        return create_movie_items(movies)
    else:
        return create_tv_show_items(movies)
	
def dvd_release_menu():
    items = []
    lists = ['Top Rentals', 'Current Releases', 'New Releases', 'Upcoming']
    for list in lists:
        items.append(create_subdirectory_tuple(list, 'dvd releases menu'))
    return items
	
def dvd_releases(list):
    items = []
    list = list.replace(' ', '_').lower()
    if list == "top_rentals":
        url = url = "%s%s%s" % ("http://api.rottentomatoes.com/api/public/v1.0/lists/dvds/",list, ".json?country=us&apikey=crcvkfzgky27e276ug8pjckt")
    else:
        url = "%s%s%s" % ("http://api.rottentomatoes.com/api/public/v1.0/lists/dvds/",list, ".json?limit=16&page=1&country=us&apikey=crcvkfzgky27e276ug8pjckt")
    body = get_url(url, cache=CACHE_PATH).strip()
    all_mov = regex_get_all(body, '{"id"', '}}')
    movies = []
    for mov in all_mov:
        try:
            imdb_id = "%s%s" % ("tt", regex_from_to(mov, 'imdb":"', '"}'))
        except:
            imdb_id = ""
        name = regex_from_to(mov, 'title":"', '","year')
        year = regex_from_to(mov, 'year":', ',"')
        rating = regex_from_to(mov, 'critics_score":', ',"')
        votes = regex_from_to(mov, 'audience_score":', '}')

        movies.append({'imdb_id': imdb_id, 'name': name, 'year': year, 'rating': rating, 'votes': votes})
    return create_movie_items(movies)
	

def search_menu():
    items = []
    items.append(create_directory_tuple('Search IMDB', 'imdb search menu'))
    items.append(create_directory_tuple('Search Furk', 'furk search menu'))
    items.append(create_directory_tuple('Search People', 'imdb actor menu'))
    return items
	
def maintenance():
    items = []
    items.append(create_directory_tuple('Update Subscriptions (scheduled for ' + ADDON.getSetting('service_time') +')', 'force subscriptions'))
    items.append(create_directory_tuple('Update Library', 'scan library'))
    items.append(create_directory_tuple('Delete Cache Files', 'delete cache'))
    if ADDON.getSetting('meta_custom_directory') == "true":
        items.append(create_directory_tuple('Move Meta Files', 'move metafiles'))
    items.append(create_directory_tuple('Delete Meta Files', 'delete metafiles'))
    items.append(create_directory_tuple('Delete Meta Zip Files', 'delete meta zip'))
    items.append(create_directory_tuple('Delete Packages', 'delete packages'))
    items.append(create_directory_tuple('Clear Search Lists', 'delete search lists'))
    items.append(create_directory_tuple('Clear Wishlists', 'delete wishlists'))
    items.append(create_directory_tuple('Toggle One-Click', 'toggle one-click'))
    return items
	
def myfiles_directory():
    items = []
    items.append(create_directory_tuple('My Files - Finished', 'my files menu'))
    items.append(create_directory_tuple('My Files - Deleted', 'my files deleted menu'))
    items.append(create_directory_tuple('Wishlist - Pending', 'wishlist pending menu'))
    items.append(create_directory_tuple('Wishlist - Finished', 'wishlist finished menu'))
    items.append(create_directory_tuple('[COLOR gold]' + ">> Run Wishlist Search <<" + '[/COLOR]', 'wishlist search'))
    items.append(create_directory_tuple('Downloaded - Movies', 'download movies menu'))
    items.append(create_directory_tuple('Downloaded - TV Episodes', 'download episodes menu'))
    items.append(create_directory_tuple('Active Downloads', 'active download menu'))
    items.append(create_directory_tuple('Failed Downloads', 'failed download menu'))
    return items
	

def imdb_menu():
    items = []
    items.append(create_movie_directory_tuple('Top Movies', 'all movies menu')) 
    items.append(create_movie_directory_tuple('New Movies', 'new movies menu'))
    items.append(create_movie_directory_tuple('Coming Soon', 'movies soon menu'))
    items.append(create_directory_tuple('DVD Releases', 'dvd release menu'))
    items.append(create_directory_tuple('Movies by Genre', 'movie genres menu')) 
    items.append(create_directory_tuple('Movies by Group', 'movie groups menu'))
    items.append(create_directory_tuple('Movies by Studio', 'movie studios menu'))
    items.append(create_directory_tuple('Scene Releases', 'nzbmovie menu'))	
    items.append(create_movie_directory_tuple('Blu-Ray at Amazon', 'blu-ray menu'))
    return items
	
def imdb_menu_tv():
    items = []
    items.append(create_directory_tuple('Top TV Shows', 'all tv shows menu'))  
    items.append(create_directory_tuple('TV shows by Genre', 'tv show genres menu'))
    items.append(create_directory_tuple('TV shows by Group', 'tv show groups menu'))	
    items.append(create_directory_tuple('Active TV Shows', 'active tv shows menu'))
    return items
	
def nzbmovie_menu():
    items = []
    items.append(create_movie_directory_tuple('Top Downloads - This Week', 'nzbweek menu'))
    items.append(create_movie_directory_tuple('Top Downloads - This Month', 'nzbmonth menu'))
    items.append(create_movie_directory_tuple('Top Downloads - This Year', 'nzbyear menu'))
    items.append(create_movie_directory_tuple('Most Requested', 'nzbwatchlist menu')) 	
    return items
	
def imdb_list_menu():
    items = []
    items.append(create_movie_directory_tuple('My Watchlist - Movies', 'watchlist menu'))
    items.append(create_directory_tuple('My Watchlist - TV Shows', 'watchlist tv menu'))
    items.append(create_movie_directory_tuple(IMDB_LISTNAME1, 'list1 menu'))
    items.append(create_movie_directory_tuple(IMDB_LISTNAME2, 'list2 menu')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME3, 'list3 menu')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME4, 'list4 menu')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME5, 'list5 menu')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME6, 'list6 menu')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME7, 'list7 menu')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME8, 'list8 menu')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME9, 'list9 menu')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME10, 'list10 menu')) 	
    return items

def movies_all_menu():
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_TOP_MOV
    params["title_type"] = "feature,documentary"
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["production_status"] = PRODUCTION_STATUS
    movies = search_imdb(params)
    return create_movie_items(movies)
	
def movies_actors_menu(name, imdb_id):
    items = []
    files = []
        
    dialog = xbmcgui.Dialog()
    filmtype_list = ["Actor","Actress", "Director", "Writer", "Producer", "Miscellaneous Crew", "Cinematographer", "Soundtrack", "Editor", "Self"]
    filmtype_list_return = ["actor", "actress", "director", "writer", "producer", "miscellaneous crew", "cinematographer", "soundtrack", "editor", "self"]
    
    filmtype_id = dialog.select(name, filmtype_list)
    if(filmtype_id < 0):
        return (None, None)
        dialog.close()
    
    type = filmtype_list_return[filmtype_id]
    url = "%s%s%s%s" % ("http://m.imdb.com/name/", imdb_id, "/filmotype/", type)
	
    body = get_url(url, cache=CACHE_PATH)
    all_tr = regex_get_all(body, '<div class="poster', '<div class="detail')
    
    movies = []
    for tr in all_tr:
        all_td = regex_get_all(tr, '<div class="title">', '/div>')
        imdb_id = regex_from_to(all_td[0], '/title/', '/')
        name = regex_from_to(all_td[0], ';">', '</a')
        year = regex_from_to(all_td[0], '</a> (', ') ').replace("(","").replace(")","").strip()
        rating = ""
        votes = ""
        exclude = regex_from_to(all_td[0], '</a> (', ') ')

        if exclude.find("(TV")<0 and exclude.find("(Shor")<0 and exclude.find("(Vid")<0:
            movies.append({'imdb_id': imdb_id, 'name': name, 'year': year, 'rating': rating, 'votes': votes})
    return create_movie_items(movies)
	
def nzbweek_menu():
    params = "Toplists/"
    movies = search_nzbmovie(params)
    return create_movie_items(movies)
	
def nzbmonth_menu():
    params = "Toplists/Downloads/Month/"
    movies = search_nzbmovie(params)
    return create_movie_items(movies)
	
def nzbyear_menu():
    params = "Toplists/Downloads/Year/"
    movies = search_nzbmovie(params)
    return create_movie_items(movies)
	
def nzbwatchlist_menu():
    params = "Toplists/Watchlist/"
    movies = search_nzbmovie(params)
    return create_movie_items(movies)
	
def watchlist_menu():
    params = {}
    params["title_type"] = "feature,documentary"
    movies = watchlist_imdb(params)
    return create_movie_items(movies)
	
def watchlist_tv_menu():
    params = {}
    params["title_type"] = "tv_series,mini_series"
    tv_shows = watchlist_imdb(params)
    return create_tv_show_items(tv_shows)

					
def list1_menu():
    list = IMDB_LIST1
    movies = customlist_imdb(list)
    return create_movie_items(movies)
	
def list2_menu():
    list = {}
    list = IMDB_LIST2
    movies = customlist_imdb(list)
    return create_movie_items(movies)
	
def list3_menu():
    list = {}
    list = IMDB_LIST3
    movies = customlist_imdb(list)
    return create_movie_items(movies)
	
def list4_menu():
    list = {}
    list = IMDB_LIST4
    movies = customlist_imdb(list)
    return create_movie_items(movies)
	
def list5_menu():
    list = {}
    list = IMDB_LIST5
    movies = customlist_imdb(list)
    return create_movie_items(movies)
	
def list6_menu():
    list = {}
    list = IMDB_LIST6
    movies = customlist_imdb(list)
    return create_movie_items(movies)
	
def list7_menu():
    list = {}
    list = IMDB_LIST7
    movies = customlist_imdb(list)
    return create_movie_items(movies)
	
def list8_menu():
    list = {}
    list = IMDB_LIST8
    movies = customlist_imdb(list)
    return create_movie_items(movies)
	
def list9_menu():
    list = {}
    list = IMDB_LIST9
    movies = customlist_imdb(list)
    return create_movie_items(movies)
	
def list10_menu():
    list = {}
    list = IMDB_LIST10
    movies = customlist_imdb(list)
    return create_movie_items(movies)
	

def movies_genres_menu():
    items = []
    genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'History', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    for genre in genres:
        items.append(create_subdirectory_tuple(genre, 'movie genre menu'))
    return items

def movies_genre_menu(genre):
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_MOV_GEN
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["title_type"] = "feature,documentary"
    params["genres"] = genre
    params["production_status"] = PRODUCTION_STATUS
    movies = search_imdb(params)
    return create_movie_items(movies)

def movies_groups_menu():
    items = []
    groups = ['Now Playing US', 'Oscar Winners', 'Oscar nominees', 'Oscar Best Picture Winners', 'Oscar Best Director Winners',
          'Golden Globe Winners', 'Golden Globe Nominees', 'National Film Registry', 'Razzie Winners', 'Top 100', 'Bottom 100']
    for group in groups:
        items.append(create_subdirectory_tuple(group, 'movie group menu'))
    return items

def movies_group_menu(group):
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_MOV_GRP
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["title_type"] = "feature,documentary"
    params["groups"] = group.replace(' ', '_')
    params["production_status"] = PRODUCTION_STATUS
    movies = search_imdb(params)
    return create_movie_items(movies)
	
def movies_studios_menu():
    items = []
    studios = ['Columbia', 'Disney', 'Dreamworks', 'Fox', 'Mgm', 'Paramount', 'Universal', 'Warner']
    for studio in studios:
        items.append(create_subdirectory_tuple(studio, 'movie studio menu'))
    return items

def movies_studio_menu(studio):
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_MOV_STU
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["title_type"] = "feature,documentary"
    params["companies"] = studio
    params["production_status"] = PRODUCTION_STATUS
    movies = search_imdb(params)
    return create_movie_items(movies)

def movies_new_menu():
    d = (date.today() - timedelta(days=NEWMOVIE_DAYS))
    params = {}
    params["release_date"] = "%s," % d
    params["sort"] = SORT_MOV_NEW
    params["title_type"] = "feature,documentary"
    params["num_votes"] = NUM_VOTES
    params["production_status"] = PRODUCTION_STATUS
    movies = search_imdb(params)
    return create_movie_items(movies)
	
def movies_soon_menu():
    from_date = (date.today() + timedelta(1))
    to_date = (from_date + timedelta(30))
    params = {}
    params["release_date"] = "%s,%s" % (from_date, to_date)
    params["title_type"] = "feature,documentary"
    movies = search_imdb(params)
    return create_movie_items(movies)
	
def blu_ray_menu():
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_BLU_RAY
    params["title_type"] = "feature,documentary"
    params["has"] = "asin-blu-ray-us"
    params["production_status"] = PRODUCTION_STATUS
    movies = search_imdb(params)
    return create_movie_items(movies)


def tv_shows_all_menu():
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_TOP_TV
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["title_type"] = "tv_series,mini_series"
    params["production_status"] = PRODUCTION_STATUS
    tv_shows = search_imdb(params)
    return create_tv_show_items(tv_shows)

def tv_shows_genres_menu():
    items = []
    genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'History', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    for genre in genres:
        items.append(create_subdirectory_tuple(genre, 'tv show genre menu'))
    return items

def tv_shows_genre_menu(genre):
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_TV_GEN
    params["title_type"] = "tv_series,mini_series"
    params["genres"] = genre
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["production_status"] = PRODUCTION_STATUS
    tv_shows = search_imdb(params)
    return create_tv_show_items(tv_shows)
	
def tv_shows_groups_menu():
    items = []
    tvgroups = ['Emmy Winners', 'Emmy Nominees', 'Golden Globe Winners', 'Golden Globe Nominees']
    for tvgroup in tvgroups:
        items.append(create_subdirectory_tuple(tvgroup, 'tv show group menu'))
    return items

def tv_shows_group_menu(tvgroup):
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_TV_GRP
    params["title_type"] = "tv_series,mini_series"
    params["groups"] = tvgroup.replace(' ', '_')
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["production_status"] = PRODUCTION_STATUS
    tv_shows = search_imdb(params)
    return create_tv_show_items(tv_shows)

def tv_shows_active_menu():
    params = {}
    params["production_status"] = "active"
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["sort"] = SORT_TV_ACT
    params["title_type"] = "tv_series,mini_series"
    tv_shows = search_imdb(params)
    return create_tv_show_items(tv_shows)
	
def tv_shows_seasons_menu(name, imdb_id):
    items = []
    info = TheTVDBInfo(imdb_id)
    episodes = info.episodes()
    
    seasons = set()
    
    for episode in episodes:
        first_aired = episode.FirstAired()
        if len(first_aired) > 0:
            d = first_aired.split('-')
            episode_date = date(int(d[0]), int(d[1]), int(d[2]))
            if UNAIRED:
                season_number = int(episode.SeasonNumber())
                seasons.add(season_number)
            else:
                if date.today() > episode_date: #####removed to allow upcoming seasons
                    season_number = int(episode.SeasonNumber())
                    seasons.add(season_number)
                
    for season in sorted(seasons):
        if META_QUALITY == 'low':
            image_base_url = 'http://thetvdb.com/banners/seasons/_cache/'
        else:
            image_base_url = 'http://thetvdb.com/banners/seasons/'
        

        poster_href = str(info.id()) + "-" + str(season) + ".jpg"		
        poster = '%s%s' % (image_base_url, poster_href)

		
        if META_QUALITY == 'low':
            image_base_url = 'http://thetvdb.com/banners/_cache/'
        else:
            image_base_url = 'http://thetvdb.com/banners/'		
        fanart_href = info.fanart()
        if len(fanart_href) > 0:
            fanart = '%s%s' % (image_base_url, fanart_href)
		
        data = "%s<|>%d" % (name, season)
        season_tuple = create_season_tuple('Season %d' % season, data, imdb_id, poster, fanart)
        items.append(season_tuple)
        setView('movies', 'tvshows-view')
    return items;
    
def tv_shows_episodes_menu(data, imdb_id):
    items = []
    info = TheTVDBInfo(imdb_id)
    data_list = data.split("<|>")
    name = data_list[0]
    season = data_list[1]
    episodes = info.episodes()
    
    name = name.split('(')[0][:-1]
    
    for episode in episodes:
###########################################################################################################################################
        if META_QUALITY == 'low':
            image_base_url = 'http://thetvdb.com/banners/_cache/'
        else:
            image_base_url = 'http://thetvdb.com/banners/'
        poster_href = episode.filename()
        if len(poster_href) > 0:
            poster = '%s%s' % (image_base_url, poster_href)
        
        fanart_href = info.fanart()
        if len(fanart_href) > 0:
            fanart = '%s%s' % (image_base_url, fanart_href)
			
        title = episode.EpisodeName()
        year = episode.FirstAired().split('-')[0]
        overview = episode.Overview()
        if episode.Rating() == "":
            rating = 5.0
        else:
            rating = episode.Rating()
        premiered = episode.FirstAired()
        genre = info.Genre()

##########################################################################################################################################		
        first_aired = episode.FirstAired()
        if len(first_aired) > 0:
            d = first_aired.split('-')
            episode_date = date(int(d[0]), int(d[1]), int(d[2]))
            if UNAIRED:
                season_number = int(episode.SeasonNumber())
                if season_number == int(season):
                    episode_number = int(episode.EpisodeNumber())
                    episode_name = episode.EpisodeName()
                    cleaned_name = clean_file_name(episode_name, use_blanks=False)
                    if date.today() > episode_date: #default text if episode has been aired
                        display = first_aired + ' - ' + "S%.2dE%.2d - %s" % (season_number, episode_number, cleaned_name)
                    elif date.today() == episode_date: #set orange font if air date is today
                        display = '[COLOR orange]' + first_aired + ' - ' + "S%.2dE%.2d - %s" % (season_number, episode_number, cleaned_name)+ '[/COLOR]'
                    elif date.today() < episode_date: #set red font if episode has not been aired
                        display = '[COLOR red]' + first_aired + ' - ' + "S%.2dE%.2d - %s" % (season_number, episode_number, cleaned_name)+ '[/COLOR]'
                    data = "%s<|>%s<|>%d<|>%d" % (name, episode_name, season_number, episode_number)
                    easyname = "S%.2d E%.2d %s" % (season_number, episode_number, name)
                    episode_tuple = create_episode_tuple(display, data, imdb_id, poster, title, year, overview, rating, premiered, genre, fanart, easyname)
                    items.append(episode_tuple)
					
            else:
                if date.today() > episode_date:
                    season_number = int(episode.SeasonNumber())
                    if season_number == int(season):
                        episode_number = int(episode.EpisodeNumber())
                        episode_name = episode.EpisodeName()
                        cleaned_name = clean_file_name(episode_name, use_blanks=False)
                        display = "S%.2dE%.2d - %s" % (season_number, episode_number, cleaned_name)
                        data = "%s<|>%s<|>%d<|>%d" % (name, episode_name, season_number, episode_number)
                        easyname = "S%.2d E%.2d %s" % (season_number, episode_number, name)
                        episode_tuple = create_episode_tuple(display, data, imdb_id, poster, title, year, overview, rating, premiered, genre, fanart, easyname)
                        items.append(episode_tuple)

    return items

def subscription_menu():
    if not os.path.isfile(SUBSCRIPTION_FILE):
        return main_menu()
    
    items = []
    s = read_from_file(SUBSCRIPTION_FILE)
    menu_items = s.split('\n')
    
    for menu_item in menu_items:
        if len(menu_item) < 3:
            break
        data = menu_item.split('\t')
        item_name = data[0]
        item_data = data[1]
        
        if item_data.startswith('tt'):
            items.append(create_tv_show_tuple(item_name, item_data))
        else:
            items.append(create_movie_directory_tuple(item_name, item_data))

    return items

def furk_search_menu():
    items = []
    items.append(create_directory_tuple('@Search...', 'furk result dialog menu'))
    
    if os.path.isfile(FURK_SEARCH_FILE):
        s = read_from_file(FURK_SEARCH_FILE)
        search_queries = s.split('\n')
        for query in search_queries:
            items.append(create_furk_search_tuple(query))

    return items

def imdb_search_menu():
    items = []
    items.append(create_directory_tuple('@Search...', 'imdb result menu'))
    
    if os.path.isfile(IMDB_SEARCH_FILE):
        s = read_from_file(IMDB_SEARCH_FILE)
        search_queries = s.split('\n')
        for query in search_queries:
            items.append(create_imdb_search_tuple(query))

    return items
	
def imdb_actor_menu():
    items = []
    items.append(create_directory_tuple('@Search...', 'imdb actor result menu'))
    
    if os.path.isfile(IMDB_ACTOR_FILE):
        s = read_from_file(IMDB_ACTOR_FILE)
        search_queries = s.split('\n')
        for query in search_queries:
            items.append(create_imdb_actorsearch_tuple(query))

    return items
	
def download_movies_menu():
    items = []
    items.append(create_directory_tuple('[COLOR gold]' + ">> Refresh <<" + '[/COLOR]', 'refresh list'))
    
    if os.path.isfile(ACTIVE_DOWNLOADS):
        s = read_from_file(ACTIVE_DOWNLOADS)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<|>')
                name = list[0]
                path = list[1]
                try:
                    size = list[2]
                    size_now = float(os.path.getsize(path))/1073741824
                    fmt_size = "%.2fGB" % float(size)
                    pct = round(100 * (float(size_now)/float(size)), 0)
                    if pct == 100:
                        pct = '[COLOR green]' + ("[%.0f%%/%s]" % (pct, fmt_size)) + '[/COLOR]'
                    else:
                        pct = '[COLOR yellow]' + ("[%.0f%%/%s]" % (pct, fmt_size)) + '[/COLOR]'
                except:
                    pct = '[COLOR green]' + ("[%.0f%%]" % (100.0/1)) + '[/COLOR]'
                    size = ""
                type = 'movie'
                items.append(create_download_file_tuple(name, path, type, pct, size))

    return items
	
def download_episodes_menu():
    items = []
    items.append(create_directory_tuple('[COLOR gold]' + ">> Refresh <<" + '[/COLOR]', 'refresh list'))
    
    if os.path.isfile(ACTIVE_DOWNLOADS_TV):
        s = read_from_file(ACTIVE_DOWNLOADS_TV)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<|>')
                name = list[0]
                path = list[1]
                try:
                    size = list[2]
                    size_now = float(os.path.getsize(path))/1073741824
                    fmt_size = "%.2fGB" % float(size)
                    pct = round(100 * (float(size_now)/float(size)), 0)
                    if pct == 100:
                        pct = '[COLOR green]' + ("[%.0f%%/%s]" % (pct, fmt_size)) + '[/COLOR]'
                    else:
                        pct = '[COLOR yellow]' + ("[%.0f%%/%s]" % (pct, fmt_size)) + '[/COLOR]'
                except:
                    pct = '[COLOR green]' + ("[%.0f%%]" % (100.0/1)) + '[/COLOR]'
                    size = ""
                type = 'tv'
                items.append(create_download_file_tuple(name, path, type, pct, size))

    return items

def people_list_menu():
    items = []
    
    if os.path.isfile(PEOPLE_LIST):
        s = read_from_file(PEOPLE_LIST)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<|>')
                name = list[0]
                imdb_id = list[1]
                photo = list[2]
                items.append(create_savedpeople_tuple(name, imdb_id, photo))

    return items
	
def wishlist_pending_menu():
    items = []
    
    if os.path.isfile(WISHLIST):
        s = read_from_file(WISHLIST)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<|>')
                name = "%s | %s | %s" % (list[0], list[1], list[2])
                action = list[1]
                pct = ""
                type = 'movie'
                size = ""
                items.append(create_download_file_tuple(name, action, type, pct, size))

    return items
	
def wishlist_finished_menu():
    items = []
    
    if os.path.isfile(WISHLIST_FINISHED):
        s = read_from_file(WISHLIST_FINISHED)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<|>')
                name = "%s | %s | %s" % (list[0], list[1], list[2])
                action = list[1]
                pct = ""
                type = 'movie'
                size = ""
                items.append(create_download_file_tuple(name, action, type, pct, size))

    return items
	
def delete_download(name, data, type):
    if type == "tv":
        data_path = os.path.join(DOWNLOAD_TV, name)
        download_list = ACTIVE_DOWNLOADS_TV
    else:
        data_path = os.path.join(DOWNLOAD_MOV, name)
        download_list = ACTIVE_DOWNLOADS
    list_data = "%s<|>%s<|>%s" % (name, data_path, data)
    print list_data
    print data_path
    if os.path.exists(data_path):
        try:
            os.remove(data_path)
            remove_search_query(list_data, download_list)
            xbmc.executebuiltin("Container.Refresh")
        except:
            print "Exception: ",str(sys.exc_info())
    else:
        print 'File not found at ',data
	
def xbmcplay(data):
    xbmc.Player().play(data)

def imdb_result_menu(query):
    if query.startswith('@'):
        query = ''
    
    keyboard = xbmc.Keyboard(query, 'Search')
    keyboard.doModal()

    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            add_search_query(query, IMDB_SEARCH_FILE)
            params = {}
            params["title"] = query
            dialog = xbmcgui.Dialog()
            if dialog.yesno("IMDB search", "What do you want to search?", "", '', "TV-shows", "Movies"):
                params["title_type"] = "feature,documentary"
                search_result = search_imdb(params)
                setView('movies', 'movies-view')
                return create_movie_items(search_result)
            else:
                params["title_type"] = "tv_series,mini_series"
                search_result = search_imdb(params)
                setView('movies', 'tvshows-view')
                return create_tv_show_items(search_result)

    #return imdb_search_menu(), []
	
def imdb_actor_result_menu(query):
    if query.startswith('@'):
        query = ''
    
    keyboard = xbmc.Keyboard(query, 'Search People')
    keyboard.doModal()

    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            add_search_query(query, IMDB_ACTOR_FILE)
            params = {}
            params["name"] = query
            search_result = search_actors(params)
            setView('movies', 'movies-view')
            return create_actor_items(search_result)
 
    #return imdb_actor_menu(), []

def episode_dialog(data, imdb_id, strm=False):
    items = []
    dialog = xbmcgui.Dialog()
    data = data.replace('[COLOR cyan]','').replace('[/COLOR]','').replace('[COLOR gold]','')
    quality_list = ["Custom Search", "Season Search", "Any",  "1080P", "720P", "HDTV", "480P", "BDRIP", "BRRIP", "DVDRIP"]
    quality_list_return = ["Custom Search", "Season", "",  "1080P", "720P", "HDTV", "480P", "BDRIP", "BRRIP", "DVDRIP"]
	
    if re.search('<|>',data):
        data = data.split('<|>')
    else:
        if re.search('$',data):
            data = data.split('$')
    tv_show_name = data[0].replace(" Mini-Series","").replace("The ","")
    episode_name = data[1]
    season_number = int(data[2])
    episode_number = int(data[3])

    season_episode = "s%.2de%.2d" % (season_number, episode_number)
    season_episode2 = "%s %dx%.2d" % (tv_show_name, season_number, episode_number)
    season_episode3 = "%s season %d" % (tv_show_name, season_number)

    tv_show_season = "%s season" % (tv_show_name)
    tv_show_episode = "%s %s" % (tv_show_name, season_episode)
    track_filter = [episode_name, season_episode, season_episode2]
	
    if not login_at_furk():
        return []
    xbmcname = str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "))	
    files = []
  
    if FURK_SEARCH_MF:
        tv_show = tv_show_name.lower().split(' ')
        mfiles = []
        my_files = FURK.file_get('0')
        mfiles = my_files.files
	
        for f in mfiles:
            if (tv_show_name.find(' ')>0 and tv_show[0] in f.name.lower() and tv_show[1] in f.name.lower()) or (tv_show_name in f.name.lower()):
                count_files = (f.files_num_video)
                name = f.name
                url = f.url_dl
                id = f.id
                size = f.size
                size = float(size)/1073741824
                size = "[%.2fGB]" % size
                text = '[COLOR gold]' + "%s %s %s [%s files]" %("MF:",size, f.name, count_files) + '[/COLOR]'
                try:
                    poster = f.ss_urls_tn[0]
                except:
                    poster = ""
                xbmcname = f.name

                mode = "t files menu"
                archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster, "")
                items.append(archive_tuple)

    if QUALITYSTYLE == "preferred":
        searchstring = "%s %s" % (tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "), TVCUSTOMQUALITY)
        files = search_furk(searchstring)
        if len(files)==0:
            notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
            xbmc.executebuiltin(notify)
            searchstring = str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "))
            files = search_furk(searchstring)
    else:
        quality_id = dialog.select("Select your preferred option", quality_list)
        quality = quality_list_return[quality_id]
    
        if(quality_id == 0):
            searchstring = tv_show_name
            keyboard = xbmc.Keyboard(searchstring, 'Custom Search')
            keyboard.doModal()
            if keyboard.isConfirmed():
                searchstring = keyboard.getText()
        elif(quality_id == 2):
            searchstring = str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "))
        elif(quality_id == 1):
            searchstring = str(season_episode3)
        else:            
            searchstring = "%s %s" % (tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "), quality)
        if(quality_id < 0):
            return (None, None)
            dialog.close()
        files = search_furk(searchstring)

    if len(files) == 0:
        if dialog.yesno("File Search", 'No files found for: ' + searchstring, "Search latest torrents?"):
            download_kat(tv_show_name, season_episode)
            return (None, None)
        else:
            return (None, None)
		
    if FURK_LIM_FS_TV:
        fs_limit = FURK_LIM_FS_NUM_TV
    else:
        fs_limit = 50
    for f in files:
        if len(f.name) > 0 and float(f.size)/1073741824 < fs_limit:
            name = f.name.encode('utf-8','ignore')
            url = f.url_dl
            id = f.id
            is_ready = f.is_ready
            info_hash = f.info_hash
            size = f.size
            size = float(size)/1073741824
            size = "[%.2fGB]" % size
            if is_ready == "1" and f.type == "video" and f.url_dl != None:
                text = '[COLOR cyan]' + "%s %s" %(size, name) + '[/COLOR]'
                try:
                    poster = f.ss_urls_tn[0]
                except:
                    poster = ""
                mode = "t files tv menu"
            else:
                text = '[COLOR red]' + "%s %s" %(size, name)+ '[/COLOR]'
                poster = ""
                id = info_hash
                mode = "add download"

            archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster, imdb_id)
            items.append(archive_tuple)
            setView('movies', 'movies-view')

    return items;

	
def strm_episode_dialog(data, imdb_id, strm=False):
    menu_texts = []
    menu_data = []
    menu_linkid = []
    menu_url_pls = []
	
    if ONECLICK_SEARCH:
        one_click_episode(data, imdb_id, strm=True)
    else:
        dialog = xbmcgui.Dialog()
        quality_list = ["Custom Search", "Season Search", "Any",  "1080P", "720P", "HDTV", "480P", "BDRIP", "BRRIP", "DVDRIP"]
        quality_list_return = ["Custom Search", "Season", "",  "1080P", "720P", "HDTV", "480P", "BDRIP", "BRRIP", "DVDRIP"]
	
        if re.search('<|>',data):
            data = data.split('<|>')
        else:
            if re.search('$',data):
                data = data.split('$')
        tv_show_name = data[0].replace(" Mini-Series","").replace("The ","")
        episode_name = data[1]
        season_number = int(data[2])
        episode_number = int(data[3])

        season_episode = "s%.2de%.2d" % (season_number, episode_number)
        season_episode2 = "%s %dx%.2d" % (tv_show_name, season_number, episode_number)
        season_episode3 = "%s season %d" % (tv_show_name, season_number)
        easyname = "S%.2d E%.2d %s" % (season_number, episode_number, tv_show_name)
        blank = None
        fanart = None
        description = None

        tv_show_season = "%s season" % (tv_show_name)
        tv_show_episode = "%s %s" % (tv_show_name, season_episode)
        track_filter = [episode_name, season_episode, season_episode2]
	
        if not login_at_furk():
            return []
			
        if FURK_SEARCH_MF:
            tv_show = tv_show_name.lower().split(' ')
            mfiles = []
            my_files = FURK.file_get('0')
            mfiles = my_files.files
	
            for f in mfiles:
                if (tv_show_name.find(' ')>0 and tv_show[0] in f.name.lower() and tv_show[1] in f.name.lower()) or (tv_show_name in f.name.lower()):
                    count_files = (f.files_num_video)
                    name = f.name
                    size = f.size
                    size = float(size)/1073741824
                    size = "[%.2fGB]" % size
                    text = '[COLOR gold]' + "%s %s %s [%s files]" %("MF:",size, f.name, count_files) + '[/COLOR]'
                    menu_texts.append(text)
                    menu_data.append(f.url_dl)
                    menu_linkid.append(f.id)
                    menu_url_pls.append(f.url_pls)
	
        files = []

        if QUALITYSTYLE == "preferred":
            searchstring = "%s %s" % (tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "), TVCUSTOMQUALITY)
            files = search_furk(searchstring)
            if files.count('"type":"video"')==0:
                notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
                xbmc.executebuiltin(notify)
                searchstring = str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "))
                files = search_furk(searchstring)
        else:
            quality_id = dialog.select("Select your preferred option", quality_list)
            quality = quality_list_return[quality_id]
    
            if(quality_id == 0):
                searchstring = tv_show_name
                keyboard = xbmc.Keyboard(searchstring, 'Custom Search')
                keyboard.doModal()
                if keyboard.isConfirmed():
                    searchstring = keyboard.getText()
            elif(quality_id == 2):
                searchstring = str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":",""))
            elif(quality_id == 1):
                searchstring = str(season_episode3)
            else:            
                searchstring = "%s %s" % (tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":",""), quality)
            if(quality_id < 0):
                return (None, None)
                dialog.close()
            files = search_furk(searchstring)

        if QUALITYSTYLE == "preferred" or (FURK_LIM_FS_TV and (quality_id != 1)):
            fs_limit = FURK_LIM_FS_NUM_TV
        else:
            fs_limit = 50
        for f in files:
            if f.type == "video" and f.url_dl != None and float(f.size)/1073741824 < fs_limit:
                name = f.name
                size = f.size
                size = float(size)/1073741824
                size = "[%.2fGB]" % size
                text = '[COLOR cyan]' + "%s %s" %(size, name) + '[/COLOR]'
                menu_texts.append(text)
                menu_data.append(f.url_dl)
                menu_linkid.append(f.id)
                menu_url_pls.append(f.url_pls)
				
        menu_texts.append("...Search Easynews")
        menu_texts.append("...Search 1Channel")
        menu_texts.append("...Search Icefilms")
        menu_texts.append("...Search latest torrents")

        menu_id = dialog.select('Select Archive', menu_texts)
        if(menu_id < 0):
            return (None, None)
            dialog.close()
        if(menu_id == len(menu_texts)-4):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.EasyNews'):
                xbmc.executebuiltin(('Container.Update(%s?name=%s&url=None&mode=13&iconimage=None&fanart=%s&series=%s&description=%s&downloadname=downloadname)' %('plugin://plugin.video.EasyNews/', blank, fanart, easyname,description)))
            else:
                dialog.ok("Addon not installed", "", "Install the EasyNews addon to use this function")
        elif(menu_id == len(menu_texts)-3):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.1channel'):
                xbmc.executebuiltin(('Container.Update(%s?mode=7000&section=tv&query=%s)' %('plugin://plugin.video.1channel/',tv_show_name)))
            else:
                dialog.ok("Addon not installed", "", "Install the 1Channel addon to use this function")
        elif(menu_id == len(menu_texts)-2):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.icefilms'):
                iurl='http%3a%2f%2fwww.icefilms.info%2f'
                iname = "%s %sx%.2d" % (tv_show_name,season_number,episode_number)
                xbmc.executebuiltin(('Container.Update(%s?mode=555&url=%s&search=%s&nextPage=%s)' %('plugin://plugin.video.icefilms/',iurl,urllib.quote(iname),"0")))
            else:
                dialog.ok("Addon not installed", "", "Install the Icefilms addon to use this function")
        elif(menu_id == len(menu_texts)-1):
            download_kat(tv_show_name, season_episode)
        else:
            id = str(menu_linkid[menu_id])
            t_file_dialog(id, imdb_id, tv_show_episode)
	
def t_file_dialog_tv(xbmcname, id, imdb_id, strm=False):
    items = []
    files = []
    dialog = xbmcgui.Dialog()
    my_files = FURK.t_file_get(id, t_files="1")
    files = my_files.files
    type = "tv"

    for f in files:
        try:
            poster = f.ss_urls_tn[0]
        except:
            poster = ""
        t_files = f.t_files

    all_tf = regex_get_all(str(t_files), "{", "'}")
    for tf in all_tf:
        all_td = regex_get_all(tf, "{", "'}")
        name = regex_from_to(str(all_td), "name': u'", "', u")
        format = name[len(name)-3:]
        url = regex_from_to(str(all_td), "url_dl': u'", "', u")
        size = regex_from_to(str(all_td), "size': u'", "'")
        size = float(size)/1073741824
        size = "[%.2fGB]" % size
        text = "[%s] %s %s" %(format, size, name)

        if name.lower().find('sample')<0 and (name.endswith('avi') or name.endswith('mp4') or name.endswith('mkv') or name.endswith('flv') or name.endswith('wmv') or (name.endswith('srt') and DOWNLOAD_SUB)):
            mode = "execute video"
            file_list_tuple = create_file_list_tuple(xbmcname, text, name, mode, url, size, poster, type, imdb_id)
            items.append(file_list_tuple)
            setView('movies', 'tvshows-view')
    return items;
			
def add_download(name, info_hash):
    dialog = xbmcgui.Dialog()
    if mode == "wishlist search":
        FURK.dl_add(info_hash)
    else:
        if dialog.yesno("Add Download", "Download this file to your Furk account?", "Success depends on number of seeders"):
            response = FURK.dl_add(info_hash)
            if response['status'] == 'ok':
                notify = 'XBMC.Notification(Download added to Furk account,Check status in My Files,3000)'
                xbmc.executebuiltin(notify)
            else:
                notify = 'XBMC.Notification(Error,Unable to add download,3000)'
                xbmc.executebuiltin(notify)
			
def add_wishlist(name, type):
    name = name.replace("(","").replace(")","")
    dialog = xbmcgui.Dialog()
    quality_list = ["Custom","Any", "1080P", "720P", "DVDSCR", "SCREENER", "BDRIP", "BRRIP", "BluRay 720P", "BluRay 1080P", "DVDRIP", "R5", "HDTV", "TELESYNC", "TS", "CAM"]
    quality_list_return = ["custom", "any","1080P", "720P", "DVDSCR", "SCREENER", "BDRIP", "BRRIP", "BluRay 720P", "BluRay 1080P", "DVDRIP", "R5", "HDTV", "TELESYNC", "TS", "CAM"]
    quality_id = dialog.select("Select your preferred quality", quality_list)
    if(quality_id == 0):
        quality = name
        keyboard = xbmc.Keyboard(quality, 'Custom Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
            quality = keyboard.getText()
    else:
        quality = quality_list_return[quality_id]
    if(quality_id < 0):
        return (None, None)
        dialog.close()
		
    action_list = ["Download","Add Stream", "Add to My Files", "Check for new torrents"]
    action_list_return = ["download","stream", "myfiles", "newtorrents"]
    action_id = dialog.select("What would you like to do?", action_list)
    action = action_list_return[action_id]
    if(action_id < 0):
        return (None, None)
        dialog.close()
    episode = type
    list_data = "%s %s<|>%s<|>%s" % (name, quality, action, episode)
    add_search_query(list_data, WISHLIST)
	
def add_people(name, data, imdb_id):
    list_data = "%s<|>%s<|>%s" % (name, data, imdb_id)
    add_search_query(list_data, PEOPLE_LIST)

def movie_dialog(data, imdb_id=None, strm=False):
    items = []
    if FURK_SEARCH_MF:
        name2 = data[:len(data)-7].replace("The ","").lower()
        mfiles = []
        my_files = FURK.file_get('0')
        mfiles = my_files.files
        name3 = name2.split(' ')
	
        for f in mfiles:
            if (name2.find(' ')>0 and name3[0] in f.name.lower() and name3[1] in f.name.lower()) or (name2 in f.name.lower()):
                count_files = (f.files_num_video)
                name = f.name
                url = f.url_dl
                id = f.id
                size = f.size
                size = float(size)/1073741824
                size = "[%.2fGB]" % size
                text = '[COLOR gold]' + "%s %s %s [%s files]" %("MF:",size, f.name, count_files) + '[/COLOR]'
                try:
                    poster = f.ss_urls_tn[0]
                except:
                    poster = ""
                xbmcname = f.name

                mode = "t files menu"
                archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster, "")
                items.append(archive_tuple)
    files = []
        
    dialog = xbmcgui.Dialog()
    quality_list = ["Any","1080P", "720P", "DVDSCR", "SCREENER", "BDRIP", "BRRIP", "BluRay 720P", "BluRay 1080P", "DVDRIP", "R5", "HDTV", "TELESYNC", "TS", "CAM"]
    quality_list_return = ["","1080P", "720P", "DVDSCR", "SCREENER", "BDRIP", "BRRIP", "BluRay 720P", "BluRay 1080P", "DVDRIP", "R5", "HDTV", "TELESYNC", "TS", "CAM"]
    
    if QUALITYSTYLE == "preferred":
            searchstring = "%s %s" % (str(data.replace("-"," ").replace(" Documentary","").replace(":"," ").replace("(","").replace(")","")), CUSTOMQUALITY)
            files = search_furk(searchstring)
            if (files.count('.mp4') + files.count('.avi') + files.count('.mkv')) == 0 and len(files) == 0:
                notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
                xbmc.executebuiltin(notify)
                files = search_furk(str(data.replace("-","").replace(" Documentary","").replace(":","").replace("(","").replace(")","")))
    else:
        quality_id = dialog.select("Select your preferred option", quality_list)
        quality = quality_list_return[quality_id]
        if(quality_id < 0):
            return (None, None)
            dialog.close()
        if(quality_id == 0):
            searchstring = str(data.replace("-"," ").replace(" Documentary","").replace(":"," ").replace("(","").replace(")",""))
        else:
            searchstring = "%s %s" % (str(data.replace("-"," ").replace(" Documentary","").replace(":"," ").replace("(","").replace(")","")), quality)
        files = search_furk(searchstring)
    xbmcname = str(data.replace("-"," ").replace(" Documentary","").replace(":"," "))
    if len(files) == 0:
        if dialog.yesno("File Search", 'No files found for: ' + searchstring, "Search latest torrents?"):
            download_kat(str(data.replace("-"," ").replace(" Documentary","").replace(":"," ")), "dummy")
            return (None, None)
        else:
            return (None, None)

    if FURK_LIM_FS:
        fs_limit = FURK_LIM_FS_NUM
    else:
        fs_limit = 50
    for f in files:
        if float(f.size)/1073741824 < fs_limit and f.type == "video" and f.video_info.find("mpeg2video")<0:
            name = f.name.encode('utf-8','ignore')
            url = f.url_dl
            id = f.id
            is_ready = f.is_ready
            info_hash = f.info_hash
            size = f.size
            size = float(size)/1073741824
            size = "[%.2fGB]" % size
            text = "%s %s" %(size, name)
            if  is_ready == "1" and f.type == "video" and f.url_dl != None:
                text = '[COLOR cyan]' + "%s %s" %(size, name) + '[/COLOR]'
                try:
                    poster = f.ss_urls_tn[0]
                except:
                    poster = ""
                mode = "t files menu"
            else:
                text = '[COLOR red]' + "%s %s" %(size, name)+ '[/COLOR]'
                poster = ""
                id = info_hash
                mode = "add download"

            archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster, imdb_id)
            items.append(archive_tuple)
            setView('movies', 'movies-view')
		
    return items;
	
def strm_movie_dialog(name, imdb_id, strm=False):
    open_playlists = True
    menu_texts = []
    menu_data = []
    menu_linkid = []
    menu_url_pls = []
    name2 = name[:len(data)-7].replace("The ","").lower()
    filename=name
		
    if ONECLICK_SEARCH:
        one_click_movie(name, imdb_id, strm=True)

    else:
        if FURK_SEARCH_MF:
            name3 = name2.split(' ')
            mfiles = []
            my_files = FURK.file_get('0')
            mfiles = my_files.files
	
            for f in mfiles:
                if (name2.find(' ')>0 and name3[0] in f.name.lower() and name3[1] in f.name.lower()) or (name2 in f.name.lower()):
                    count_files = (f.files_num_video)
                    name = f.name
                    size = f.size
                    size = float(size)/1073741824
                    size = "[%.2fGB]" % size
                    text = '[COLOR gold]' + "%s %s %s [%s files]" %("MF:",size, f.name, count_files) + '[/COLOR]'
                    menu_texts.append(text)
                    menu_data.append(f.url_dl)
                    menu_linkid.append(f.id)
                    menu_url_pls.append(f.url_pls)
					
        dialog = xbmcgui.Dialog()
        quality_list = ["Custom Search", "Any","1080P", "720P", "DVDSCR", "SCREENER", "BDRIP", "BRRIP", "BluRay 720P", "BluRay 1080P", "DVDRIP", "R5", "HDTV", "TELESYNC", "TS", "CAM"]
        quality_list_return = ["Custom","","1080P", "720P", "DVDSCR", "SCREENER", "BDRIP", "BRRIP", "BluRay 720P", "BluRay 1080P", "DVDRIP", "R5", "HDTV", "TELESYNC", "TS", "CAM"]
	
        if not login_at_furk():
            return []
		
        files = []
        if QUALITYSTYLE == "preferred":
            searchstring = "%s %s" % (str(data.replace("-"," ").replace(" Documentary","").replace(":"," ")), CUSTOMQUALITY)
            files = search_furk(searchstring)
            if files.count('"type":"video"')==0:
                notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
                xbmc.executebuiltin(notify)
                files = search_furk(str(data.replace("-","").replace(" Documentary","").replace(":","")))
        else:		
            quality_id = dialog.select("Select your preferred option", quality_list)
            quality = quality_list_return[quality_id]
            if(quality_id < 0):
                return (None, None)
                dialog.close()
            if(quality_id == 0):
                searchstring = str(data.replace("-"," ").replace(" Documentary","").replace(":"," ").replace("(","").replace(")",""))
                keyboard = xbmc.Keyboard(searchstring, 'Custom Search')
                keyboard.doModal()
                if keyboard.isConfirmed():
                    searchstring = keyboard.getText()
            elif(quality_id == 1):
                searchstring = str(data.replace("-"," ").replace(" Documentary","").replace(":"," ").replace("(","").replace(")",""))
            else:
                searchstring = "%s %s" % (str(data.replace("-"," ").replace(" Documentary","").replace(":"," ").replace("(","").replace(")","")), quality)
            files = search_furk(searchstring)
    
        if FURK_LIM_FS:
            fs_limit = FURK_LIM_FS_NUM
        else:
            fs_limit = 50
        for f in files:
            if f.type == "video" and f.url_dl != None and float(f.size)/1073741824 < fs_limit:
                name = f.name
                size = f.size
                size = float(size)/1073741824
                size = "[%.2fGB]" % size
                text = '[COLOR cyan]' + "%s %s" %(size, name) + '[/COLOR]'
                menu_texts.append(text)
                menu_data.append(f.url_dl)
                menu_linkid.append(f.id)
                menu_url_pls.append(f.url_pls)
				
        menu_texts.append("...Search Easynews")
        menu_texts.append("...Search 1Channel")
        menu_texts.append("...Search Icefilms")
        menu_texts.append("...Search MashUp")
        menu_texts.append("...Search latest torrents")

        menu_id = dialog.select('Select Archive', menu_texts)
        if(menu_id < 0):
            return (None, None)
            dialog.close()
        if(menu_id == len(menu_texts)-5):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.EasyNews'):
                xbmc.executebuiltin(('Container.Update(%s?name=%s&url=None&mode=3&iconimage=%s&fanart=%s&series=None&description=None&downloadname=downloadname)' %('plugin://plugin.video.EasyNews/',name2, iconimage,fanart)))
            else:
                dialog.ok("Addon not installed", "", "Install the EasyNews addon to use this function")
        elif(menu_id == len(menu_texts)-4):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.1channel'):
                xbmc.executebuiltin(('Container.Update(%s?mode=7000&section=&query=%s)' %('plugin://plugin.video.1channel/',name2)))
            else:
                dialog.ok("Addon not installed", "", "Install the 1Channel addon to use this function")
        elif(menu_id == len(menu_texts)-3):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.icefilms'):
                url='http%3a%2f%2fwww.icefilms.info%2f'
                xbmc.executebuiltin(('Container.Update(%s?mode=555&url=%s&search=%s&nextPage=%s)' %('plugin://plugin.video.icefilms/',url,urllib.quote_plus(name2),"0")))
            else:
                dialog.ok("Addon not installed", "", "Install the IceFilms addon to use this function")
        elif(menu_id == len(menu_texts)-2):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.movie25'):
                xbmc.executebuiltin(('Container.Update(%s?mode=4&url=%s)' %('plugin://plugin.video.movie25/',urllib.quote_plus(name.replace("The ","")))))
            else:
                dialog.ok("Addon not installed", "", "Install the MashUp addon to use this function")
        elif(menu_id == len(menu_texts)-1):
            download_kat(str(data.replace("-"," ").replace(" Documentary","").replace(":"," ")), "dummy")
        else:
            id = str(menu_linkid[menu_id])
            t_file_dialog(id, imdb_id, filename)


def view_trailer(name, imdb_id, xbmcname, strm=False):
    menu_texts = []
    menu_data = []
    menu_res = []
    menu_list_item = []
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Searching for trailer')
    dialog = xbmcgui.Dialog()
    try:
        url = "http://www.hd-trailers.net/movie/" + name
        response = get_url(url, cache=CACHE_PATH)
        match=re.compile('href="http://(.+?)" rel=(.+?)title="(.+?)">(.+?)</a></td>').findall(response) 
        if len(match)==0:
            url = "http://www.hd-trailers.net/movie/" + name.replace('and','')
            response = get_url(url, cache=CACHE_PATH)
            match=re.compile('href="http://(.+?)" rel=(.+?)title="(.+?)">(.+?)</a></td>').findall(response) 
            if len(match)==0:
                dialog.ok("Trailer Search", 'No trailers found for:', xbmcname) 
                return
        for url, info, title, res in match:
            if url.find('apple')>0:
                url = '%s|User-Agent=QuickTime' % ("http://" + url)
            elif url.find('youtube')>0:
                video_id = url.replace('www.youtube.com/watch?v=','')
                url = (
                    'plugin://plugin.video.youtube/'
                    '?action=play_video&videoid=%s' % video_id
                )
            else:
                url = "http://" + url
            if TRAILER_RESTRICT:
                if url.find('yahoo')<0 and res==TRAILER_QUALITY:
                    menu_texts.append("[%s] %s" % (res, clean_file_name(title, use_blanks=False)))
                    menu_list_item.append(clean_file_name(title, use_blanks=False))
                    menu_data.append(url)
                    menu_res.append(res)
            else:
                if url.find('yahoo')<0:
                    menu_texts.append("[%s] %s" % (res, clean_file_name(title, use_blanks=False)))
                    menu_list_item.append(clean_file_name(title, use_blanks=False))
                    menu_data.append(url)
                    menu_res.append(res)
					
        if TRAILER_ONECLICK:
            menu_id =0
        else:
            menu_id = dialog.select('Select Trailer', menu_texts)
        if(menu_id < 0):
            return (None, None)
            dialog.close()
        else:	
            url = menu_data[menu_id]
            name = menu_texts[menu_id]
            list_item = menu_list_item[menu_id]
			
        pDialog.close()
    
        if not url or not name:
            if strm:
                set_resolved_to_dummy()
            return
    
        li = xbmcgui.ListItem(list_item)
    
        execute_video(name, url, imdb_id, strm)
    except:
        dialog.ok("Trailer Search", 'No trailers found for:', xbmcname) 
        

	
def t_file_dialog_movie(xbmcname, id, imdb_id, strm=False):
    items = []
    files = []

    dialog = xbmcgui.Dialog()
    my_files = FURK.t_file_get(id, t_files="1")
    files = my_files.files

    for f in files:
        try:
            poster = f.ss_urls_tn[0]
        except:
            poster = ""
        t_files = f.t_files

    all_tf = regex_get_all(str(t_files), "{", "'}")
    for tf in all_tf:
        all_td = regex_get_all(tf, "{", "'}")
        name = regex_from_to(str(all_td), "name': u'", "', u")
        format = name[len(name)-3:]
        url = regex_from_to(str(all_td), "url_dl': u'", "', u")
        size = regex_from_to(str(all_td), "size': u'", "'")
        size = float(size)/1073741824
        size = "[%.2fGB]" % size
        text = "[%s] %s %s" %(format, size, name)

        if name.lower().find('sample')<0 and (name.endswith('avi') or name.endswith('mp4') or name.endswith('mkv') or name.endswith('flv') or name.endswith('wmv') or (name.endswith('srt') and DOWNLOAD_SUB)):
            mode = "execute video"
            type = "movie"
            file_list_tuple = create_file_list_tuple(xbmcname, text, name, mode, url, size, poster, type, imdb_id)
            items.append(file_list_tuple)
            setView('movies', 'movies-view')
    return items;

def t_file_dialog(id, imdb_id, filename, strm=True):
    menu_texts = []
    menu_data = []
    menu_size = []
    menu_list_item = []
    files = []
    dialog = xbmcgui.Dialog()
    my_files = FURK.t_file_get(id, t_files="1")
    files = my_files.files
    for f in files:
        t_files = f.t_files
    all_tf = regex_get_all(str(t_files), "{", "'}")
    for tf in all_tf:
        all_td = regex_get_all(tf, "{", "'}")
        try:
            name = regex_from_to(str(all_td), "name': u'", "', u")
        except:
            name = "file.avi"
        format = name[len(name)-3:]
        url = regex_from_to(str(all_td), "url_dl': u'", "', u")
        size = regex_from_to(str(all_td), "size': u'", "'")
        size = float(size)/1073741824
        size = "[%.2fGB]" % size
        if name.endswith('avi') or name.endswith('mp4') or name.endswith('mkv'):
            menu_texts.append("[%s] %s %s" % (format, str(size), name))
            menu_list_item.append(name)
            menu_data.append(url)
            menu_size.append(size)
		
    menu_id = dialog.select('Select file', menu_texts)
    if(menu_id < 0):
        return (None, None)
        dialog.close()
    else:	
        url = menu_data[menu_id]
        name = menu_list_item[menu_id]
        list_item = menu_list_item[menu_id]
    
        if not url or not name:
            if strm:
                set_resolved_to_dummy()
            return
    
        li = xbmcgui.ListItem(list_item)
        if LIBRARY_FORMAT:    
            execute_video(filename, url, imdb_id, strm)
        else:
            execute_video(name, url, imdb_id, strm)


def one_click_movie(name, imdb_id, strm=False):
    open_playlists = True
    quality = CUSTOMQUALITY
    dialog = xbmcgui.Dialog()
    filename=name
	
    files = []
    files = search_furk(str(data.replace("-"," ").replace(" Documentary","").replace(":","")) + '+' + quality)
    if len(files)==0:
        notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
        xbmc.executebuiltin(notify)
        files = search_furk(str(data.replace("-","").replace(" Documentary","").replace(":","")))

    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Searching for files 1-Click')
        
    tracks = []
    count = 0
    for f in files:
        if f.type == "video" and f.url_dl != None:
            if FURK_LIM_FS:
                if int(f.size)/1073741824 < FURK_LIM_FS_NUM:
                    if pDialog.iscanceled(): 
                        pDialog.close()
                        break
                    count = count + 1
                    if count > FURK_LIMIT:
                        pDialog.close()
                        break
                    percent = int(float(count * 100) / len(files))
                    text = "%s files found" % len(tracks)
                    pDialog.update(percent, text)
                    new_tracks = get_playlist_tracks(f, open_playlists=open_playlists)
                    tracks.extend(new_tracks)
					
            else:
                if pDialog.iscanceled(): 
                    pDialog.close()
                    break
                count = count + 1
                if count > FURK_LIMIT:
                    pDialog.close()
                    break
                percent = int(float(count * 100) / len(files))
                text = "%s files found" % len(tracks)
                pDialog.update(percent, text)
                new_tracks = get_playlist_tracks(f, open_playlists=open_playlists)
                tracks.extend(new_tracks)

    (url, name, id) = track_dialog(tracks)
    pDialog.close()
     
    if not url or not name:
        if strm:
            set_resolved_to_dummy()
        return
	
    if LIBRARY_FORMAT:    
        execute_video(filename, url, imdb_id, strm)
    else:
        execute_video(name, url, imdb_id, strm)
	
def one_click_episode(data, imdb_id, strm=False):
    open_playlists = True
    menu_texts = []
    menu_data = []
    menu_linkid = []
    menu_url_pls = []
    quality = TVCUSTOMQUALITY

    if re.search('<|>',data):
        data = data.split('<|>')
    else:
        if re.search('$',data):
            data = data.split('$')
    tv_show_name = data[0].replace(" Mini-Series","").replace("The ","")
    episode_name = data[1]
    season_number = int(data[2])
    episode_number = int(data[3])

    season_episode = "s%.2de%.2d" % (season_number, episode_number)
    season_episode2 = "%s %dx%.2d" % (tv_show_name, season_number, episode_number)
    season_episode3 = "%s season %d" % (tv_show_name, season_number)

    tv_show_season = "%s season" % (tv_show_name)
    tv_show_episode = "%s %s" % (tv_show_name, season_episode)
    track_filter = [episode_name, season_episode, season_episode2]
	
    files = []
    files = search_furk(str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":","")) + '+' + quality)
    if len(files)==0:
        notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
        xbmc.executebuiltin(notify)
        files = search_furk(str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":","")))

    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Searching for files 1-Click')
        
    tracks = []
    count = 0
    for f in files:
        if f.type == "video" and f.url_dl != None:
            if FURK_LIM_FS_TV:
                if int(f.size)/1073741824 < FURK_LIM_FS_NUM_TV:
                    if pDialog.iscanceled(): 
                        pDialog.close()
                        break
                    count = count + 1
                    if count > FURK_LIMIT:
                        pDialog.close()
                        break
                    percent = int(float(count * 100) / len(files))
                    text = "%s files found" % len(tracks)
                    pDialog.update(percent, text)
                    new_tracks = get_playlist_tracks(f, open_playlists=open_playlists)
                    tracks.extend(new_tracks)
					
            else:
                if pDialog.iscanceled(): 
                    pDialog.close()
                    break
                count = count + 1
                if count > FURK_LIMIT:
                    pDialog.close()
                    break
                percent = int(float(count * 100) / len(files))
                text = "%s files found" % len(tracks)
                pDialog.update(percent, text)
                new_tracks = get_playlist_tracks(f, open_playlists=open_playlists)
                tracks.extend(new_tracks)

    (url, name, id) = track_dialog(tracks)
    pDialog.close()
     
    if not url or not name:
        if strm:
            set_resolved_to_dummy()
        return
	
    li = xbmcgui.ListItem(clean_file_name(data))
    if LIBRARY_FORMAT:    
        execute_video(tv_show_episode, url, imdb_id, strm)
    else:
        execute_video(name, url, imdb_id, strm)


def furksearch_dialog(query, imdb_id=None, strm=False):
    items = []	
    files = []
    if query.startswith('@'):
        query = ''
    
    keyboard = xbmc.Keyboard(query, 'Search')
    keyboard.doModal()

    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            add_search_query(query, FURK_SEARCH_FILE)
            files = search_furk(str(query))
    xbmcname = str(query)
	
    if FURK_SEARCH_MF:
        name2 = query[:len(query)-7].replace("The ","").lower()
        mfiles = []
        my_files = FURK.file_get('0')
        mfiles = my_files.files
        name3 = name2.split(' ')
	
        for f in mfiles:
            if (name2.find(' ')>0 and name3[0] in f.name.lower() and name3[1] in f.name.lower()) or (name2 in f.name.lower()):
                count_files = (f.files_num_video)
                name = f.name
                url = f.url_dl
                id = f.id
                size = f.size
                size = float(size)/1073741824
                size = "[%.2fGB]" % size
                text = '[COLOR gold]' + "%s %s %s [%s files]" %("MF:",size, f.name, count_files) + '[/COLOR]'
                try:
                    poster = f.ss_urls_tn[0]
                except:
                    poster = ""
                xbmcname = f.name

                mode = "t files menu"
                archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster, "")
                items.append(archive_tuple)
	
    if len(files) == 0:
        dialog.ok("File Search", 'No files found for:', query) 

    for f in files:
        if f.type == "video" and f.video_info.find("mpeg2video")<0:
            name = f.name.encode('utf-8','ignore')
            url = f.url_dl
            id = f.id
            is_ready = f.is_ready
            info_hash = f.info_hash
            size = f.size
            size = float(size)/1073741824
            size = "[%.2fGB]" % size
            text = "%s %s" %(size, name)
            if is_ready == "1" and f.url_dl != None:
                text = '[COLOR cyan]' + "%s %s" %(size, name) + '[/COLOR]'
                try:
                    poster = f.ss_urls_tn[0]
                except:
                    poster = ""
                mode = "t files menu"
            else:
                text = '[COLOR red]' + "%s %s" %(size, name)+ '[/COLOR]'
                poster = os.path.join(ADDON.getAddonInfo('path'),'art','noentry.png')
                id = info_hash
                mode = "add download"

            archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster,"")
            items.append(archive_tuple)
            setView('movies', 'movies-view')
    return items;
	
def one_click_download():
    open_playlists = True
    sleep = 10
    if os.path.isfile(WISHLIST):
        s = read_from_file(WISHLIST)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<|>')
                action = list[1]
                episode = list[2]
                if episode == "dummy":
                    searchname1 = list[0]
                else:
                    searchname1 = "%s %s" % (list[0], list[2])
                searchname = searchname1.replace(" any","")
	
                if action == "newtorrents":
                    name = list[0]
                    download_kat(name, episode)
                else:	
                    files = []
                    files = search_furk(str(searchname))
                    if files.count('"type":"video"')==0:
                        if mode != "wishlist search":
                            notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
                            xbmc.executebuiltin(notify)
                    else:        
                        tracks = []
                        count = 0
                        for f in files:
                            if f.type == "video" and f.url_dl != None:
                                if FURK_LIM_FS:
                                    if int(f.size)/1073741824 < FURK_LIM_FS_NUM:
                                        new_tracks = get_playlist_tracks(f, open_playlists=open_playlists)
                                        tracks.extend(new_tracks)
					
                                else:
                                    new_tracks = get_playlist_tracks(f, open_playlists=open_playlists)
                                    tracks.extend(new_tracks)
                        try:
                            (url, name, id) = track_dialog(tracks)
                            if LIBRARY_FORMAT:
                                name = "%s.%s" % (str(searchname.lower()),name.lower()[len(name)-3:])
                            else:
                                name = name.lower()
                            if action == "download":
                                if episode == "dummy":
                                    type = "movie"
                                else:
                                    type = "tv"
                                download_only(name, url, type)
                            if action == "stream":
                                if episode == "dummy":
                                    path = MOVIES_PATH
                                else:
                                    path = TV_SHOWS_PATH
                                create_strm_file(name, url, id, "strm file dialog", path)
                            if action == "myfiles":
                                FURK.file_link(id)
                            name = list[0]
                            list_data = "%s<|>%s<|>%s" % (name, action, episode)
                            remove_search_query(list_data, WISHLIST)
                            add_search_query(list_data, WISHLIST_FINISHED)
                        except:
                            pass

                    sleep = sleep + 1				
                    time.sleep(sleep) #sleep for 10+ seconds to get around furk api call limit. 
                    print "What the Furk......sleeping for " + str(sleep) + " seconds"
        scan_library() # scan library when finished
            
def set_resolved_to_dummy():
    listitem = xbmcgui.ListItem('Dummy data to avoid error message', path=DUMMY_PATH)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def track_dialog(tracks):
    menu_texts = []
    menu_data = []
    menu_linkid = []
    for track in tracks:
        text = (track['name'])
        id = (track['id'])
        menu_texts.append(text)
        menu_data.append(track['location'])
        menu_linkid.append(track['id'])

    if len(menu_data) == 0:
        if mode != "wishlist search":
            builtin = 'XBMC.Notification(No files found,The search was unable to find any files,3000)'
            xbmc.executebuiltin(builtin)
        return (None, None)

    menu_id = 0
    if mode != "wishlist search":
        notify = 'XBMC.Notification(Starting stream,Be patient.......,5000)'
        xbmc.executebuiltin(notify)
		
    url = menu_data[menu_id]
    name = menu_texts[menu_id]
    id = menu_linkid[menu_id]
    
    return (url, name, id)


def search_furk(query, sort='cached', filter=FURK_RESULTS, moderated=FURK_MODERATED):
    query = clean_file_name(query)
    query = query.replace('\'', ' ')

    if not login_at_furk():
        return []
    
    files = []
    if type(query).__name__ == 'list':
        for q in query:
            search_result = FURK.search(q, moderated=FURK_MODERATED, filter=FURK_RESULTS)
            if search_result.query_changed == None:
                files.extend(search_result.files)
    else:
        search_result = FURK.search(query, filter=FURK_RESULTS, moderated=FURK_MODERATED)
        if search_result.query_changed == None:
            files = search_result.files
    return files
	
###################################################################	
def myfiles(unlinked, strm=False):
    items = []
	
    if not login_at_furk():
        return []
		
    files = []
    my_files = FURK.file_get(unlinked)
    files = my_files.files
	
    for f in files:
        count_files = (f.files_num_video)
        name = f.name
        url = f.url_dl
        id = f.id
        size = f.size
        size = float(size)/1073741824
        size = "[%.2fGB]" % size
        text = "%s %s [%s files]" %(size, f.name, count_files)
        try:
            poster = f.ss_urls_tn[0]
        except:
            poster = ""
        xbmcname = f.name

        mode = "t files menu"
        archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster, "")
        items.append(archive_tuple)
        setView('movies', 'movies-view')
    return items;

def myfiles_add(name, id):
    dialog = xbmcgui.Dialog()
    response = FURK.file_link(id)

    if response['status'] == 'ok':
        dialog.ok("Add to My Files", name, 'Success - Added to My Files')
    else:
        dialog.ok("Add to My Files", name, response['status']) 
    return (None, None)
    dialog.close()
	
def get_downloads(dl_status):
    downloads = str(FURK.dl_get(dl_status))
    dls_all = regex_from_to(str(downloads), "dls': ", ", u'found_dls")
    all_dls = regex_get_all(dls_all, '{', 'None}')
    
    items = []
    for dls in all_dls:
        name = regex_from_to(dls, "name': u'", "', u")
        size = regex_from_to(dls, "size': u'", "', u")
        speed = regex_from_to(dls, "speed': u'", "', u")
        downloaded = regex_from_to(dls, "have': u'", "', u")
        seeders = regex_from_to(dls, "seeders': u'", "', u")
        id = regex_from_to(dls, "id': u'", "', u")
        fail_reason = regex_from_to(dls, "fail_reason': u'", "', u")
        size = float(size)/1073741824
        size = "[%.2fGB]" % size
        if int(speed) < 1048576:
            speed = float(speed)/1024
            speed = "[%.0fkB/s]" % speed
        else:
            speed = float(speed)/1024/1024
            speed = "[%.0fMB/s]" % speed
        downloaded = downloaded + "%"
		
        mode = "delete dls"
        archive_tuple = create_dls_tuple(name, size, speed, mode, downloaded, str(id), seeders, fail_reason)
        items.append(archive_tuple)

    return items;

def myfiles_remove(name, id):
    dialog = xbmcgui.Dialog()
    response = FURK.file_unlink(id)
    if response['status'] == 'ok':
        dialog.ok("Remove from My Files", name, 'Success')
    else:
        dialog.ok("Remove from My Files", name, 'Error')
    return (None, None)
    dialog.close()
	
def myfiles_clear(name, id):
    dialog = xbmcgui.Dialog()
    response = FURK.file_clear(id)

    if response['status'] == 'ok':
        dialog.ok("Clear Deleted file", name, 'Success - File removed')
    else:
        dialog.ok("Clear Deleted file", name, response['status']) 
    return (None, None)
    dialog.close()


def myfiles_protect(name, id):
    dialog = xbmcgui.Dialog()
    is_protected = '1'
    response = FURK.file_protect(id, is_protected)
    if response['status'] == 'ok':
        dialog.ok("File Protection", name, 'Protected')
    else:
        if response['error'] == 'limit exceeded':
            dialog.ok("File Protection", name, 'Error! Your storage limit for protected files is exceeded','Current usage is ' + response['usage'] + ' GB')
        elif response['error'] == 'not premium':
            dialog.ok("File Protection", name, 'Error! This feature is for premium users only')
        elif response['status'] == 'error':
            dialog.ok("File Protection", name, response['error'])
    return (None, None)
    dialog.close()


def myfiles_unprotect(name, id):
    dialog = xbmcgui.Dialog()
    is_protected = '0'
    response = FURK.file_protect(id, is_protected)
    if response['status'] == 'ok':
        dialog.ok("File Protection", name, 'Unprotected')
    else:
        if response['error'] == 'limit exceeded':
            dialog.ok("File Protection", name, 'Error! Your storage limit for protected files is exceeded','Current usage is ' + response['usage'] + ' GB')
        elif response['error'] == 'not premium':
            dialog.ok("File Protection", name, 'Error! This feature is for premium users only')
        elif response['status'] == 'error':
            dialog.ok("File Protection", name, response['error'])
    return (None, None)
    dialog.close()
######################################################################



def remove_list_duplicates(list_to_check): 
    temp_set = {} 
    map(temp_set.__setitem__, list_to_check, []) 
    return temp_set.keys()

def filter_playlist_tracks(tracks, track_filters):
    r = []
    if type(track_filters).__name__ == 'list':
        for track in tracks:
            name = make_string_comparable(track['name'])
            for f in track_filters:
                track_filter = make_string_comparable(f)
                if name.find(track_filter) >= 0:
                    r.append(track)
                    break
    else:
        track_filter = make_string_comparable(track_filters)
        for track in tracks:
            name = make_string_comparable(track['name'])
            if name.find(track_filter) >= 0:
                r.append(track)
    return r

def make_string_comparable(s):
    s = s.lower()
    s = ''.join(e for e in s if e.isalnum())
    return s

def get_playlist_tracks(playlist_file, open_playlists=False):
    tracks = []
    size = float(playlist_file.size)/1073741824
    id = playlist_file.id
 		
    try:
        if (name.endswith('.avi') or name.endswith('.mkv') or name.endswith('.mp4')) and name.lower().find("sample")<0 and name.lower().find("sampz")<0:
            tracks = [{'name': "[%.2fGB] " % size + name, 'location': playlist_file.url_dl, 'id': playlist_file.id}]#"[%.2fGB] " % size + 
        elif open_playlists:
            playlist_url = playlist_file.url_pls
            playlist = get_url(playlist_url)
            tracks = scrape_xspf(playlist, id)#, size, prefix
    except:
        pass
    return tracks
	

def create_movie_items(movies):
    items = []
    missing_meta = []

    for movie in movies:
        if movie['year'] == "rem":
            name = movie['name']
        else:
		    name = "%s (%s)" % (movie['name'], movie['year'])
        imdb_id = movie['imdb_id']
        try:
            rating = movie['rating']
            votes = movie['votes']
        except:
            rating = '0'
            votes = '0'
        movie_tuple = create_movie_tuple(name, imdb_id, rating, votes)
        items.append(movie_tuple)
        if not meta_exist(imdb_id, META_PATH) or imdb_id==None:
            missing_meta.append(imdb_id)
    
    return items, missing_meta

def create_tv_show_items(tv_shows):
    items = []
    missing_meta = []

    for tv_show in tv_shows:
        if tv_show['year'] == "rem":
            name = tv_show['name']
        else:
            name = "%s (%s)" % (tv_show['name'], tv_show['year'])
        imdb_id = tv_show['imdb_id']
        tv_show_tuple = create_tv_show_tuple(name, imdb_id)
        items.append(tv_show_tuple)
        if not meta_exist(imdb_id, META_PATH):
            missing_meta.append(imdb_id)
    
    return items, missing_meta
	
def create_actor_items(actors):
    items = []

    for actor in actors:
        name = actor['name']
        photo = actor['photo']
        imdb_id = actor['imdb_id']
        profession = actor['profession']
        actor_tuple = create_actor_tuple(name, photo, imdb_id, profession)
        items.append(actor_tuple)
    
    return items

def create_actor_tuple(name, photo, imdb_id, profession):
    actor_url = create_url(name, "actor movies menu", imdb_id, "")
    actor_list_item = create_actor_list_item(name, photo, imdb_id, profession);
    actor_tuple = (actor_url, actor_list_item, True)
    return actor_tuple

def create_movie_tuple(name, imdb_id, rating, votes):
    if votes == 'D':
        movie_url = create_url(name.replace('IMDB USERS WHO LIKE ','').replace(' ALSO LIKE:',''), "movie dialog menu", "", imdb_id)
    else:
        movie_url = create_url(name, "movie dialog menu", "", imdb_id)
    movie_list_item = create_movie_list_item(name, imdb_id, rating, votes);
    movie_tuple = (movie_url, movie_list_item, True)
    return movie_tuple

def create_movie_directory_tuple(name, mode):
    movie_directory_url = create_url(name, mode, "", "")
    movie_directory_list_item = create_movie_directory_list_item(name, mode);
    movie_directory_tuple = (movie_directory_url, movie_directory_list_item, True)
    return movie_directory_tuple

def create_directory_tuple(name, mode):
    directory_url = create_url(name, mode, "", "")
    directory_list_item = create_directory_list_item(name, mode);
    directory_tuple = (directory_url, directory_list_item, True)
    return directory_tuple
    return directory_tuple
	
def create_subdirectory_tuple(name, mode):
    subdirectory_url = create_url(name, mode, "", "")
    subdirectory_list_item = create_sub_directory_list_item(name, mode);
    subdirectory_tuple = (subdirectory_url, subdirectory_list_item, True)
    return subdirectory_tuple

def create_tv_show_tuple(name, imdb_id):
    tv_show_url = create_url(name.replace('IMDB USERS WHO LIKE ','').replace(' ALSO LIKE:',''), "seasons menu", "", imdb_id)
    tv_show_list_item = create_tv_show_list_item(name, imdb_id);
    tv_show_tuple = (tv_show_url, tv_show_list_item, True)
    return tv_show_tuple

def create_season_tuple(name, data, imdb_id, poster, fanart):
    season_url = create_url(name, 'episodes menu', data, imdb_id)
    season_list_item = create_season_list_item(name, data, imdb_id, poster, fanart);
    season_tuple = (season_url, season_list_item, True)
    return season_tuple

def create_episode_tuple(name, data, imdb_id, poster, title, year, overview, rating, premiered, genre, fanart, easyname):
    episode_url = create_url(name, "episode dialog menu", data, imdb_id)
    episode_list_item = create_episode_list_item(name, data, imdb_id, poster, title, year, overview, rating, premiered, genre, fanart, easyname);
    episode_tuple = (episode_url, episode_list_item, True)
    return episode_tuple
	
def create_furk_search_tuple(query):
    furk_search_url = create_url(query, 'furk result dialog menu', query, "")
    furk_search_list_item = create_furk_search_list_item(query);
    furk_search_tuple = (furk_search_url, furk_search_list_item, True)
    return furk_search_tuple

def create_imdb_search_tuple(query):
    imdb_search_url = create_url(query, "imdb result menu", query, "")
    imdb_search_list_item = create_imdb_search_list_item(query);
    imdb_search_tuple = (imdb_search_url, imdb_search_list_item, True)
    return imdb_search_tuple
	
def create_imdb_actorsearch_tuple(query):
    imdb_actorsearch_url = create_url(query, "imdb actor result menu", query, "")
    imdb_actorsearch_list_item = create_imdb_actorsearch_list_item(query);
    imdb_actorsearch_tuple = (imdb_actorsearch_url, imdb_actorsearch_list_item, True)
    return imdb_actorsearch_tuple
	
def create_archive_tuple(xbmcname, text, name, mode, url, id, size, poster, imdb_id):
    archive_url = create_url(xbmcname, mode, id, imdb_id)
    archive_list_item = create_archive_list_item(xbmcname, text, name, url, id, size, poster);
    archive_tuple = (archive_url, archive_list_item, True)
    return archive_tuple
	
def create_file_list_tuple(xbmcname, text, name, mode, url, size, poster, type, imdb_id):
    if LIBRARY_FORMAT:
        file_list_url = create_url(xbmcname, mode, url, imdb_id)
    else:
        file_list_url = create_url(name, mode, url, imdb_id)
    file_list_item = create_file_list_item(xbmcname, text, name, url, size, poster, type, imdb_id);
    file_list_tuple = (file_list_url, file_list_item, True)
    return file_list_tuple
	
def create_download_file_tuple(name, path, type, pct, size):
    download_file_url = create_url(name, "play local", path, "")
    download_file_item = create_download_file_list_item(name, path, type, pct, size);
    download_file_tuple = (download_file_url, download_file_item, True)
    return download_file_tuple
	
def create_savedpeople_tuple(name, imdb_id, photo):
    people_url = create_url(name, "actor movies menu", imdb_id)
    people_item = create_people_list_item(name, imdb_id, photo);
    people_tuple = (people_url, people_item, True)
    return people_tuple
	
def create_dls_tuple(name, size, speed, mode, downloaded, id, seeders, fail_reason):
    dls_url = create_url(name, mode, id, "")
    dls_item = create_dls_list_item(name, size, speed, downloaded, id, seeders, fail_reason);
    dls_tuple = (dls_url, dls_item, True)
    return dls_tuple

def create_url(name, mode, data="", imdb_id=""):
    name = urllib.quote(str(name))
    data = urllib.quote(str(data))
    mode = str(mode)
    url = sys.argv[0] + '?name=%s&data=%s&mode=%s&imdb_id=%s' % (name, data, mode, imdb_id)
    return url
	
def create_dls_list_item(name, size, speed, downloaded, id, seeders, fail_reason):
    text = "[%s] %s [%s seeds] %s %s" % (downloaded, speed, seeders, size, name) 
    li = xbmcgui.ListItem(clean_file_name(text, use_blanks=False))
    return li
	
def create_furk_search_list_item(query):
    contextMenuItems = []
    #remove furk search
    remove_url = '%s?name=%s&mode=remove furk search' % (sys.argv[0], query)
    contextMenuItems.append(('Remove', 'XBMC.RunPlugin(%s)' % remove_url))

    li = xbmcgui.ListItem(clean_file_name(query, use_blanks=False))
    li.addContextMenuItems(contextMenuItems, True)
    return li 

def create_imdb_search_list_item(query):
    contextMenuItems = []
    #remove furk search
    remove_url = '%s?name=%s&mode=remove imdb search' % (sys.argv[0], query)
    contextMenuItems.append(('Remove', 'XBMC.RunPlugin(%s)' % remove_url))

    li = xbmcgui.ListItem(query)
    li.addContextMenuItems(contextMenuItems, True)
    return li 
	
def create_imdb_actorsearch_list_item(query):
    contextMenuItems = []
    #remove furk search
    remove_url = '%s?name=%s&mode=remove actor search' % (sys.argv[0], query)
    contextMenuItems.append(('Remove', 'XBMC.RunPlugin(%s)' % remove_url))

    li = xbmcgui.ListItem(query)
    li.addContextMenuItems(contextMenuItems, True)
    return li 

iconimage = None
def create_actor_list_item(name, photo, imdb_id, profession):
    contextMenuItems = []
    text = "%s | %s" % (name, profession)
    name = clean_file_name(name, use_blanks=False)
    actor_url = '%s?name=%s&data=%s&imdb_id=%s&mode=add people' % (sys.argv[0], urllib.quote(name), imdb_id, urllib.quote(photo))
    contextMenuItems.append(('Add to People List', 'XBMC.RunPlugin(%s)' % actor_url))
    
    li = xbmcgui.ListItem(clean_file_name(text, use_blanks=False))
    li.addContextMenuItems(contextMenuItems, replaceItems=True)
    li.setIconImage(photo)
    return li
	
def create_movie_list_item(name, imdb_id, rating, votes):
    contextMenuItems = []
    if mode == "dvd releases menu":
        ratings = '[COLOR cyan]' + "[%s: %s %s: %s]" % ("Critics", rating, "User", votes) + '[/COLOR]'
        listname = "%s - %s" % (clean_file_name(name, use_blanks=False), ratings)
    else:
        listname = clean_file_name(name, use_blanks=False)
    contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
    name_trailer = clean_file_name(name[:len(name)-7], use_blanks=False).replace("3D","").replace('.','-').replace(':','-').replace('&','and').replace(" ","-").replace("'","-").lower()
    data_trailer = imdb_id
    trailer_url = '%s?name=%s&data=%s&imdb_id=%s&mode=view trailer' % (sys.argv[0], urllib.quote(name_trailer), urllib.quote(data_trailer), urllib.quote(name))
    contextMenuItems.append(('View trailer', 'XBMC.RunPlugin(%s)' % trailer_url))
    contextMenuItems.append(('IMDB users also like...', "XBMC.Container.Update(%s?mode=similartitles menu&name=%s&data=%s&imdb_id=%s)" % (sys.argv[0], urllib.quote(name), "MOV", imdb_id ) ) )
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.EasyNews'):
        name2 = name[:len(data)-7].replace("The ","")
        contextMenuItems.append(('@Search Movie Easynews', 'XBMC.Container.Update(%s?name=%s&url=None&mode=3&iconimage=%s&fanart=%s&series=None&description=None&downloadname=downloadname)' %('plugin://plugin.video.EasyNews/',name2, iconimage,fanart)))
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.1channel'):
        name2 = name[:len(data)-7].replace("The ","")        
        contextMenuItems.append(('@Search Movie 1Channel', 'XBMC.Container.Update(%s?mode=7000&section=&query=%s)' %('plugin://plugin.video.1channel/',name2)))
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.movie25'):
        contextMenuItems.append(('@Search Movie MashUp', 'Container.Update(%s?mode=4&url=%s)' %('plugin://plugin.video.movie25/',urllib.quote_plus(name.replace("The ","")))))
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.icefilms'):
        iurl='http%3a%2f%2fwww.icefilms.info%2f'
        contextMenuItems.append(('@Search Movie Icefilms', 'Container.Update(%s?mode=555&url=%s&search=%s&nextPage=%s)' %('plugin://plugin.video.icefilms/',iurl,urllib.quote(name2),"0")))

    if exist_in_dir(clean_file_name(name), MOVIES_PATH, isMovie=True):
        remove_url = '%s?name=%s&data=%s&imdb_id=%s&mode=remove movie strm' % (sys.argv[0], urllib.quote(name), urllib.quote(name), imdb_id)
        contextMenuItems.append(('Remove from XBMC library', 'XBMC.RunPlugin(%s)' % remove_url))
    else:
        add_url = '%s?name=%s&data=%s&imdb_id=%s&mode=add movie strm' % (sys.argv[0], urllib.quote(name), urllib.quote(name), imdb_id)
        contextMenuItems.append(('Add movie to XBMC library', 'XBMC.RunPlugin(%s)' % add_url))
    name_kat = name[:len(name)-7].replace("The ","")
    data_kat = "dummy"
    kat_url = '%s?name=%s&data=%s&imdb_id=%s&mode=search kat daily' % (sys.argv[0], urllib.quote(name_kat), data_kat, imdb_id)
    contextMenuItems.append(('Search latest torrents', 'XBMC.RunPlugin(%s)' % kat_url))
	
    type = "dummy"
    wishlist_url = '%s?name=%s&data=%s&imdb_id=%s&mode=add wishlist' % (sys.argv[0], urllib.quote(name), type, imdb_id)
    contextMenuItems.append(('Add to Wishlist', 'XBMC.RunPlugin(%s)' % wishlist_url))
    name2 = name[:len(data)-7].replace("The ","")  
    li = xbmcgui.ListItem(clean_file_name(listname, use_blanks=False))
    li.addContextMenuItems(contextMenuItems, replaceItems=False)
    li = set_movie_meta(li, imdb_id, META_PATH)
    
    return li

       
def create_tv_show_list_item(name, imdb_id):
    contextMenuItems = []
    suffix = ""
    
    contextMenuItems.append(('TV Show information', 'XBMC.Action(Info)'))
    contextMenuItems.append(('IMDB users also like...', "XBMC.Container.Update(%s?mode=similartitles tv menu&name=%s&data=%s&imdb_id=%s)" % (sys.argv[0], urllib.quote(name).replace(" Mini-Series","").replace(" TV Series",""), "TV", imdb_id ) ) )
    if exist_in_dir(clean_file_name(name.split('(')[0][:-1]), TV_SHOWS_PATH):
        remove_url = '%s?data=%s&imdb_id=%s&mode=remove tv show strm' % (sys.argv[0], urllib.quote(name), imdb_id)
        contextMenuItems.append(('Remove from XBMC library', 'XBMC.RunPlugin(%s)' % remove_url))
    else:
        add_url = '%s?data=%s&imdb_id=%s&mode=add tv show strm' % (sys.argv[0], urllib.quote(name), imdb_id)
        contextMenuItems.append(('Add TV show to XBMC library', 'XBMC.RunPlugin(%s)' % add_url))
        
    if subscription_index(name, imdb_id) < 0:
        subscribe_url = '%s?name=%s&data=%s&mode=subscribe' % (sys.argv[0], urllib.quote(name), imdb_id)
        contextMenuItems.append(('Subscribe', 'XBMC.RunPlugin(%s)' % subscribe_url))
    else:
        if UNICODE_INDICATORS:
            suffix = u' \u2665'
        else:
            suffix = " (S)"
        unsubscribe_url = '%s?name=%s&data=%s&mode=unsubscribe' % (sys.argv[0], urllib.quote(name), imdb_id)
        contextMenuItems.append(('Unsubscribe', 'XBMC.RunPlugin(%s)' % unsubscribe_url))
        
    li = xbmcgui.ListItem(clean_file_name(name, use_blanks=False) + suffix)
    li.addContextMenuItems(contextMenuItems, True)
    li = set_tv_show_meta(li, imdb_id, META_PATH)
    
    return li
        
def create_season_list_item(name, data, imdb_id, poster, fanart):
    contextMenuItems = []
    data_split = data.split('<|>')
    tv_show_name = data_split[0].replace(" Mini-Series","").replace(" TV Series","")
    tv_show_name = tv_show_name[:len(tv_show_name)-7]
    season_number = data_split[1]
    show_season = "%s Season %s" % (tv_show_name, season_number)
	
    li = xbmcgui.ListItem(clean_file_name(name, use_blanks=False))
    li.addContextMenuItems(contextMenuItems, replaceItems=False)
    li.setProperty("Video", "true")
    li.setProperty("IsPlayable", "true")
    li.setThumbnailImage(poster)
    li.setProperty('fanart_image', fanart)
    return li
	
def create_archive_list_item(xbmcname, text, name, url, id, size, poster):
    contextMenuItems = []
    if mode == 'my files deleted menu':
        mf_action = '%s?name=%s&data=%s&mode=mf clear' % (sys.argv[0], urllib.quote(name), id)  
        contextMenuItems.append(('Clear deleted file', 'XBMC.RunPlugin(%s)' % mf_action))
    if mode != 'my files menu' and text.find('[COLOR gold]')<0:
        mf_action = '%s?name=%s&data=%s&mode=mf add' % (sys.argv[0], urllib.quote(name), id)  
        contextMenuItems.append(('Add to My Files', 'XBMC.RunPlugin(%s)' % mf_action))
    if mode == 'my files menu' or text.find('[COLOR gold]')==0:
        mf_action = '%s?name=%s&data=%s&mode=mf remove' % (sys.argv[0], urllib.quote(name), id)  
        contextMenuItems.append(('Remove from My Files', 'XBMC.RunPlugin(%s)' % mf_action))
    mf_action = '%s?name=%s&data=%s&mode=mf protect' % (sys.argv[0], urllib.quote(name), id)  
    contextMenuItems.append(('Protect - My Files', 'XBMC.RunPlugin(%s)' % mf_action))
    if mode == 'my files menu':
        mf_action = '%s?name=%s&data=%s&mode=mf unprotect' % (sys.argv[0], urllib.quote(name), id)  
        contextMenuItems.append(('Unprotect - My Files', 'XBMC.RunPlugin(%s)' % mf_action))
    li = xbmcgui.ListItem(clean_file_name(text, use_blanks=False))
    li.addContextMenuItems(contextMenuItems, replaceItems=False)
    li.setThumbnailImage(poster)
    return li
	
def create_file_list_item(xbmcname, text, name, url, size, poster, type, imdb_id):
    contextMenuItems = []
    if LIBRARY_FORMAT:
        filename = "%s.%s" % (xbmcname,name[len(name)-3:])
    else:
        filename = name
    if name.endswith("srt"):
        text = '[COLOR cyan]' + text + '[/COLOR]'

    download_only = '%s?name=%s&data=%s&imdb_id=%s&mode=download only' % (sys.argv[0], urllib.quote(filename), url, type)  
    contextMenuItems.append(('Download File', 'XBMC.RunPlugin(%s)' % download_only))		
    if not name.endswith("srt"): 
        download_play = '%s?name=%s&data=%s&imdb_id=%s&mode=download play' % (sys.argv[0], urllib.quote(filename), url, type)  
        contextMenuItems.append(('Download and Play', 'XBMC.RunPlugin(%s)' % download_play))
        if type == "movie":
            add_url = '%s?name=%s&data=%s&imdb_id=%s&mode=add moviefile strm' % (sys.argv[0], urllib.quote(filename), url, imdb_id)
        else:
            add_url = '%s?name=%s&data=%s&imdb_id=%s&mode=add episode strm' % (sys.argv[0], urllib.quote(filename), url, imdb_id)
        contextMenuItems.append(('Add stream to XBMC library', 'XBMC.RunPlugin(%s)' % add_url))

    li = xbmcgui.ListItem(clean_file_name(text, use_blanks=False))
    li.addContextMenuItems(contextMenuItems, replaceItems=False)
    li.setThumbnailImage(poster)
    return li
	
def create_download_file_list_item(name, path, type, pct, size):
    contextMenuItems = []
    if mode != "wishlist pending menu" and mode != "wishlist finished menu":
        delete_file = '%s?name=%s&data=%s&imdb_id=%s&mode=delete download' % (sys.argv[0], urllib.quote(name), size, type)  
        contextMenuItems.append(('Delete File', 'XBMC.RunPlugin(%s)' % delete_file))
    if mode == "wishlist pending menu" or mode == "wishlist finished menu":
        if mode == "wishlist pending menu":
            list_path = WISHLIST
        else:
            list_path = WISHLIST_FINISHED
        list_data = name.replace(" | ", "<|>")
        remove_url = '%s?name=%s&data=%s&mode=remove wishlist search' % (sys.argv[0], urllib.quote(list_data), list_path)
        contextMenuItems.append(('Remove', 'XBMC.RunPlugin(%s)' % remove_url))
    li = xbmcgui.ListItem("%s %s" % (clean_file_name(name.replace("dummy", ""), use_blanks=False), pct))
    li.addContextMenuItems(contextMenuItems, replaceItems=True)
    return li
	
def create_people_list_item(name, imdb_id, photo):
    contextMenuItems = []
    list_path = PEOPLE_LIST
    list_data = "%s<|>%s<|>%s" % (name, imdb_id, photo)
    remove_url = '%s?name=%s&data=%s&mode=remove wishlist search' % (sys.argv[0], urllib.quote(list_data), list_path)
    contextMenuItems.append(('Remove', 'XBMC.RunPlugin(%s)' % remove_url))
    li = xbmcgui.ListItem(clean_file_name(name, use_blanks=False))
    li.setIconImage(photo)
    li.addContextMenuItems(contextMenuItems, replaceItems=True)
    return li
	
series = None
description = None
blank = None
    
def create_episode_list_item(name, data, imdb_id, poster, title, year, overview, rating, premiered, genre, fanart, easyname):
    contextMenuItems = []
    data_split = data.split('<|>')
    tv_show_name = data_split[0].replace(" Mini-Series","").replace(" TV Series","").replace("The ","")
    season_number = int(data_split[2])
    episode_number = int(data_split[3])
    season_episode = "s%.2de%.2d" % (season_number, episode_number)
	
    contextMenuItems.append(('TV Show information', 'XBMC.Action(Info)'))
    data1 = str(data).replace('<|>', '$')
	
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.EasyNews'):
        contextMenuItems.append(('@Search Episode Easynews', 'XBMC.Container.Update(%s?name=%s&url=None&mode=13&iconimage=None&fanart=%s&series=%s&description=%s&downloadname=downloadname)' %('plugin://plugin.video.EasyNews/', blank, fanart, easyname,description)))
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.1channel'):
        data = data.split('<|>')
        tv_show_name = data[0].replace(" Mini-Series","")
        contextMenuItems.append(('@Search Tv 1Channel', 'XBMC.Container.Update(%s?mode=7000&section=tv&query=%s)' %('plugin://plugin.video.1channel/',tv_show_name)))
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.icefilms'):
        iurl='http%3a%2f%2fwww.icefilms.info%2f'
        iname = "%s %sx%.2d" % (tv_show_name,season_number,episode_number)
        contextMenuItems.append(('@Search Episode Icefilms', 'Container.Update(%s?mode=555&url=%s&search=%s&nextPage=%s)' %('plugin://plugin.video.icefilms/',iurl,urllib.quote(iname),"0")))

    name_kat = tv_show_name.replace("The ","")
    data_kat = season_episode
    kat_url = '%s?name=%s&data=%s&imdb_id=%s&mode=search kat daily' % (sys.argv[0], urllib.quote(name_kat), data_kat, imdb_id)
    contextMenuItems.append(('Search latest torrents', 'XBMC.RunPlugin(%s)' % kat_url))
    wishlist_url = '%s?name=%s&data=%s&imdb_id=%s&mode=add wishlist' % (sys.argv[0], urllib.quote(name_kat), data_kat, imdb_id)
    contextMenuItems.append(('Add to Wishlist', 'XBMC.RunPlugin(%s)' % wishlist_url))
    li = xbmcgui.ListItem(clean_file_name(name, use_blanks=False))
    li.addContextMenuItems(contextMenuItems, replaceItems=False)
    li.setProperty("Video", "true")
    li.setProperty("IsPlayable", "true")
    li.setInfo(type='Video', infoLabels={'title': title,
    'year': int(year),
    'genre': genre,
    'plot': overview,
    'rating': float(rating),
    'premiered': premiered})
    li.setThumbnailImage(poster)
    li.setProperty('fanart_image', fanart)

    return li
	
   
def create_movie_directory_list_item(name, mode):
    contextMenuItems = []
    suffix = ""
    
    if subscription_index(name, mode) < 0:
        subscribe_url = '%s?name=%s&data=%s&mode=subscribe' % (sys.argv[0], urllib.quote(name), mode)
        contextMenuItems.append(('Subscribe', 'XBMC.RunPlugin(%s)' % subscribe_url))
    else:
        if UNICODE_INDICATORS:
            suffix = u' \u2665'
        else:
            suffix = " (S)"
        unsubscribe_url = '%s?name=%s&data=%s&mode=unsubscribe' % (sys.argv[0], urllib.quote(name), mode)
        contextMenuItems.append(('Unsubscribe', 'XBMC.RunPlugin(%s)' % unsubscribe_url))

    li = xbmcgui.ListItem(clean_file_name(name, use_blanks=False) + suffix, thumbnailImage=os.path.join(ADDON.getAddonInfo('path'),'art',mode + '.png'))
    li.setProperty('fanart_image', fanart)
    li.addContextMenuItems(contextMenuItems, replaceItems=False)
    
    return li

def create_directory_list_item(name, mode):
    li = xbmcgui.ListItem(clean_file_name(name, use_blanks=False),thumbnailImage=os.path.join(ADDON.getAddonInfo('path'),'art',mode + '.png'))
    li.setProperty('fanart_image', fanart)
    return li
	
def create_sub_directory_list_item(name, mode):
    li = xbmcgui.ListItem(clean_file_name(name, use_blanks=False),thumbnailImage=os.path.join(ADDON.getAddonInfo('path'),'art',name + '.png'))
    li.setProperty('fanart_image', fanart)
    return li

def scan_library():
    if xbmc.getCondVisibility('Library.IsScanningVideo') == False:           
        xbmc.executebuiltin('UpdateLibrary(video)')

def clean_library():
    xbmc.executebuiltin('CleanLibrary(video)')

def get_missing_meta(missing_meta, type):
    if len(missing_meta) > 0 and DOWNLOAD_META:
        xbmc.log("[What the Furk...XBMCHUB.COM] Downloading missing %s meta data for %d files..." % (type, len(missing_meta)))
        dlThread = DownloadThread(missing_meta, type)
        dlThread.start()
        xbmc.log("[What the Furk...XBMCHUB.COM] ...meta download complete!")
    
class DownloadThread(Thread):
    def __init__(self, missing_meta, meta_type):
        self.missing_meta = missing_meta
        self.type = meta_type
        Thread.__init__(self)

    def run(self):
        if self.type == 'movies':
            for imdb_id in self.missing_meta:
                download_movie_meta(imdb_id, META_PATH)
        if self.type == 'tv shows':
            for imdb_id in self.missing_meta:
                download_tv_show_meta(imdb_id, META_PATH)
        xbmc.executebuiltin("Container.Refresh")
		

class DownloadFileThread(Thread):
    def __init__(self, name, url, data_path):
        self.data = url
        self.path = data_path
        Thread.__init__(self)

    def run(self):
        path = self.path
        data = self.data
        urllib.urlretrieve(data, path)
        notify = "%s,%s,%s" % ('XBMC.Notification(Download finished',clean_file_name(name, use_blanks=False),'5000)')
        xbmc.executebuiltin(notify)
		
class DownloadFileThreadTV(Thread):
    def __init__(self, name, url, data_path):
        self.data = url
        self.path = data_path
        Thread.__init__(self)

    def run(self):
        path = self.path
        data = self.data
        urllib.urlretrieve(data, path)
        notify = "%s,%s,%s" % ('XBMC.Notification(Download finished',clean_file_name(name, use_blanks=False),'5000)')
        xbmc.executebuiltin(notify)


def get_all_meta():
    genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
          'Fantasy', 'History', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    groups = ['Now Playing US', 'Oscar Winners', 'Oscar Nominees', 'Oscar Best Picture Winners', 'Oscar Best Director Winners',
          'Golden Globe Winners', 'Golden Globe Nominees', 'National Film Registry', 'Razzie Winners', 'Top 100', 'Bottom 100']
    tvgroups = ['Emmy Winners', 'Emmy Nominees', 'Golden Globe Winners', 'Golden Globe Nominees']
    studios = ['Columbia', 'Disney', 'Dreamworks', 'Fox', 'Mgm', 'Paramount', 'Universal', 'Warner']
		  
    xbmc.log("[What the Furk...XBMCHUB.COM] Downloading movies_all_menu...")
    items, missing_meta = movies_all_menu()
    for imdb_id in missing_meta:
            download_movie_meta(imdb_id, META_PATH)
    xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
	
    xbmc.log("[What the Furk...XBMCHUB.COM] Downloading nzbweek_menu...")
    items, missing_meta = nzbweek_menu()
    for imdb_id in missing_meta:
            download_movie_meta(imdb_id, META_PATH)
    xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
	
    xbmc.log("[What the Furk...XBMCHUB.COM] Downloading nzbweek_menu...")
    items, missing_meta = nzbmonth_menu()
    for imdb_id in missing_meta:
            download_movie_meta(imdb_id, META_PATH)
    xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
	
    xbmc.log("[What the Furk...XBMCHUB.COM] Downloading nzbweek_menu...")
    items, missing_meta = nzbyear_menu()
    for imdb_id in missing_meta:
            download_movie_meta(imdb_id, META_PATH)
    xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
	
    xbmc.log("[What the Furk...XBMCHUB.COM] Downloading nzbweek_menu...")
    items, missing_meta = nzbwatchlist_menu()
    for imdb_id in missing_meta:
            download_movie_meta(imdb_id, META_PATH)
    xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
	
    xbmc.log("[What the Furk...XBMCHUB.COM] Downloading movies_watchlist_menu...")
    items, missing_meta = watchlist_menu()
    for imdb_id in missing_meta:
            download_movie_meta(imdb_id, META_PATH)
    xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
	
    xbmc.log("[What the Furk...XBMCHUB.COM] Downloading tvshows_watchlist_menu...")
    items, missing_meta = watchlist_tv_menu()
    for imdb_id in missing_meta:
            download_tv_show_meta(imdb_id, META_PATH)
    xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
    
    for genre in genres:  
        xbmc.log("[What the Furk...XBMCHUB.COM] Downloading movies_genre_menu %s..." % genre)
        items, missing_meta = movies_genre_menu(str(genre).lower())
        for imdb_id in missing_meta:
            download_movie_meta(imdb_id, META_PATH)
        xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
		
    for group in groups:  
        xbmc.log("[What the Furk...XBMCHUB.COM] Downloading movies_group_menu %s..." % group)
        items, missing_meta = movies_group_menu(str(group).lower())
        for imdb_id in missing_meta:
            download_movie_meta(imdb_id, META_PATH)
        xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
		
    for studio in studios:  
        xbmc.log("[What the Furk...XBMCHUB.COM] Downloading movies_studio_menu %s..." % studio)
        items, missing_meta = movies_studio_menu(str(studio).lower())
        for imdb_id in missing_meta:
            download_movie_meta(imdb_id, META_PATH)
        xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
        
    xbmc.log("[What the Furk...XBMCHUB.COM] Downloading movies_new_menu...")
    items, missing_meta = movies_new_menu()
    for imdb_id in missing_meta:
                download_movie_meta(imdb_id, META_PATH)
    xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
	
    xbmc.log("[What the Furk...XBMCHUB.COM] Downloading movies_soon_menu...")
    items, missing_meta = movies_soon_menu()
    for imdb_id in missing_meta:
                download_movie_meta(imdb_id, META_PATH)
    xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
	
    xbmc.log("[What the Furk...XBMCHUB.COM] Downloading blu_ray_menu...")
    items, missing_meta = blu_ray_menu()
    for imdb_id in missing_meta:
                download_movie_meta(imdb_id, META_PATH)
    xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
    
    xbmc.log("[What the Furk...XBMCHUB.COM] Downloading tv_shows_all_menu...")
    items, missing_meta = tv_shows_all_menu()
    for imdb_id in missing_meta:
                download_tv_show_meta(imdb_id, META_PATH)
    xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
    
    for genre in genres:
        xbmc.log("[What the Furk...XBMCHUB.COM] Downloading tv_shows_genre_menu %s..." % genre)
        items, missing_meta = tv_shows_genre_menu(str(genre).lower())
        for imdb_id in missing_meta:
                download_tv_show_meta(imdb_id, META_PATH)
        xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
		
    for tvgroup in tvgroups:  
        xbmc.log("[What the Furk...XBMCHUB.COM] Downloading tv_shows_group_menu %s..." % tvgroup)
        items, missing_meta = tv_shows_group_menu(str(tvgroup).lower())
        for imdb_id in missing_meta:
            download_tv_show_meta(imdb_id, META_PATH)
        xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
     
    xbmc.log("[What the Furk...XBMCHUB.COM] Downloading tv_shows_active_menu...")
    items, missing_meta = tv_shows_active_menu()
    for imdb_id in missing_meta:
                download_tv_show_meta(imdb_id, META_PATH)
    xbmc.log("[What the Furk...XBMCHUB.COM] ...complete!")
    xbmc.log("[What the Furk...XBMCHUB.COM] META DOWNLOAD COMPLETE!")    

def setView(content, viewType):
	# set content type so library shows more views and info
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
	if ADDON.getSetting('auto-view') == 'true':
		xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
    	    
def get_menu_items(name, mode, data, imdb_id):
    enable_sort = False
    
    if mode == "main menu": #Main menu
        items = main_menu()
    elif mode == "imdb menu":
        items = imdb_menu()
    elif mode == "imdb tv menu":
        items = imdb_menu_tv()
    elif mode == "search menu":
        items = search_menu()
    elif mode == "imdb list menu":
        items = imdb_list_menu()
    elif mode == "nzbmovie menu":
        items = nzbmovie_menu()
    elif mode == "all movies menu": #all menu
        items, missing_meta = movies_all_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "actor movies menu":
        items, missing_meta = movies_actors_menu(name, data)
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT#elif mode == "test":
    elif mode == "dvd release menu": #Genres menu
        items = dvd_release_menu()
    elif mode == "dvd releases menu":
        items, missing_meta = dvd_releases(str(name).lower())
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "download movies menu": #all menu
        items = download_movies_menu()
    elif mode == "download episodes menu": #all menu
        items = download_episodes_menu()#
    elif mode == "people list menu":
        items = people_list_menu()
    elif mode == "wishlist pending menu":
        items = wishlist_pending_menu()
    elif mode == "wishlist finished menu": #all menu
        items = wishlist_finished_menu()
    elif mode == "nzbweek menu": 
        items, missing_meta = nzbweek_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "nzbmonth menu": 
        items, missing_meta = nzbmonth_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "nzbyear menu":
        items, missing_meta = nzbyear_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
		
    elif mode == "nzbwatchlist menu": 
        items, missing_meta = nzbwatchlist_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
		
    elif mode == "maintenance menu":
        items = maintenance()
		
    elif mode == "download menu":
        items = downloads()

    elif mode == "watchlist menu": #all menu
        items, missing_meta = watchlist_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list1 menu": #all menu
        items, missing_meta = list1_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list2 menu": #all menu
        items, missing_meta = list2_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list3 menu": #all menu
        items, missing_meta = list3_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list4 menu": #all menu
        items, missing_meta = list4_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list5 menu": #all menu
        items, missing_meta = list5_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list6 menu": #all menu
        items, missing_meta = list6_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list7 menu": #all menu
        items, missing_meta = list7_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list8 menu": #all menu
        items, missing_meta = list8_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list9 menu": #all menu
        items, missing_meta = list9_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list10 menu": #all menu
        items, missing_meta = list10_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "watchlist tv menu": #Genre menu
        items, missing_meta = watchlist_tv_menu()
        get_missing_meta(missing_meta, 'tv shows')
        setView('movies', 'tvshows-view')
        enable_sort = XBMC_SORT
    elif mode == "movie genres menu": #Genres menu
        items = movies_genres_menu()
    elif mode == "movie genre menu": #Genre menu
        items, missing_meta = movies_genre_menu(str(name).lower())
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "movie groups menu": #Groups menu
        items = movies_groups_menu()
    elif mode == "movie group menu": #Group menu
        items, missing_meta = movies_group_menu(str(name).lower())
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "movie studios menu": #Studios menu
        items = movies_studios_menu()
    elif mode == "movie studio menu": #Studio menu
        items, missing_meta = movies_studio_menu(str(name).lower())
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "new movies menu": #New movies menu
        items, missing_meta = movies_new_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "movies soon menu": #Coming Soon
        items, missing_meta = movies_soon_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "blu-ray menu": #blu-ray
        items, missing_meta = blu_ray_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "similartitles menu":
        items, missing_meta = imdb_similar_menu(name, data, imdb_id)
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "similartitles tv menu":
        items, missing_meta = imdb_similar_menu(name, data, imdb_id)
        get_missing_meta(missing_meta, 'tv shows')
        setView('movies', 'tvshows-view')
        enable_sort = XBMC_SORT
    elif mode == "all tv shows menu": #all menu
        items, missing_meta = tv_shows_all_menu()
        get_missing_meta(missing_meta, 'tv shows')
        setView('movies', 'tvshows-view')
        enable_sort = XBMC_SORT
    elif mode == "tv show genres menu": #Genres menu
        items = tv_shows_genres_menu()
    elif mode == "tv show genre menu": #Genre menu
        items, missing_meta = tv_shows_genre_menu(str(name).lower())
        get_missing_meta(missing_meta, 'tv shows')
        setView('movies', 'tvshows-view')
        enable_sort = XBMC_SORT
    elif mode == "tv show groups menu": #Groups menu
        items = tv_shows_groups_menu()
    elif mode == "tv show group menu": #Group menu
        items, missing_meta = tv_shows_group_menu(str(name).lower())
        get_missing_meta(missing_meta, 'tv shows')
        setView('movies', 'tvshows-view')
        enable_sort = XBMC_SORT
    elif mode == "active tv shows menu": #New movies menu
        items, missing_meta = tv_shows_active_menu()
        get_missing_meta(missing_meta, 'tv shows')
        setView('movies', 'tvshows-view')
        enable_sort = XBMC_SORT
    elif mode == "episodes menu":
        items = tv_shows_episodes_menu(data, imdb_id)
        setView('movies', 'episodes-view')
    elif mode == "seasons menu":
        items = tv_shows_seasons_menu(name, imdb_id)
        get_missing_meta(imdb_id, 'tv shows')
    elif mode == "my files directory menu":
        items = myfiles_directory()
    elif mode == "my files menu":
        items = myfiles(unlinked='0')
    elif mode == "my files deleted menu":
        items = myfiles(unlinked='1')
    elif mode == "movie dialog menu":
        items = movie_dialog(name, imdb_id)
    elif mode == "episode dialog menu":
        items = episode_dialog(data, imdb_id)
    elif mode == "t files menu":
        items = t_file_dialog_movie(name, data, imdb_id)
    elif mode == "t files tv menu":
        items = t_file_dialog_tv(name, data, imdb_id)
    elif mode == "subscription menu": #Subscription menu
        items = subscription_menu()
    elif mode == "furk search menu": #Search menu
        items = furk_search_menu()
    elif mode == "imdb search menu": #Search menu
        items = imdb_search_menu()
    elif mode == "imdb result menu":
        items, missing_meta = imdb_result_menu(data)
    elif mode == "imdb actor menu": #Search menu
        items = imdb_actor_menu()
    elif mode == "imdb actor result menu":
        items = imdb_actor_result_menu(data)
    elif mode == "furk result dialog menu":
        items = furksearch_dialog(data)
    elif mode == "active download menu":
        items = get_downloads(dl_status='active')
    elif mode == "failed download menu":
        items = get_downloads(dl_status='failed')
    else:
        items = []
        
    if enable_sort:
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)    
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)    
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)    
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)      
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
    return items

#Other

def get_params(paramstring):
    param = {}
    if len(paramstring) >= 2:
        paramstring = paramstring.replace('?', '')
        pairsofparams = paramstring.split('&')
        for p in pairsofparams:
            splitparams = p.split('=')
            if len(splitparams) == 2:
                param[splitparams[0]] = splitparams[1]            
    return param


params = get_params(sys.argv[2])

try:
    name = urllib.unquote_plus(params["name"])
except:
    name = ""
try:
    data = urllib.unquote_plus(params["data"])
except:
    data = ""
try:
    imdb_id = urllib.unquote_plus(params["imdb_id"])
except:
    imdb_id = ""
try:
    mode = urllib.unquote_plus(params["mode"])
except:
    mode = "main menu"

xbmc.log("[What the Furk...XBMCHUB.COM] mode=%s     name=%s     data=%s     imdb_id=%s" % (mode, name, data, imdb_id))

if mode.endswith('menu'):
    items = get_menu_items(name, mode, data, imdb_id)
    try:
        xbmcplugin.addDirectoryItems(int(sys.argv[1]), items, len(items))
    except:
        pass

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    setup()
    dev_message()

elif mode == "strm file dialog":
    li = xbmcgui.ListItem(name)
    execute_video(name, data, imdb_id, strm=True)
elif mode == "strm movie dialog":
    strm_movie_dialog(name, imdb_id, strm=False)
elif mode == "strm tv show dialog":
    strm_episode_dialog(data, imdb_id, strm=False)
elif mode == "play":
    execute_video(name, imdb_id)
elif mode == "remove furk search":
    remove_search_query(name, FURK_SEARCH_FILE)
    xbmc.executebuiltin("Container.Refresh")
elif mode == "remove imdb search":
    remove_search_query(name, IMDB_SEARCH_FILE)
    xbmc.executebuiltin("Container.Refresh")
	
elif mode == "remove actor search":
    remove_search_query(name, IMDB_ACTOR_FILE)
    xbmc.executebuiltin("Container.Refresh")
	
elif mode == "remove wishlist search":
    remove_search_query(name, data)
    xbmc.executebuiltin("Container.Refresh")

elif mode == "subscribe":
    subscribe(name, data)
    xbmc.executebuiltin("Container.Refresh")
elif mode == "delete cache":
    deletecachefiles()
elif mode == "delete meta zip":
    deletemetazip()
elif mode == "delete search lists":
    deletesearchlists()
elif mode == "delete packages":
    deletepackages()
elif mode == "delete wishlists":
    deletewishlists()
elif mode == "delete metafiles":
    deletemetafiles()
elif mode == "move metafiles":
    move_meta()
elif mode == "account info":
    account_info()

elif mode == "unsubscribe":
    if name.find('[') >= 0:
        name = name.split('[')[0][:-1]
    unsubscribe(name, data)
    xbmc.executebuiltin("Container.Refresh")
elif mode == "get subscriptions":
    get_subscriptions()
elif mode == "force subscriptions":
    ADDON.setSetting('service_time', str(datetime.datetime.now()).split('.')[0])
    time.sleep(2)
    get_subscriptions()
    hours_list = [2, 5, 10, 15, 24]
    hours = hours_list[settings.subscription_timer()]
    ADDON.setSetting('service_time', str(datetime.datetime.now() + timedelta(hours=hours)).split('.')[0])
    time.sleep(1)
    xbmc.executebuiltin("Container.Refresh")
    
elif mode == "add movie strm":
    create_strm_file(name, data, imdb_id, "strm movie dialog", MOVIES_PATH)
elif mode == "add moviefile strm":
    create_strm_file(name, data, imdb_id, "strm file dialog", MOVIES_PATH)
    scan_library()
elif mode == "add episode strm":
    #data = clean_file_name(data.split('(')[0][:-1])
    create_strm_file(name, data, imdb_id, "strm file dialog", TV_SHOWS_PATH)
    #list_data = "%s<|>%s" % (name, data_path)
    #add_search_query(list_data, download_list)
    #xbmc.executebuiltin("Container.Refresh")
elif mode == "one-click on":
    ADDON.setSetting('oneclick_search', value='true')
    xbmc.executebuiltin("Container.Refresh")
elif mode == "one-click off":
    ADDON.setSetting('oneclick_search', value='false')
    xbmc.executebuiltin("Container.Refresh")
elif mode == "remove movie strm":
    remove_strm_file(data, MOVIES_PATH)
elif mode == "add tv show strm":
    data = clean_file_name(data.split('(')[0][:-1])
    create_tv_show_strm_files(data, imdb_id, "strm tv show dialog", TV_SHOWS_PATH)
    #scan_library()
    #xbmc.executebuiltin("Container.Refresh")
elif mode == "remove tv show strm":
    data = clean_file_name(data.split('(')[0][:-1])
    remove_tv_show_strm_files(data, TV_SHOWS_PATH)
	
elif mode == "seasonsearch":
    #manage_myfiles_true()
    season_dialog(name, imdb_id)
	
elif mode == "mf add":
    myfiles_add(name, data)
	
elif mode =="mf clear":
    myfiles_clear(name, data)
	
elif mode == "mf remove":
    myfiles_remove(name, data)
	
elif mode == "mf protect":
    myfiles_protect(name, data)
	
elif mode == "mf unprotect":
    myfiles_unprotect(name, data)
	
elif mode == "download play":
    download_play(name, data, imdb_id)

elif mode == "download only":
    download_only(name, data, imdb_id)
	
elif mode == "execute video":
    execute_video(name, data, imdb_id, strm=False)
	
elif mode == "add download":
    add_download(name, data)#
	
elif mode == "play local":
    xbmcplay(data)
	
elif mode == "delete download":
    delete_download(name, data, imdb_id)
	
elif mode == "scan library":
    scan_library()
	
elif mode == "search kat daily":
    download_kat(name, data)
	
elif mode == "wishlist search":
    one_click_download()
	
elif mode == "add wishlist":
    add_wishlist(name, data)
	
elif mode == "add people":
    add_people(name, data, imdb_id)
	
elif mode == "refresh list":
    xbmc.executebuiltin("Container.Refresh")
	
elif mode == "toggle one-click":
    toggle_one_click()
	
elif mode == "dev message":
    ADDON.setSetting('dev_message', value='run')
    dev_message()
	
elif mode == "view trailer":
    view_trailer(name, data, imdb_id)



	



  
	


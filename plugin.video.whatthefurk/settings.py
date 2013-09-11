'''

@author: Batch
'''
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os
from common import create_directory, create_file

ADDON = xbmcaddon.Addon(id='plugin.video.whatthefurk')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk'), '')

def addon():
    return ADDON

def data_path():
    return DATA_PATH

def cache_path():
    return create_directory(DATA_PATH, "cache")

def cookie_jar():
    return create_file(DATA_PATH, "cookiejar.lwp")

def subscription_file():
    return create_file(DATA_PATH, "subsciption.list")

def imdb_search_file():
    return create_file(DATA_PATH, "imdb_search.list")
	
def imdb_actor_file():
    return create_file(DATA_PATH, "imdb_actors.list")

def downloads_file():
    return create_file(DATA_PATH, "active_downloads.list")
	
def downloads_file_tv():
    return create_file(DATA_PATH, "active_downloads_tv.list")
	
def wishlist():
    return create_file(DATA_PATH, "wishlist.list")
	
def people_list():
    return create_file(DATA_PATH, "people_list.list")
	
def wishlist_finished():
    return create_file(DATA_PATH, "wishlist_finished.list")

def furk_search_file():
    return create_file(DATA_PATH, "furk_search.list")

def download_path():
    return create_directory(DATA_PATH, "download")

def disable_dialog():
    return ADDON.getSetting('disable_dialog')

def meta_path():
    if ADDON.getSetting('meta_custom_directory') == "true":
        return ADDON.getSetting('meta_path')
    else:
        return create_directory(DATA_PATH, "meta")
		
def skip_file_browse():
    if ADDON.getSetting('skip_file_browse') == "true":
        return True
    else:
        return False
		
def show_rating():
    if ADDON.getSetting('show_rating') == "true":
        return True
    else:
        return False

def furk_moderated():
    if ADDON.getSetting('furk_moderated') == "true":
        return "yes"
    else:
        return "no"

def restrict_trailer():
    if ADDON.getSetting('restrict_trailer') == "true":
        return True
    else:
        return False
		
def trailer_quality():
    quality = ADDON.getSetting('trailer_quality')
    if quality == '0':
        return '480p'
    elif quality == '1':
        return '720p'
    else:
        return '1080p'
		
def furkdelay():
    delay = ADDON.getSetting('furkdelay')
    if delay == '0':
        return 0
    elif delay == '1':
        return 1
    elif delay == '2':
        return 2
    elif delay == '3':
        return 3
    elif delay == '4':
        return 4
    else:
        return 5
		
def trailer_one_click():
    if ADDON.getSetting('trailer_one_click') == "true":
        return True
    else:
        return False
		
def download_subtitles():
    if ADDON.getSetting('download_subtitles') == "true":
        return True
    else:
        return False
		
def check_myfiles():
    if ADDON.getSetting('check_myfiles') == "true":
        return True
    else:
        return False
		
def oneclick_search():
    if ADDON.getSetting('oneclick_search') == "true":
        return True
    else:
        return False
		
def lib_format():
    if ADDON.getSetting('lib_format') == "true":
        return True
    else:
        return False
		
def furk_playlists():
    if ADDON.getSetting('furk_playlists') == "true":
        return True
    else:
        return False
		
def show_unaired():
    if ADDON.getSetting('show_unaired') == "true":
        return True
    else:
        return False
		
def nzvmovie_url():
    return "http://www.nzbmovieseeker.com/"
  
def imdb_actors_url():
    return "http://m.imdb.com/search/name?"
		
def imdb_search_url():
    region = ADDON.getSetting('imdb_region')
    if region == '0':
        return "http://akas.imdb.com/search/title?"
    else:
        return "http://m.imdb.com/search/title?"
	
def imdb_list_url():
    region = ADDON.getSetting('imdb_region')
    if region == '0':
        return "http://akas.imdb.com/list/"
    else:
        return "http://www.imdb.com/list/"
	
def imdb_watchlist_url():
    region = ADDON.getSetting('imdb_region')
    if region == '0':
        return "http://akas.imdb.com/user/" + ADDON.getSetting('imdb_user') + "/watchlist?"
    else:
        return "http://www.imdb.com/user/" + ADDON.getSetting('imdb_user') + "/watchlist?"
	
def imdb_filter_count():
    return "1000"

def imdb_filter_status():
    return "released"

def qualitystyle():
    style = ADDON.getSetting('qualitystyle')
    if style == '0':
        return "preferred"
    else:
        return "full list"
		
def qualitystyle_tv():
    style = ADDON.getSetting('qualitystyle_tv')
    if style == '0':
        return "preferred"
    else:
        return "full list"

	
def furk_limit_result():
    limit = ADDON.getSetting('furk_limit_result')
    if limit == '0':
        return 1
    elif limit == '1':
        return 3
    elif limit == '2':
        return 5
    elif limit == '3':
        return 10
    elif limit == '4':
        return 15
    elif limit == '5':
        return 20
    elif limit == '6':
        return 25
    elif limit == '7':
        return 50
    else:
        return 25

def furk_sort():
    furk_sort = ADDON.getSetting('furk_sort')
    if furk_sort == '0':
        return 'cached'
    elif furk_sort == '1':
        return 'relevance'
    elif furk_sort == '2':
        return 'size'
    elif furk_sort == '3':
        return 'date'
    else:
        return 'cached'

def furk_results():
    furk_results = ADDON.getSetting('furk_results')
    if furk_results == '0':
        return 'all'
    elif furk_results == '1':
        return 'cached'
    else:
        return 'cached'

def custom_quality():
    quality = ADDON.getSetting('quality')
    if quality == '0':
        return 'CAM'
    elif quality == '1':
        return 'TS'
    elif quality == '2':
        return 'TELESYNC'
    elif quality == '3':
        return 'R5'
    elif quality == '4':
        return 'DVDSCR'
    elif quality == '5':
        return 'DVDRIP'
    elif quality == '6':
        return 'HDTV'
    elif quality == '7':
        return 'BRRIP'
    elif quality == '8':
        return 'BDRIP'
    elif quality == '9':
        return '480P'
    elif quality == '10':
        return '720P'
    elif quality == '11':
        return '1080P'
    elif quality == '12':
        return ''
    else:
        return '720P'
		
def preferred2():
    if ADDON.getSetting('search_quality_2') == "true":
        return True
    else:
        return False
		
def custom_quality2():
    quality = ADDON.getSetting('quality2')
    if quality == '0':
        return 'CAM'
    elif quality == '1':
        return 'TS'
    elif quality == '2':
        return 'TELESYNC'
    elif quality == '3':
        return 'R5'
    elif quality == '4':
        return 'DVDSCR'
    elif quality == '5':
        return 'DVDRIP'
    elif quality == '6':
        return 'HDTV'
    elif quality == '7':
        return 'BRRIP'
    elif quality == '8':
        return 'BDRIP'
    elif quality == '9':
        return '480P'
    elif quality == '10':
        return '720P'
    elif quality == '11':
        return '1080P'
    elif quality == '12':
        return ''
    else:
        return '720P'

def tvcustom_quality():
    quality = ADDON.getSetting('tvquality')
    if quality == '0':
        return 'CAM'
    elif quality == '1':
        return 'TS'
    elif quality == '2':
        return 'TELESYNC'
    elif quality == '3':
        return 'DVDSCR'
    elif quality == '4':
        return 'DVDRIP'
    elif quality == '5':
        return 'HDTV'
    elif quality == '6':
        return 'BRRIP'
    elif quality == '7':
        return 'BDRIP'
    elif quality == '8':
        return '480P'
    elif quality == '9':
        return '720P'
    elif quality == '10':
        return '1080P'
    elif quality == '11':
        return ''
    else:
        return '720P'
		
def preferred_tv2():
    if ADDON.getSetting('search_tvquality_2') == "true":
        return True
    else:
        return False
		
def tvcustom_quality2():
    quality = ADDON.getSetting('tvquality2')
    if quality == '0':
        return 'CAM'
    elif quality == '1':
        return 'TS'
    elif quality == '2':
        return 'TELESYNC'
    elif quality == '3':
        return 'DVDSCR'
    elif quality == '4':
        return 'DVDRIP'
    elif quality == '5':
        return 'HDTV'
    elif quality == '6':
        return 'BRRIP'
    elif quality == '7':
        return 'BDRIP'
    elif quality == '8':
        return '480P'
    elif quality == '9':
        return '720P'
    elif quality == '10':
        return '1080P'
    elif quality == '11':
        return ''
    else:
        return '720P'

def top_movies_sort():
    sort_id = ADDON.getSetting('top_movies_sort')
    if sort_id == '1':
        return 'user_rating,desc'
    elif sort_id == '2':
        return 'num_votes,desc'
    elif sort_id == '3':
        return 'year,desc'
    elif sort_id == '4':
        return 'release_date_us,desc'
    elif sort_id == '5':
        return 'boxoffice_gross_us,desc'
    elif sort_id == '6':
        return 'moviemeter,desc'
    else:
        return 'alpha'
		
def movie_genre_sort():
    sort_id = ADDON.getSetting('movie_genre_sort')
    if sort_id == '1':
        return 'user_rating,desc'
    elif sort_id == '2':
        return 'num_votes,desc'
    elif sort_id == '3':
        return 'year,desc'
    elif sort_id == '4':
        return 'release_date_us,desc'
    elif sort_id == '5':
        return 'boxoffice_gross_us,desc'
    elif sort_id == '6':
        return 'moviemeter,desc'
    else:
        return 'alpha'
		
def movie_group_sort():
    sort_id = ADDON.getSetting('movie_group_sort')
    if sort_id == '1':
        return 'user_rating,desc'
    elif sort_id == '2':
        return 'num_votes,desc'
    elif sort_id == '3':
        return 'year,desc'
    elif sort_id == '4':
        return 'release_date_us,desc'
    elif sort_id == '5':
        return 'boxoffice_gross_us,desc'
    elif sort_id == '6':
        return 'moviemeter,desc'
    else:
        return 'alpha'
		
def movie_studio_sort():
    sort_id = ADDON.getSetting('movie_studio_sort')
    if sort_id == '1':
        return 'user_rating,desc'
    elif sort_id == '2':
        return 'num_votes,desc'
    elif sort_id == '3':
        return 'year,desc'
    elif sort_id == '4':
        return 'release_date_us,desc'
    elif sort_id == '5':
        return 'boxoffice_gross_us,desc'
    elif sort_id == '6':
        return 'moviemeter,desc'
    else:
        return 'alpha'
		
def new_movies_sort():
    sort_id = ADDON.getSetting('new_movies_sort')
    if sort_id == '1':
        return 'user_rating,desc'
    elif sort_id == '2':
        return 'num_votes,desc'
    elif sort_id == '3':
        return 'year,desc'
    elif sort_id == '4':
        return 'release_date_us,desc'
    elif sort_id == '5':
        return 'boxoffice_gross_us,desc'
    elif sort_id == '6':
        return 'moviemeter,desc'
    else:
        return 'alpha'
		
def blu_ray_sort():
    sort_id = ADDON.getSetting('blu_ray_sort')
    if sort_id == '1':
        return 'user_rating,desc'
    elif sort_id == '2':
        return 'num_votes,desc'
    elif sort_id == '3':
        return 'year,desc'
    elif sort_id == '4':
        return 'release_date_us,desc'
    elif sort_id == '5':
        return 'boxoffice_gross_us,desc'
    elif sort_id == '6':
        return 'moviemeter,desc'
    else:
        return 'alpha'
		
def mpaa_sort():
    sort_id = ADDON.getSetting('mpaa_sort')
    if sort_id == '1':
        return 'user_rating,desc'
    elif sort_id == '2':
        return 'num_votes,desc'
    elif sort_id == '3':
        return 'year,desc'
    elif sort_id == '4':
        return 'release_date_us,desc'
    elif sort_id == '5':
        return 'boxoffice_gross_us,desc'
    elif sort_id == '6':
        return 'moviemeter,desc'
    else:
        return 'alpha'
		
	
def top_tv_sort():
    sort_id = ADDON.getSetting('top_tv_sort')
    if sort_id == '1':
        return 'user_rating,desc'
    elif sort_id == '2':
        return 'num_votes,desc'
    elif sort_id == '3':
        return 'year,desc'
    elif sort_id == '4':
        return 'release_date_us,desc'
    elif sort_id == '5':
        return 'boxoffice_gross_us,desc'
    elif sort_id == '6':
        return 'moviemeter,desc'
    else:
        return 'alpha'
		
def tv_genre_sort():
    sort_id = ADDON.getSetting('tv_genre_sort')
    if sort_id == '1':
        return 'user_rating,desc'
    elif sort_id == '2':
        return 'num_votes,desc'
    elif sort_id == '3':
        return 'year,desc'
    elif sort_id == '4':
        return 'release_date_us,desc'
    elif sort_id == '5':
        return 'boxoffice_gross_us,desc'
    elif sort_id == '6':
        return 'moviemeter,desc'
    else:
        return 'alpha'

def tv_group_sort():
    sort_id = ADDON.getSetting('tv_group_sort')
    if sort_id == '1':
        return 'user_rating,desc'
    elif sort_id == '2':
        return 'num_votes,desc'
    elif sort_id == '3':
        return 'year,desc'
    elif sort_id == '4':
        return 'release_date_us,desc'
    elif sort_id == '5':
        return 'boxoffice_gross_us,desc'
    elif sort_id == '6':
        return 'moviemeter,desc'
    else:
        return 'alpha'
		
def tv_active_sort():
    sort_id = ADDON.getSetting('tv_active_sort')
    if sort_id == '1':
        return 'user_rating,desc'
    elif sort_id == '2':
        return 'num_votes,desc'
    elif sort_id == '3':
        return 'year,desc'
    elif sort_id == '4':
        return 'release_date_us,desc'
    elif sort_id == '5':
        return 'boxoffice_gross_us,desc'
    elif sort_id == '6':
        return 'moviemeter,desc'
    else:
        return 'alpha'
		
def imdb_search_sort():
    sort_id = ADDON.getSetting('imdb_search_sort')
    if sort_id == '1':
        return 'user_rating,desc'
    elif sort_id == '2':
        return 'num_votes,desc'
    elif sort_id == '3':
        return 'year,desc'
    elif sort_id == '4':
        return 'release_date_us,desc'
    elif sort_id == '5':
        return 'boxoffice_gross_us,desc'
    elif sort_id == '6':
        return 'moviemeter,desc'
    else:
        return 'alpha'

def newmovie_days():
    newmovdays = ADDON.getSetting('newmovdays')
    if newmovdays == '9':
        return 360
    elif newmovdays == '8':
        return 300
    elif newmovdays == '7':
        return 240
    elif newmovdays == '6':
        return 180
    elif newmovdays == '5':
        return 150
    elif newmovdays == '4':
        return 120
    elif newmovdays == '3':
        return 90
    elif newmovdays == '2':
        return 60
    elif newmovdays == '1':
        return 30
    else:
        return 14
		
def xbmc_sort():
    if ADDON.getSetting('xbmc_sort') == "true":
        return True
    else:
        return False
		
def furk_search_myfiles():
    if ADDON.getSetting('furk_search_myfiles') == "true":
        return True
    else:
        return False

def imdb_filter_view():
    return "simple"

def imdb_filter_release():
    if ADDON.getSetting('release_date') == "true":
        try:
            from_date = ADDON.getSetting('release_date_from')
            to_date = ADDON.getSetting('release_date_to')
            return "%s,%s" % (from_date, to_date)
        except:
            return ","
    else:
        return ","

def imdb_filter_rating():
    if ADDON.getSetting('user_rating') == "true":
        try:
            rating_min = ADDON.getSetting('user_rating_min')
            rating_max = ADDON.getSetting('user_rating_max')
            return "%s,%s" % (rating_min, rating_max)
        except:
            return ","
    else:
        return ","
    
def imdb_filter_votes():
    if ADDON.getSetting('number_of_votes') == "true":
        try:
            votes_min = ADDON.getSetting('number_of_votes_min')
            votes_max = ADDON.getSetting('number_of_votes_max')
            return "%s,%s" % (votes_min, votes_max)
        except:
            return "2500,"
    else:
        return "2500,"

def imdb_results():
    limit = ADDON.getSetting('number_of_results')
    if limit == '0':
        return 25
    elif limit == '1':
        return 50
    elif limit == '2':
        return 100
    elif limit == '3':
        return 150
    elif limit == '4':
        return 200
    else:
        return 250

	
def imdb_user():
    return ADDON.getSetting('imdb_user')

def imdb_list1():
    return ADDON.getSetting('imdb_list1')
	
def imdb_listname1():
    return ADDON.getSetting('imdb_listname1')
	
def imdb_list2():
    return ADDON.getSetting('imdb_list2')
	
def imdb_listname2():
    return ADDON.getSetting('imdb_listname2')
	
def imdb_list3():
    return ADDON.getSetting('imdb_list3')
	
def imdb_listname3():
    return ADDON.getSetting('imdb_listname3')
	
def imdb_list4():
    return ADDON.getSetting('imdb_list4')
	
def imdb_listname4():
    return ADDON.getSetting('imdb_listname4')
	
def imdb_list5():
    return ADDON.getSetting('imdb_list5')
	
def imdb_listname5():
    return ADDON.getSetting('imdb_listname5')
	
def imdb_list6():
    return ADDON.getSetting('imdb_list6')
	
def imdb_listname6():
    return ADDON.getSetting('imdb_listname6')
	
def imdb_list7():
    return ADDON.getSetting('imdb_list7')
	
def imdb_listname7():
    return ADDON.getSetting('imdb_listname7')
	
def imdb_list8():
    return ADDON.getSetting('imdb_list8')
	
def imdb_listname8():
    return ADDON.getSetting('imdb_listname8')
	
def imdb_list9():
    return ADDON.getSetting('imdb_list9')
	
def imdb_listname9():
    return ADDON.getSetting('imdb_listname9')
	
def imdb_list10():
    return ADDON.getSetting('imdb_list10')
	
def imdb_listname10():
    return ADDON.getSetting('imdb_listname10')

def furk_account():
    if ADDON.getSetting('furk_account') == "true":
        return True
    else:
        return False

def furk_user():
    return ADDON.getSetting('furk_user')
    
def furk_pass():
    return ADDON.getSetting('furk_pass')
	
def furk_limit_file_size():
    if ADDON.getSetting('furk_limit_file_size') == "true":
        return True
    else:
        return False

def furk_format():
    if ADDON.getSetting('furk_format') == "true":
        return True
    else:
        return False
		
def furk_limit_fs_num():
    furk_limit_fs_num = ADDON.getSetting('furk_limit_fs_num')
    if furk_limit_fs_num == '6':
        return 10
    elif furk_limit_fs_num == '5':
        return 7.5
    elif furk_limit_fs_num == '4':
        return 5
    elif furk_limit_fs_num == '3':
        return 4
    elif furk_limit_fs_num == '2':
        return 3
    elif furk_limit_fs_num == '1':
        return 2
    else:
        return 1
		
def furk_limit_fs_min():
    furk_limit_fs_min = ADDON.getSetting('furk_limit_fs_min')
    if furk_limit_fs_min == '5':
        return 262144000
    elif furk_limit_fs_min == '4':
        return 209715200
    elif furk_limit_fs_min == '3':
        return 157286400
    elif furk_limit_fs_min == '2':
        return 104857600
    elif furk_limit_fs_min == '1':
        return 52428800
    else:
        return 0
		
def furk_limit_file_size_tv():
    if ADDON.getSetting('furk_limit_file_size_tv') == "true":
        return True
    else:
        return False
		
def furk_limit_fs_num_tv():
    furk_limit_fs_num = ADDON.getSetting('furk_limit_fs_num')
    if furk_limit_fs_num == '9':
        return 10
    elif furk_limit_fs_num == '8':
        return 7.5
    elif furk_limit_fs_num == '7':
        return 5
    elif furk_limit_fs_num == '6':
        return 4
    elif furk_limit_fs_num == '5':
        return 3
    elif furk_limit_fs_num == '4':
        return 2
    elif furk_limit_fs_num == '3':
        return 1
    elif furk_limit_fs_num == '2':
        return 0.75
    elif furk_limit_fs_num == '1':
        return 0.5
    else:
        return 0.25

def subscription_update():
    if ADDON.getSetting('subscription_update') == "true":
        return True
    else:
        return False
    
def use_unicode():
    if ADDON.getSetting('use_unicode_indicators') == "true":
        return True
    else:
        return False
        
def download_meta():
    if ADDON.getSetting('download_meta') == "true":
        return True
    else:
        return False
    
def movies_directory():
    if ADDON.getSetting('movies_custom_directory') == "true":
        return ADDON.getSetting('movies_directory')
    else:
        return create_directory(DATA_PATH, "movies")
    
def tv_show_directory():
    if ADDON.getSetting('tv_shows_custom_directory') == "true":
        return ADDON.getSetting('tv_shows_directory')
    else:
        return create_directory(DATA_PATH, "tv shows")
		
def movies_download_directory():
    return ADDON.getSetting('movies_download_directory')
		
def tv_download_directory():
    return ADDON.getSetting('tv_download_directory')
		
def music_download_directory():
    return ADDON.getSetting('music_download_directory')
	
def music_video_download_directory():
    return ADDON.getSetting('music_video_download_directory')
		
def first_time_startup():
    if ADDON.getSetting('first_time_startup') == "true":
        return True
    else:
        return False

def play_mode():
    return 'stream'

def dummy_path():
    return os.path.join(ADDON.getAddonInfo('path'), 'dummy.wma')

def service_sleep_time():
    return 10

def subscription_timer():
    return int(ADDON.getSetting('subscription_timer'))

def subscription_wishlist():
    if ADDON.getSetting('subscription_wishlist') == 'true':
        return True
    else:
        return False

def use_posters():
    if ADDON.getSetting('use_posters') == 'true':
        return True
    else:
        return False
    
def use_fanart():
    if ADDON.getSetting('use_fanart') == 'true':
        return True
    else:
        return False
    
def meta_quality():
    quality_id = ADDON.getSetting('meta_quality')
    if quality_id == '3':
        return 'maximum'
    elif quality_id == '2':
        return 'high'
    elif quality_id == '1':
        return 'medium'
    else:
        return 'thumb'  
    
def fanart_quality():
    quality_id = ADDON.getSetting('meta_quality')
    if quality_id == '3':
        return 'original' #thumb, poster, original
    elif quality_id == '2':
        return 'original'
    elif quality_id == '1':
        return 'poster'   
    else:
        return 'thumb' 
    
def poster_quality():
    quality_id = ADDON.getSetting('meta_quality')
    if quality_id == '3':
        return 'original' #thumb, cover, mid. original
    elif quality_id == '2':
        return 'mid' 
    elif quality_id == '1':
        return 'cover' 
    else:
        return 'thumb'

def enable_pc():
    if ADDON.getSetting('enable_pc') == "true":
        return True
    else:
        return False
		
def watershed_pc():
    id = ADDON.getSetting('watershed_pc')
    if id == '9':
        return 25
    elif id == '8':
        return 23 
    elif id == '7':
        return 22 
    elif id == '6':
        return 21
    elif id == '5':
        return 20
    elif id == '4':
        return 19
    elif id == '3':
        return 18
    elif id == '2':
        return 17
    elif id == '1':
        return 16
    else:
        return 15
		
def pw_required_at():
    id = ADDON.getSetting('pw_required_at')
    if id == '3':
        return 4
    elif id == '2':
        return 3
    elif id == '1':
        return 2
    else:
        return 1

def enable_pc_settings():
    return ADDON.getSetting('enable_pc_settings')
		
def pc_pass():
    return ADDON.getSetting('pc_pass')
	

def pc_default():
    id = ADDON.getSetting('pc_default')
    if id == '1':
        return "DO NOT PLAY"
    else:
        return "PLAY"
	

'''
kinkin
'''

import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import settings
import time,datetime
from datetime import date
from threading import Timer
from hashlib import md5
from helpers import clean_file_name
import json
import glob
import shutil
from threading import Thread
import cookielib
from helpers import clean_file_name
import plugintools
from t0mm0.common.net import Net


ADDON = settings.addon()
FAV = settings.favourites_file()
FORCE_SD = settings.force_sd()
cookie_jar = settings.cookie_jar()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.thebeautifulgame', 'art', 'fanart.jpg'))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.thebeautifulgame', 'icon.png'))
base_url = 'http://eurorivals.net'
net = Net()

def open_url(url):
    trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
    response = urllib2.urlopen(req)
    link=response.read().replace('\xe9', 'e')#.translate(trans_table)
    response.close()
    return link

def CATEGORIES(name):
    addDir("News", 'url',29,iconart, '','')
    addDir("90 Minutes", 'url',89,iconart, '','')
    addDir("Highlights", 'url',10,iconart, '','')
    addDir("Top Videos", 'http://eurorivals.net/best-football-videos.html',4,iconart, '','')   
    addDir("Top Clubs", 'http://eurorivals.net/european-football-clubs.html',20,iconart, '','')
    addDir("Lower League Clubs", 'http://eurorivals.net/european-football-clubs.html',25,iconart, '','')
    addDir("Tables", 'http://eurorivals.net/tables.html',60,iconart, '','')
    addDir("Players", 'url',39,iconart, '','')
    addDir("UEFA Club Rankings", 'http://eurorivals.net/club-rankings.html',70,iconart, '','')

def highlights(url):
    addDir("Highlights by Date", 'http://eurorivals.net/football-highlights.html',1,iconart, '','')
    addDir("Highlights by Country", 'http://eurorivals.net/football-highlights.html',11,iconart, '','')
    addDir("Champions League", 'http://eurorivals.net/champions-league',22,iconart, '','')
    addDir("Europa League", 'http://eurorivals.net/europa-league',22,iconart, '','')

def highlights_country(url):
    link = open_url(url).rstrip()
    links = regex_from_to(link, 'Filter Highlights by Country', '<div style="clear:both;"></div>')
    match = re.compile('<a href="(.+?)"  class="tiptip" title="(.+?)"><img src="(.+?)" (.+?) alt="" /></a>').findall(links)
    for u, t, th, d in match:
        url = base_url + u
        iconimage = base_url + th
        addDir(t, url,1,iconimage, '','')

def highlights_list(url):
    hidescores = False
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Hide Results?", '', 'Do you want hide the scores?'):
       hidescores = True
    link= open_url(url).rstrip()
    list = regex_from_to(link, '<table cellpadding=0 cellspacing=3 width=4', '</table>')
    all_hl = regex_get_all(list, '<tr valign=', '</tr>')
    for hl in all_hl:
        title = regex_from_to(hl, "><b>", '</b> <span').replace('<b>', '').replace('</b>', '')
        if hidescores:
            title = title.replace('0', '?').replace('1', '?').replace('2', '?').replace('3', '?').replace('4', '?').replace('5', '?').replace('6', '?').replace('7', '?').replace('8', '?').replace('9', '?')
        country = regex_from_to(hl, 'alt="', '"')
        matchdate = regex_from_to(hl, '11px;">', '</td>')
        url = base_url + regex_from_to(hl, "<a href='", "' class")
        text = "%s - [COLOR cyan]%s[/COLOR] - [COLOR gold]%s[/COLOR]" % (matchdate, title, country)
        iconimage = ""
        addDir(text,url,2,iconimage,text,"")
    try:
        pagestring = regex_from_to(link, 'class="inactive">', '</strong></div>')
        pages = re.compile('<a href="(.+?)#list" class="active">(.+?)</a>').findall(pagestring)
        for u, p in pages:
            url = base_url + u
            text = "> Page %s" % p
            addDir(text,url,1,"","","")
    except:
        pass
		
def ninety_minutes_menu():
    addDir("90 Minutes - Latest", 'http://livefootballvideo.com/fullmatch',92,iconart, '','')
    addDir("90 Minutes - Top Competitions", 'http://livefootballvideo.com/competitions',93,iconart, '','')
    addDir("90 Minutes - All Competitions", 'http://livefootballvideo.com/competitions',93,iconart, '','')
    addDir("90 Minutes - All Teams", 'http://livefootballvideo.com/teams',90,iconart, '','')

def ninety_minutes_submenu(name, url):
    link = open_url(url).replace('\n','')
    print link
    if name == "90 Minutes - Top Competitions":#url, title
        data = regex_from_to(link, '>Competitions<', 'title="All')
        match = re.compile('<a href="(.+?)">(.+?)</a>').findall(data)
        for url, title in match:
            urlname = url.replace('http://livefootballvideo.com/competitions/', '')
            iconimage = 'http://livefootballvideo.com/images/leagues/big/x%s.png.pagespeed.ic.45fxD8-tJP.png' % urlname
            addDir(title,url,92,iconimage,"","")
    else:
        #match = re.compile('<li><img src="(.+?)"/> <a href="(.+?)" title="(.+?)">(.+?)</a></li>').findall(link)
        match = re.compile('<li><img style="display:none;visibility:hidden;" data-cfsrc="(.+?)"/><noscript><img src="(.+?)"/></noscript> <a href="(.+?)" title="(.+?)">(.+?)</a></li>').findall(link)
        for d2,iconimage,url,d1,title in match:
            iconimage = iconimage.replace('small', 'big')
            url = 'http://livefootballvideo.com' + url
            addDir(title,url,92,iconimage,"","")		

def ninety_minutes_teams(name,url,iconimage):
    link = open_url(url).replace('\n','')
    #match = re.compile('<li><img src="(.+?)"/> <a href="(.+?)" title="(.+?)">(.+?)</a></li>').findall(link)
    match = re.compile('<li><img style="display:none;visibility:hidden;" data-cfsrc="(.+?)"/><noscript><img src="(.+?)"/></noscript> <a href="(.+?)" title="(.+?)">(.+?)</a></li>').findall(link)
    for d2,iconimage,url,d1,title in match:
        urlname = url.replace('/teams/', '')
        iconimage = 'http://livefootballvideo.com/images/teams/big/x%s.png.pagespeed.ic.45fxD8-tJP.png' % urlname
        url = 'http://livefootballvideo.com' + url
        addDir(title,url,92,iconimage,"","clubs")
	
def ninety_minutes_latest(name,url,iconimage):
    link = open_url(url).replace('\n','')
    all_match = regex_get_all(link, 'rel="bookmark', '</p></div></li>')
    for m in all_match:
        title = regex_from_to(m, 'title="', '"')
        datestr = regex_from_to(m, 'longdate" rel="', '</p>')
        datestr = datestr[12:]
        url = regex_from_to(m, '<a href="', '"')
        iconimage = regex_from_to(m, '<img src="', '"')
        title = "%s - %s" % (datestr,title)
        addDir(title,url,91,iconimage,"","clubs")
    if 'class="nextpostslink' in link:
        all_pages = regex_from_to(link, "<span class='pages", 'class="nextpostslink')
        pages = re.compile('href="(.+?)">(.+?)</a>').findall(all_pages)
        for url, pg in pages:
            if not 'laquo' in pg:
                addDir('[COLOR cyan]' + '>> Page ' + pg + '[/COLOR]',url,92,"","","")
		
def ninety_minutes_source(name,url,iconimage):
#'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'
    link = open_url(url).replace("'", '"').replace('\n','')
    print link
    fullmatch = regex_from_to(link, 'Full Match Video', 'Start Iframe')
    all_lang = regex_get_all(fullmatch, '<h3 class="heading', '</p></div>')
    for lang in all_lang:
        language = regex_from_to(lang, '<span>', '</span>')
        match_urls=re.compile('src="(.+?)"').findall(lang)
        for url in match_urls:
            url = url.replace('&amp;', '&')
            if 'dailymotion' in url:
                videoid = regex_from_to(url, 'http://www.dailymotion.com/embed/video/', '?logo').replace('?', '')
                iconimage = dm_icon(videoid)
            if 'dailymotion' in url:
                title = " [dailymotion.com]"
            elif 'vk.com' in url:
                title = " [vk.com]"
            elif 'videa' in url:
                title = " [videa.com]"
            elif 'rutube' in url:
                title = " [rutube.com]"
            elif 'youtube' in url:
                title = " [youtube.com]"
            elif 'firedrive' in url:
                title = " [firedrive.com]"            
            addDirPlayable(name + ' - ' + language + title,url,3,iconimage,"")
		
def best_videos_list(url):
    link= open_url(url).rstrip()
    all_hl = regex_get_all(link, '<div class="videoitem', '</div><div style')
    for hl in all_hl:
        try:
            titlereg = regex_from_to(hl, '<div style="max-height', '</div>')
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(titlereg)
            for u, t in match:
                title = t
                url = base_url + u
            vidlink = regex_from_to(hl, 'background-image:url', '.jpg').replace('(http://img.youtube.com/vi/','').replace('/default','')
            iconimage = 'http://i1.ytimg.com/vi/%s/mqdefault.jpg' % vidlink
            play_url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+vidlink
            plugintools.add_item( action="play" , title=title , plot="" , url=play_url ,thumbnail=iconimage , folder=True )
        except:
            pass

		
def uefa_rankings(url):
    link = open_url(url)
    link = re.sub(r'<sp.+?">', '', link).replace('</span>', '')
    headings = re.compile('<td width="40">(.+?)</td><td width="40">(.+?)</td><td width="40">(.+?)</td><td width="40">(.+?)</td><td width="40">(.+?)</td><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(.+?)</td></tr>').findall(link)
    for a,b,c,d,e,tot in headings:
        text = "Pos. %s     %s     %s    %s     %s     %s      Team" % (a,b,c,d,e,tot)
        addDirPlayable('[COLOR red]' + text.replace('20','') + '[/COLOR]','url',999,iconart,"")
    list = re.compile('<tr height=24><td>(.+?)</td><td align=right><a href="(.+?)">(.+?)</a></td><td align=right width=40><img src="(.+?)" style="border:0;background-color:#fff" width="20" height="20" title=(.+?)"/></td><td align=right>(.+?)</td><td align=right>(.+?)</td><td align=right>(.+?)</td><td align=right>(.+?)</td><td align=right>(.+?)</td><td align=right>(.+?)</td></tr>').findall(link)
    for pos,url,name,iconimage,d1,sc1,sc2,sc3,sc4,sc5,tot in list:
        pos = pos.replace('st', '').replace('rd', '').replace('th', '').replace('nd', '')
        pos = (pos + '.').ljust(7-len(pos))
        name = name
        sc1 = sc1.ljust(9)
        sc2 = sc2.ljust(9)
        sc3 = sc3.ljust(9)
        sc4 = sc4.ljust(9)
        sc5 = sc5.ljust(9)
        tot = tot.ljust(9)
        url = base_url + url.replace('" style="font-weight:bold;','')
        iconimage = base_url + iconimage
        squadurl = url.replace('clubs', 'squad')
        text = "[COLOR lime]%s[/COLOR] %s %s %s %s %s [COLOR cyan]%s[/COLOR] [COLOR gold]%s[/COLOR]" % (pos,sc1,sc2,sc3,sc4,sc5,tot,name)
        addDir(text,url,22,iconimage,squadurl,"clubs")
		
def club_directory(url):
    link = open_url(url)
    section = regex_from_to(link, '<hr style="margin-top:30px;"/>', '<h1>')
    country_list = regex_get_all(section, '<h3 class="betting">', '</table>')
    for country in country_list:
        title = regex_from_to(country, 'alt="', '"')
        iconimage = 'http://livefootballvideo.com/images/teams/big/100x100x%s.png.pagespeed.ic.aMshmfIEyS.png' % title.lower().replace(' ', '-').replace('usa', 'united-states').replace('macedonia', 'macedonia-fyr').replace('bosnia', 'bosnia-herzegovina')
        #iconimage = base_url + regex_from_to(country, '<img src="', '"')
        club_list = regex_from_to(country, '<table', '</table>')
        addDir(title,'url',21,iconimage,club_list,"")
		
def club_directory_lower(url):
    link = open_url(url)
    section = regex_from_to(link, '<h1>', '</a></li>')
    country_list = regex_get_all(section, '<h3 class="betting">', '</table>')
    for country in country_list:
        title = regex_from_to(country, 'alt="', '"')
        iconimage = 'http://livefootballvideo.com/images/teams/big/100x100x%s.png.pagespeed.ic.aMshmfIEyS.png' % title.lower().replace(' ', '-').replace('usa', 'united-states').replace('macedonia', 'macedonia-fyr').replace('bosnia', 'bosnia-herzegovina')
        #iconimage = base_url + regex_from_to(country, '<img src="', '"')
        club_list = regex_from_to(country, '<table', '</table>')
        addDir(title,'url',21,iconimage,club_list,"")
		
def club_menu(name, url, list):
    clubs = re.compile('<a href="(.+?)">(.+?)</a>').findall(list)
    for u, t in clubs:
        uname = regex_from_to(u, '/clubs/', '.html')
        url = base_url + u
        squadurl = url.replace('clubs', 'squad')
        iconimage = 'http://livefootballvideo.com/images/teams/big/100x100x%s.png.pagespeed.ic.aMshmfIEyS.png' % t.lower().replace(' ', '-').replace('usa', 'united-states').replace('macedonia', 'macedonia-fyr').replace('bosnia', 'bosnia-herzegovina').replace('man-utd', 'manchester-united').replace('man-city', 'manchester-city').replace('tottenham', 'tottenham-hotspur').replace('west-brom', 'west-bromwich-albion').replace('west-ham', 'west-ham-united')
        addDir(t,url,22,iconimage,squadurl,"clubs")
	
def club_results(name, url, iconimage):
    hidescores = False
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Hide Results?", '', 'Do you want hide the scores?'):
       hidescores = True
    try:
        splitname = name.split(']')
        teamname = splitname[5].replace('[/COLOR','')
    except:
        teamname = ''
    link = open_url(url)
    match = regex_get_all(link, '<div class="scrowsmall"', '</div></div><div class="clr"')
    pages = regex_get_all(link, ' onclick="xmlhttpPost', '</a>')
    for m in match:
        if 'title="' in m:
            mdetail = re.compile('title="(.+?)">(.+?)</div><div class="sccompsm"><a href="(.+?)">(.+?)</a></div><div class="schomeco">(.+?)</div><div class="scpen blank"></div><div class="scscoreco (.+?)" onClick="lightbox(.+?)" >(.+?)</div><div class="scpen blank"></div><div class="scawayco">(.+?)</div><div class="scvideo"><a href="(.+?)">(.+?)</a>').findall(m)
        else:
            mdetail = re.compile('<div class="scrow(.+?)"><div class="sc(.+?)"></div><div class="sccompsm"><a href="(.+?)">(.+?)</a></div><div class="schomeco">(.+?)</div><div class="scpen blank"></div><div class="scscoreco (.+?)" onClick="lightbox(.+?)" >(.+?)</div><div class="scpen blank"></div><div class="scawayco">(.+?)</div><div class="scvideo"><a href="(.+?)">(.+?)</a>').findall(m)
        for day,datestr,lgeurl,lgename,home,dum2,dum1,score,away,url,hltag in mdetail:
            if hidescores:
                score = score.replace('0', '?').replace('1', '?').replace('2', '?').replace('3', '?').replace('4', '?').replace('5', '?').replace('6', '?').replace('7', '?').replace('8', '?').replace('9', '?')
            datestr = datestr.replace('time', '')
            url = base_url + url
            text = "%s - [COLOR cyan]%s [COLOR lime]%s[/COLOR] %s[/COLOR] - [COLOR gold]%s[/COLOR]" % (datestr, home, score, away, hltag)
            iconimage = 'http://livefootballvideo.com/images/teams/big/100x100x%s.png.pagespeed.ic.aMshmfIEyS.png' % teamname.lower().replace(' ', '-').replace('usa', 'united-states').replace('macedonia', 'macedonia-fyr').replace('bosnia', 'bosnia-herzegovina')
            addDir(text,url,2,iconimage,text,"")
    for m in match:
        mdetail = re.compile('title="(.+?)">(.+?)</div><div class="sccompsm"><a href="(.+?)">(.+?)</a></div><div class="schomeco">(.+?)</div><div class="scpen blank"></div><div class="(.+?)" onClick="lightbox(.+?)" >(.+?)</div><div class="scpen blank"></div><div class="scawayco">(.+?)</div><div class="scnovideo (.+?)">(.+?);</div>').findall(m)
        for day,datestr,lgeurl,lgename,home,dum1,dum2,score,away,url,hltag in mdetail:
            if hidescores:
                score = score.replace('0', '?').replace('1', '?').replace('2', '?').replace('3', '?').replace('4', '?').replace('5', '?').replace('6', '?').replace('7', '?').replace('8', '?').replace('9', '?')
            url = base_url + url
            text = "%s - [COLOR cyan]%s %s %s[/COLOR]" % (datestr, home, score, away)
            addDir(text,url,999,iconimage,text,"")

    for p in pages:
        url = base_url + regex_from_to(p, "xmlhttpPost", "',").replace("('", "")
        title = regex_from_to(p, 'aaa;"', '</div>').replace('>&laquo; ', '').replace(' &raquo;', '')
        addDir(title,url,22,iconimage,"","")

def tables_directory(url):
    link = open_url(url)
    country_list = re.compile('<a href="(.+?)" class="tiptip" title="(.+?)"><img src=(.+?)" /></a>').findall(link)
    for url, title, dummy in country_list:
        iconimage = 'http://livefootballvideo.com/images/teams/big/100x100x%s.png.pagespeed.ic.aMshmfIEyS.png' % title.lower().replace(' ', '-').replace('usa', 'united-states').replace('macedonia', 'macedonia-fyr').replace('bosnia', 'bosnia-herzegovina')
        url = base_url + url
        addDir(title,url,61,iconimage,title,"")

def tables_menu(url,iconimage):
    link = open_url(url).strip('\n').replace('&nbsp;', '').replace('&', 'aand')
    table_list = regex_get_all(link, '<h2 style="margin-bottom', '</table>')
    for t in table_list:
        table_name = regex_from_to(t, '0px;">', '</h2>')
        addDir(table_name,'url',62,"",t,"")
 
def league_table(name, url, list):
    teamlist = regex_get_all(list.replace('aand', '&'), '<tr style="height', '</div></td></tr>')
    addDirPlayable('[COLOR red]Pos. Pld   W    D      L      F      A      GD    Pts   Team[/COLOR]','url',999,iconart,"")
    for t in teamlist:
        if '<a href=' in t and 'img src="' in t:
            match = re.compile('<td>(.+?)</td><td><div style="width:150px;height:20px;white-space:nowrap;overflow:hidden;"><a href="(.+?)" style="font-weight:bold;" title="(.+?)">(.+?)</a> </div><td height="20"> <img src="(.+?)" style="vertical-align:middle;border:0;background-color:#fff" width="20" height="20" title="(.+?)" alt="(.+?)"/></td><td>(.+?)</td><td class="lthomewin">(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td class="lthomewin">(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td class="lthomewin">(.+?)</td><td><b>(.+?)</b>').findall(t)
        elif '<a href=' in t:
            match = re.compile('<td>(.+?)</td><td><div style="width:150px;height:20px;white-space:nowrap;overflow:hidden;"><a href="(.+?)" style="font-weight:bold;" title="(.+?)">(.+?)</a> </(.+?)><td (.+?)="(.+?)"> </td><td>(.+?)</td><td class="lthomewin">(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td class="lthomewin">(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td class="lthomewin">(.+?)</td><td><b>(.+?)</b>').findall(t)
        else:
            match = re.compile('<td>(.+?)</td><td><div style="(.+?):150px;(.+?):20px;white-space:nowrap;overflow:hidden;"><b>(.+?)</b>(.+?)</(.+?)><(.+?)></td><td>(.+?)</td><td class="lthomewin">(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td class="lthomewin">(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td class="lthomewin"> (.+?)</td><td><b>(.+?)</b></td>').findall(t)
        for pos,url,d1,team,iconimage,d2,d3,pld,hw,hd,hl,hf,ha,aw,ad,al,af,aa,gd,pts in match:
            pos = (pos + '.').ljust(7-len(pos))
            iconimage = 'http://eurorivals.net' + iconimage
            team = team
            if '-' in gd:
                gd = gd.ljust(9-len(gd))
            else:
                gd = gd.ljust(9-len(gd)+1)
            pld = pld.ljust(7-len(pld))
            url = base_url + url
            won = (str(int(hw) + int(aw)))
            drw = str(int(hd) + int(ad))
            lost = str(int(hl) + int(al))
            f = str(int(hf) + int(af))
            a = str(int(ha) + int(aa))
            won = won.ljust(7-len(won))
            drw = drw.ljust(7-len(drw))
            lost = lost.ljust(7-len(lost))
            f = f.ljust(7-len(f))
            a = a.ljust(7-len(a))
            squadurl = url.replace('clubs', 'squad')
            if 'images' in iconimage:
                text = '[COLOR gold]' + team + '[/COLOR]'
            else:
                text = '[COLOR silver]' + team + '[/COLOR]'
            text1 = "[COLOR lime]%s[/COLOR] %s %s %s %s %s %s %s [COLOR cyan]%s[/COLOR]" % (pos, pld, str(won), str(drw), str(lost), str(f), str(a), gd, pts)
            text = text1 + '    ' + text
            if 'images' in iconimage:
                addDir(text,url,22,iconimage,squadurl,"clubs")
            else:
                addDirPlayable(text,'url',999,iconimage,squadurl)
		
def source_video(name, url, iconimage):
    link = open_url(url)
    video_links = regex_get_all(link, '<div class="singlevideo">', 'div></div>')
    for links in video_links:
        url = regex_from_to(links, 'src="', '"').replace('&amp;', '&')
        if 'dailymotion' in url:
            videoid = url[39:46]
            iconimage = dm_icon(videoid)
        elif 'youtube' in url:
            videoid = regex_from_to(url, 'http://www.youtube.com/embed/', 'showinfo').replace('?', '')
            iconimage = 'http://i1.ytimg.com/vi/%s/mqdefault.jpg' % videoid
        else:
            iconimage = ""
        if 'rutube' in url:
            source = 'Source: rutube'
        else:
            source = regex_from_to(links, 'Football Highlights</a> ', '<')
        if len(source)>8 and 'facebook' not in url and 'sapo.pt' not in url:
            addDirPlayable(name + ' ' + source,url,3,iconimage,name)
			
def dm_icon(videoid):
    url = 'https://api.dailymotion.com/video/%s?fields=thumbnail_large_url' % videoid
    try:
        link = open_url(url)
        iconimage=regex_from_to(link, 'thumbnail_large_url":"', '"').replace('\/','/')
        return iconimage
    except:
        return ''
			
		
def play_video(name, url, iconimage):
    dp = xbmcgui.DialogProgress()
    dp.create('Opening ' + name)
    playlink = resolve_url(url)
    if playlink == 'none available':
        notification(name, 'Video is no longer available', '3000', iconart)
    elif playlink == 'skypremium':
        notification(name, 'Video only for Sky Sports subscribers', '3000', iconart)
    else:
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        playlist.add(playlink,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	
        handle = str(sys.argv[1])    
        if handle != "-1":
            listitem.setProperty("IsPlayable", "true")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        else:
            try:
                xbmcPlayer.play(playlist)
            except:
                dialog = xbmcgui.Dialog()
                dialog.ok("Playback failed", "Check your account settings")
    dp.close()
	
def resolve_url(url):
    #VK.com
    if 'vk.com' in url:
        hosturl = 'http://eurorivals.net/football-highlights.html'
        header_dict = {}
        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header_dict['Host'] = 'vk.com'
        header_dict['Referer'] = str(hosturl)
        header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
        net.set_cookies(cookie_jar)
        link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
        net.save_cookies(cookie_jar)
        if FORCE_SD:
            if 'url480":"' in link:
                vidlinks = re.compile('url480":"(.+?)"').findall(link)
            elif 'url360":"' in link:
                vidlinks = re.compile('url360":"(.+?)"').findall(link)
            elif 'url240":"' in link:
                vidlinks = re.compile('url240":"(.+?)"').findall(link)
            else:
                vidlinks = re.compile('url720":"(.+?)"').findall(link)
            for playlink in vidlinks:
                playlink = playlink.replace('\/', '/')
        else:
            if 'url720":"' in link:
                vidlinks = re.compile('url720":"(.+?)"').findall(link)
            elif 'url480":"' in link:
                vidlinks = re.compile('url480":"(.+?)"').findall(link)
            elif 'url360":"' in link:
                vidlinks = re.compile('url360":"(.+?)"').findall(link)
            else:
                vidlinks = re.compile('url240":"(.+?)"').findall(link)
            for playlink in vidlinks:
                playlink = playlink.replace('\/', '/')
			
    #VIDEA.HU
    if 'videa.hu' in url:#http://videa.hu/player?v=a6eZxnrQf9JoHi9o
        url = url.replace('http://videa.hu/player?',  'http://videa.hu/flvplayer_get_video_xml.php?')
        link = open_url(url)
        if not 'video_url="' in link:
            playlink = 'none available'
        else:
            playlink = regex_from_to(link, 'video_url="', '"')
			
    #EURORIVALS
    if 'eurorivals.net' in url:
        link = open_url(url)
        video_id = regex_from_to(link, 'src="http://www.youtube.com/embed/', '"')
        playlink = ('plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id)

    #YOUTUBE
    if 'youtube' in url:
        video_id = regex_from_to(url, 'http://www.youtube.com/embed/', 'showinfo').replace('?', '')
        playlink = ('plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id)
		
    #DAILYMOTION
    if 'dailymotion' in url:
        url = url.replace('swf', 'embed/video')
        link = open_url(url)
        if 'stream_h264_hd1080_url":"http' in link:
            playlink = regex_from_to(link, 'stream_h264_hd1080_url":"', '"').replace('\/', '/')
        elif 'stream_h264_hd_url":"http' in link:
            playlink = regex_from_to(link, 'stream_h264_hd_url":"', '"').replace('\/', '/')
        elif 'stream_h264_hq_url":"http' in link:
            playlink = regex_from_to(link, 'stream_h264_hq_url":"', '"').replace('\/', '/')
        elif 'stream_h264_ld_url":"http' in link:
            playlink = regex_from_to(link, 'stream_h264_ld_url":"', '"').replace('\/', '/')
        elif 'stream_h264_url":"http' in link:
            playlink = regex_from_to(link, 'stream_h264_url":"', '"').replace('\/', '/')
        else:
            playlink = 'none available'
			
    #RUTUBE
    if 'rutube' in url:
        try:
            if 'http' in url:
                video_id = url[29:36]
            else:
                video_id = url.replace('//rutube.ru/video/embed/', '')
            print video_id
            link = open_url('http://rutube.ru/api/play/trackinfo/%s/?format=xml'%video_id)
            playlink = regex_from_to(link, '<m3u8>', '</m3u8>')
        except:
            playlink = 'none available'
		
    #SKY SPORTS
    if 'skysports' in url:
        link = open_url(url)
        try:
            playlink = regex_from_to(link, 'video-url="', '"')
        except:
            playlink = 'skypremium'
			
    #FIREDRIVE
    if 'firedrive' in url:
        trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
        #url = url.replace('embed', 'file')
        hosturl = url
        header_dict = {}
        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header_dict['Host'] = 'www.firedrive.com'
        header_dict['Referer'] = str(hosturl)
        net.set_cookies(cookie_jar)
        link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
        regex_from_to(link, 'confirm" value="', '"')
        net.save_cookies(cookie_jar)
        confirm = regex_from_to(link, 'confirm" value="', '"')
        form_data = ({'confirm': confirm})
        url = url.replace('embed', 'file')
        header_dict['Referer'] = str(url)
        net.set_cookies(cookie_jar)
        link = net.http_POST(url, form_data=form_data,headers=header_dict).content.translate(trans_table).rstrip()
        sources = regex_from_to(link, 'sources:', 'fileref')
        fileurl = regex_from_to(sources, "file: '", "'")
        if 'hd=' in sources:
            playlink = fileurl.replace('stream', 'hd')
        else:
            playlink = fileurl		
		
    return playlink

def news_directory(url):
    addDir("Latest News", 'http://eurorivals.net/news',30,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Sky Sports Videos", 'http://www1.skysports.com/watch/video/sports/football',79,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Transfer Rumours", 'http://eurorivals.net/news/transfer-rumours',30,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Premier League News", 'http://eurorivals.net/news/premier-league',30,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Spanish La Liga News", 'http://eurorivals.net/news/la-liga',30,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Italian Serie A News", 'http://eurorivals.net/news/serie-a',30,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("German Bundesliga News", 'http://eurorivals.net/news/bundesliga',30,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("French Lique 1 News", 'http://eurorivals.net/news/ligue-1',30,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Champions League News", 'http://eurorivals.net/news/champions-league',30,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Europa League News", 'http://eurorivals.net/news/europa-league',30,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Scottish Premiership News", 'http://eurorivals.net/news/scottish-premiership',30,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')

def news(url):
    link = open_url(url)
    link1 = regex_from_to(link,'start of main content cell', 'end of main content cell')
    all_news = regex_get_all(link1, '<a href="/guardian', '</a>')
    for news in all_news:
        try:
            title = regex_from_to(news, 'title="', '"').replace('</strong>', '').replace('<strong>', '').replace('</b>', '').replace('<b>', '').replace('</p>', '').replace('<p>', '')
        except:
            try:
                title = regex_from_to(news, 'font-weight:bold;">', '</a>')
            except:
                title = regex_from_to(news, '&quot;>', '</a>')
        title = title.replace('&nbsp;', ' ')
        url = base_url + regex_from_to(news, 'href="', '"')
        try:
            iconimage = regex_from_to(news, 'image:url(', ');')
        except:
            iconimage = ""
        addDirPlayable(title,url,31,iconimage,title)

		
def news_link(name, url, iconimage):
    dp = xbmcgui.DialogProgress()
    dp.create('Opening article')
    link = open_url(url).replace(' </div> </div>', '').replace('left">', '> ').replace('/tr>', '>\n').replace('      <caption>            ', '').replace('          </caption>      <thead>        ', '\n').replace('      </thead>      <tbody>        ', '')#.encode('utf-8','ignore')
    try:
        try:
            newsbody = regex_from_to(link, '<p>', '</p><div class').replace('</p>', '\n').replace('<p>', '\n').replace('&eacute;', 'e').replace('&nbsp;', ' ')
        except:
            try:
                newsbody = regex_from_to(link, '<p>', '</p></blockquote').replace('</p>', '\n').replace('<p>', '\n').replace('&eacute;', 'e').replace('&nbsp;', ' ')
            except:
                newsbody = regex_from_to(link, '<p>', '</p> </div><div class').replace('</p>', '\n').replace('<p>', '\n').replace('&eacute;', 'e').replace('&nbsp;', ' ')
        newsbody = re.sub(r'<.+?>', '', newsbody).replace('<>', '')
        header = "[B][COLOR red]" + name + "[/B][/COLOR]"
        TextBoxes(header,newsbody)
    except:
        notification('Article not available', 'issue scraping website', '3000', iconart)
    dp.close()

def sky_news_mainmenu(url):
    addDir("Sky Sports News Videos", 'http://www1.skysports.com/watch/video/sports/football',80,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Sky Sports TV Shows", 'http://www1.skysports.com/watch/video/tv-shows',84,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')

def sky_news(url):
    addDir("Premier League", 'http://www1.skysports.com/watch/video/sports/football/competitions/premier-league',81,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Championship", 'http://www1.skysports.com/watch/video/sports/football/competitions/championship',81,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("League One", 'http://www1.skysports.com/watch/video/sports/football/competitions/league-one',81,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("League Two", 'http://www1.skysports.com/watch/video/sports/football/competitions/league-two',81,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Scottish Football", 'http://www1.skysports.com/watch/video/sports/football/competitions/scottish-football',81,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Primera Liga", 'http://www1.skysports.com/watch/video/sports/football/competitions/primera-liga',81,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Champions League", 'http://www1.skysports.com/watch/video/sports/football/competitions/champions-league',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Capital One Cup", 'http://www1.skysports.com/watch/video/sports/football/competitions/capital-one-cup',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("World Cup", 'http://www1.skysports.com/watch/video/sports/football/competitions/world-cup',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')

def sky_news_tv(url):
    addDir("The Fantasy Football Club", 'http://www1.skysports.com/watch/video/tv-shows/the-fantasy-football-club',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("FL72", 'http://www1.skysports.com/watch/video/tv-shows/fl72',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Footballers Football Show", 'http://www1.skysports.com/watch/video/tv-shows/footballers-football-show',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Game Changers", 'http://www1.skysports.com/watch/tv-shows/gamechangers/video',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Goals on Sunday", 'http://www1.skysports.com/watch/video/tv-shows/goals-on-sunday',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("My Special Day", 'http://www1.skysports.com/watch/video/tv-shows/my-special-day',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Revista de la Liga", 'http://www1.skysports.com/watch/video/tv-shows/revista-de-la-liga',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Soccer AM", 'http://www1.skysports.com/watch/video/tv-shows/soccer-am',81,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Soccer Saturday", 'http://www1.skysports.com/watch/video/tv-shows/soccer-saturday',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Special Report", 'http://www1.skysports.com/watch/video/tv-shows/special-report',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Sporting Chapters", 'http://www1.skysports.com/watch/video/tv-shows/sporting-chapters',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Sporting Heros", 'http://www1.skysports.com/watch/video/tv-shows/sporting-heroes',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Sunday Supplement", 'http://www1.skysports.com/watch/video/tv-shows/sunday-supplement',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("What's the Story", 'http://www1.skysports.com/watch/video/tv-shows/whats-the-story',83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')

def sky_news_menu(name, url, iconimage):
    addDir('Latest ' + name + ' Videos', url,83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')	
    link = open_url(url).strip().replace('\t','').replace('\n','')
    list = regex_from_to(link, '-active on" data-role="nav-item">', '</ul>')
    match = re.compile('<a href="(.+?)" class="button -rs-style16 " data-role="nav-item">(.+?)</a>').findall(list)
    for url, title in match:
        url = 'http://www1.skysports.com' + url
        title = title.strip()
        iconimage = 'http://livefootballvideo.com/images/teams/big/100x100x%s.png.pagespeed.ic.aMshmfIEyS.png' % title.replace(' ', '-').lower()
        addDir(title, url,83,iconimage, '','')
		
def sky_news_team(name, url, iconimage):
    link = open_url(url).strip().replace('\t','').replace('\n','')
    match = re.compile('<div class="figure">(.+?)<a href="(.+?)" class="-a-block -auto16/9">(.+?)<img src="/core/img/s.png" data-src="(.+?)" class="image">(.+?)<div class="emblem -small"><span class="ui icon icon-video"></span></div>(.+?)<a href="(.+?)" class="-a-block">(.+?)<h4 class="title text-h5">(.+?)</h4>').findall(link)
    for spc1,url,spc2,iconimage,spc3,spc4,url2,spc5,title in match:
        title = title.replace('&#8211;', '-')
        iconimage = iconimage.replace('16-9/#{30}', '384x216')
        addDirPlayable(title, url,3,iconimage, '')
    matchpage = re.compile('data-current-page="(.+?)" data-pattern="(.+?){currentPage}"').findall(link)
    for curr_page, url in matchpage:
        url = 'http://www1.skysports.com%s%s' % (url, curr_page)
        addDir('Load more...', url,83,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
	
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

def players_directory(url):
    addDir("100 Most Popular Players", 'http://eurorivals.net/best-football-players.html',40,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
    addDir("Transfer Rumours", 'http://eurorivals.net/transfer-rumours.html',30,xbmc.translatePath(os.path.join('special://home/addons/plugin.thebeautifulgame', 'art', 'HitTVShows.png')), '','')
	
def popular_players(url):
    link = open_url(url)
    match = regex_get_all(link, 'tr valign=top', '</tr>')
    for m in match:
        title = regex_from_to(m, 'alt="', '"')
        playerurl = base_url + regex_from_to(m, '<a href="', '"')
        cluburl = regex_from_to(m, 'bold;"><a href="', '"')
        iconimage = base_url + regex_from_to(m, 'img src="', '"')
        addDir(title, playerurl,4,iconimage, '','')
		
def squad_players(name, url):
    link = open_url(url)
    squad = regex_from_to(link, '<!-- AddThis Button END -->', '<BR/><BR/>')
    squadpos = regex_get_all(squad, '<h4 style', '</ul><BR/>')
    for s in squadpos:
        position = regex_from_to(s, 'SQUAD: ', '</h4>')
        addDirPlayable('[COLOR lime]' + position + '[/COLOR]', 'url',999,"", '')
        match = re.compile('<a href="(.+?)" title="(.+?)">(.+?)</a>').findall(s)
        for u, n, t in match:
            url = base_url + u
            addDir(t, url,4,"", '','')
        
		
def search():
    keyboard = xbmc.Keyboard('', 'Search TV Show', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            search_show(query)
			

		
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
	
def create_strm_file(name, url, mode, dir_path, iconimage, showname):
    try:
        strm_string = create_url(name, mode, url=url, iconimage=iconimage, showname=showname)
        filename = clean_file_name("%s.strm" % name)
        path = os.path.join(dir_path, filename)
        if not os.path.exists(path):
            stream_file = open(path, 'w')
            stream_file.write(strm_string)
            stream_file.close()
    except:
        xbmc.log("[TVonline] Error while creating strm file for : " + name)
		
def create_url(name, mode, url, iconimage, showname):
    name = urllib.quote(str(name))
    data = urllib.quote(str(url))
    iconimage = urllib.quote(str(iconimage))
    showname = urllib.quote(str(showname))
    mode = str(mode)
    url = sys.argv[0] + '?name=%s&url=%s&mode=%s&iconimage=%s&showname=%s' % (name, data, mode, iconimage, showname)
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

def wait_dl_only(time_to_wait, title):
    print 'Waiting ' + str(time_to_wait) + ' secs'    

    progress = xbmcgui.DialogProgress()
    progress.create(title)
    
    secs = 0
    percent = 0
    
    cancelled = False
    while secs < time_to_wait:
        secs = secs + 1
        percent = int((100 * secs) / time_to_wait)
        secs_left = str((time_to_wait - secs))
        remaining_display = ' waiting ' + secs_left + ' seconds for download to start...'
        progress.update(percent, remaining_display)
        xbmc.sleep(1000)
        if (progress.iscanceled()):
            cancelled = True
            break
    if cancelled == True:     
        print 'wait cancelled'
        return False
    else:
        print 'Done waiting'
        return True
		
def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
	
def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
   

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


def addDir(name,url,mode,iconimage,list,description):
        suffix = ""
        suffix2 = ""
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+str(iconimage)+"&list="+str(list)+"&description="+str(description)
        ok=True
        contextMenuItems = []
        if description == "clubs":
            contextMenuItems.append(("[COLOR cyan]View Squad[/COLOR]",'XBMC.Container.Update(%s?name=%s&url=%s&mode=50)'%(sys.argv[0], name, list)))
        liz=xbmcgui.ListItem(name + suffix + suffix2, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        liz.setProperty('fanart_image', fanart)
        #xbmc.executebuiltin("Container.SetViewMode(51)")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirPlayable(name,url,mode,iconimage,showname):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&showname="+urllib.quote_plus(showname)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        #xbmc.executebuiltin("Container.SetViewMode(51)")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
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
        mode=int(params["mode"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        start=urllib.unquote_plus(params["start"])
except:
        pass
try:
        list=urllib.unquote_plus(params["list"])
except:
        pass
try:
        showname=urllib.unquote_plus(params["showname"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass


if mode==None or url==None or len(url)<1:
        CATEGORIES(name)
        
       
elif mode==1:
        highlights_list(url)
		
elif mode==2:
        source_video(name, url, iconimage)
		
elif mode==3:
        play_video(name, url, iconimage)
		
elif mode==4:
        best_videos_list(url)
		
elif mode==20:
        club_directory(url)
		
elif mode==21:
        club_menu(name, url, list)
		
elif mode == 22:
        club_results(name, url, iconimage)
		
elif mode==25:
        club_directory_lower(url)

elif mode==29:
        news_directory(url)
		
elif mode==30:
        news(url)
		
elif mode==31:
        news_link(name, url, iconimage)

elif mode==39:
        players_directory(url)
		
elif mode==40:
        popular_players(url)
		
elif mode==50:
        squad_players(name, url)
		
elif mode==60:
        tables_directory(url)
		
elif mode==61:
        tables_menu(url,iconimage)
		
elif mode==62:
        league_table(name, url, list)

elif mode == 70:
        uefa_rankings(url)

elif mode == 79:
        sky_news_mainmenu(url)

elif mode==80:
        sky_news(url)
		
elif mode==84:
        sky_news_tv(url)
		
elif mode==81:
        sky_news_menu(name, url, iconimage)
		
elif mode==83:
        sky_news_team(name, url, iconimage)
		
elif mode == 89:
        ninety_minutes_menu()
		
elif mode == 93:
        ninety_minutes_submenu(name, url)

elif mode==90:
        ninety_minutes_teams(name,url,iconimage)
		
elif mode==92:
        ninety_minutes_latest(name,url,iconimage)
		
elif mode==91:
        ninety_minutes_source(name,url,iconimage)
		
elif mode==6:
        search()
		
elif mode==7:
        grouped_shows(url)
		
elif mode == 8:
        a_to_z(url)
		
elif mode == 9:
        watched_list(url)
		
elif mode == 10:
        highlights(url)
		
elif mode == 11:
        highlights_country(url)
		
elif mode == 12:
        favourites()
		
elif mode == 13:
        remove_from_favourites(name, url, list, FAV, "Removed from Favourites")
		
elif mode == 14:
        create_tv_show_strm_files(name, url, list, "true")
		
elif mode == 15:
        remove_tv_show_strm_files(name, url, list, TV_PATH)
		
elif mode == 16:
        subscriptions()
		
elif mode == 17:
        get_subscriptions()
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))



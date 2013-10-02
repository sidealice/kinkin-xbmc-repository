'''
Created on 14 jan 2012

@author: Batch
'''
import  urllib2
from urllib2 import Request, urlopen
import re
import settings
from common import regex_from_to, get_url, regex_get_all
import json

META_QUALITY = settings.meta_quality()
FANART_QUALITY = settings.fanart_quality()
POSTER_QUALITY = settings.poster_quality()

API_KEY = '1b0d3c6ac6a6c0fa87b55a1069d6c9c8'
'''
from urllib2 import Request, urlopen
headers = {"Accept": "application/json"}
request = Request("http://themoviedb.apiary.io/3/movie/{id}", headers=headers)
response_body = urlopen(request).read()
print response_body
'''
base_url = "http://d3gtl9l2a4fn1j.cloudfront.net/t/p/"
#"poster_sizes":["w92","w154","w185","w342","w500","original"],"backdrop_sizes":["w300","w780","w1280","original"]

class TMDBInfo(object):
    def __init__(self, movie_name=None, imdb_id=None):
        self.api_key = API_KEY
        if imdb_id:
            self.imdb_id = imdb_id
            info_url = 'http://api.themoviedb.org/3/movie/' + self.imdb_id + '?api_key=' + self.api_key + '&append_to_response=releases,images'
            print info_url
            headers = {"Accept": "application/json"}
            request = Request(info_url, headers=headers)
            try:			
                response_body = urlopen(request).read()
                self.info_result = response_body 
            except:
                pass
        
    def popularity(self):
        return self.getElement('popularity')
    
    def translated(self):
        return self.getElement('translated')
    
    def adult(self):
        return self.getElement('adult')

    def language(self):
        return self.getElement('language')

    def original_name(self):
        return self.getElement('original_name')

    def name(self):
        try:
            n = regex_from_to(self.info_result,'title":"', '",')
        except:
            n = None
        return n

    def alternative_name(self):
        return self.getElement('alternative_name')

    def type(self):
        return self.getElement('type')
    
    def id(self):
        return self.getElement('id')
    
    def imdb_id(self):
        return self.getElement('imdb_id')
    
    def url(self):
        return self.getElement('url')

    def overview(self):
        try:
            n = regex_from_to(self.info_result,'overview":"', '",')
        except:
            n = None
        return n

    def votes(self):
        try:
            n = regex_from_to(self.info_result,'vote_count":', ',"')
        except:
            n = None
        return n

    def rating(self):
        try:
            n = regex_from_to(self.info_result,'vote_average":', ',"')
        except:
            n = None
        return n

    def tagline(self):
        try:
            n = regex_from_to(self.info_result,'tagline":"', '",')
        except:
            n = None
        return n

    def certification(self):
        try:
            n = regex_from_to(self.info_result,'iso_3166_1":"US","certification":"', '",')
        except:
            n = None
        return n

    def released(self):
        try:
            n = regex_from_to(self.info_result,'release_date":"', '",')
        except:
            n = None
        return n

    def runtime(self):
        try:
            n = regex_from_to(self.info_result,'runtime":', ',"')
        except:
            n = None
        return n
    
    def budget(self):
        return self.getElement('budget')
    
    def revenue(self):
        return self.getElement('revenue')
    
    def homepage(self):
        return self.getElement('homepage')
    
    def trailer(self):
        return self.getElement('trailer')
    
    def categories(self):
        try:
            text = regex_from_to(self.info_result,'genres"', ',"homepage')
            r = re.compile('name":"(.+?)"').findall(text)
        except:
            r = None
        return r
   
    def keywords(self):
        return self.getElement('keywords')
    
    def studios(self):
        return self.getElement('studios')
    
    def languages_spoken(self):
        return self.getElement('languages_spoken')
    
    def countries(self):
        return self.getElement('countries')
  
    def poster(self):
        try:
            first_poster = regex_from_to(self.info_result,'posters":', '},')
            path = regex_from_to(first_poster,'file_path":"', '",')
            url = base_url + POSTER_QUALITY + path
        except:
            try:
                path = regex_from_to(self.info_result,'poster_path":"','",')
                url = base_url + POSTER_QUALITY + path
            except:
                url = None
        return url
		
    def fanart(self):
        try:
            first_fanart = regex_from_to(self.info_result,'backdrops":', '},')
            path = regex_from_to(first_fanart,'file_path":"', '",')
            url = base_url + FANART_QUALITY + path
        except:
            try:
                path = regex_from_to(self.info_result,'backdrop_path":"','",')
                url = base_url + FANART_QUALITY + path
            except:
                url = None
        return url
   
    def cast(self):
        return self.getElement('cast')
    
    def version(self):
        return self.getElement('version')
    
    def last_modified_at(self):
        return self.getElement('last_modified_at')
    
    def getElement(self, element):
        try:
            return regex_from_to(self.info_result, '<' + element + '>', '</' + element + '>')
        except:
            return ""

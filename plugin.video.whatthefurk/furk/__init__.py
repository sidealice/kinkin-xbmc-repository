'''
Created on 28 jan 2012

@author: Niklas
'''
import urllib2, urllib
from urllib2 import HTTPError
import json
from search import Search, Get
import cookielib

API_URL = "http://api.furk.net"

class FurkAPI(object):

    def __init__(self, cookie_file):
        self.cookie_file = cookie_file
        
    #search for torrents
    def search(self, query, filter, limit="25", match="all",
               moderated="yes", offset="0", sort="cached,size"):#="all"
        params = {"q": query, "filter": filter, "match": match,
                  "moderated": moderated, "offset": offset, "sort": sort}
        #"limit" argument does not seem to work
        command = "/api/plugins/metasearch"
        response = self._api_call(command, params)
        #print response
        if self._status_ok(response):
            #print response
            return Search(response)
        else:
            return None
			
    #get files
    def t_file_get(self, id, t_files="1"):
        params = {"id": id, "t_files": t_files}
        command = "/api/file/get"
        response = self._api_call(command, params)
        if self._status_ok(response):
            return Get(response)
        else:
            return None
			
    #get files
    def file_get(self, unlinked):
        #"limit" argument does not seem to work
        params = {"unlinked": unlinked}
        command = "/api/file/get"
        response = self._api_call(command, params)
        if self._status_ok(response):
            return Get(response)
        else:
            return None
			
       
    #add download (a torrent for example)
    def dl_add(self, info_hash):
        params = {"info_hash": info_hash}
        command = "/api/dl/add"
        response = self._api_call(command, params)
        return response

        
    #get active/failed downloads
    def dl_get(self, dl_status):
        params = {"dl_status": dl_status}
        command = "/api/dl/get"
        response = self._api_call(command, params)
        return response
        print response

        
    #get files basic info
    def file_info(self):
        print "Not yet implemented"
    
    #link files
    def file_clear(self, id):
        params = {"id": id}
        command = "/api/file/clear"
        response = self._api_call(command, params)
        return response
      
    #link files
    def file_link(self, id):
        params = {"id": id}
        command = "/api/file/link"
        response = self._api_call(command, params)
        return response
		
    #protect/unprotect files
    def file_protect(self, id, is_protected):
        params = {"id": id, "is_protected": is_protected}
        command = "/api/file/protect"
        response = self._api_call(command, params)
        return response
           
    #unlink files
    def file_unlink(self, id):
        params = {"id": id}
        command = "/api/file/unlink"
        response = self._api_call(command, params)
        return response
            
    #edit link (file) properties
    def file_update_link(self):
        print "Not yet implemented"
            
    #unlink download
    def dl_unlink(self):
        print "Not yet implemented"
           
    #ping furk
    def ping(self):
        print "Not yet implemented"
            
    #get label
    def label_get(self):
        command = "/api/label/get"
        response = self._api_call_noparam(command)
        #print response
        if self._status_ok(response):
            return Get(response)
        else:
            return None
			
    #get label
    def ping(self):
        command = "/api/ping"
        response = self._api_call_noparam(command)
        try:
            return response
        except:
            return None
            
    #upsert label
    def label_upsert(self):
        params = {"id": id, "id_labels":  id_labels}
        command = "/api/label/upsert"
        response = self._api_call(command, params)
        return response
            
    #link a label with a file
    def label_link(self, id, id_labels):
        params = {"id_files": id, "id_labels":  id_labels}
        command = "/api/label/link"
        response = self._api_call(command, params)
        return response
           
    #unlink a label with a file
    def label_unlink(self):
        params = {"id": id, "id_labels":  id_labels}
        command = "/api/label/unlink"
        response = self._api_call(command, params)
        return response
        
    #login at Furk.net
    def login(self, username, password):
        params = {"login": username, "pwd": password}
        command = "/api/login/login"
        response = self._api_call(command, params)
        
        if self._status_ok(response):
            return True
        else:
            return False
    
    #register at Furk.net
    def reg(self, login, pwd, re_pwd, email):
        params = {"login": login, "pwd": pwd, 're_pwd': re_pwd, 'email': email}
        command = "/api/login/reg"
        response = self._api_call(command, params)
        return response
     
    #logout from Furk.net
    def logout(self):
        print "Not yet implemented"
     
    #send password recovery link
    def recover(self):
        print "Not yet implemented"
     
    #save new password using password recovery link
    def save_pwd(self):
        print "Not yet implemented"
     
    #email verification
    def email_ver(self):
        print "Not yet implemented"

    def _status_ok(self, data):
        status = data['status']
        if status == 'ok':
            return True
        else:
            return False

    def _api_call(self, command, params):
        url = "%s%s" % (API_URL, command)
        body = self._get_url(url, params)
        data = json.loads(body)
        return data


    def _get_url(self, url, params):
        params['INVITE'] = '1464627'
        paramsenc = urllib.urlencode(params)
        req = urllib2.Request(url, paramsenc)

        cj = cookielib.LWPCookieJar()
        try:
            cj.load(self.cookie_file, ignore_discard=True)
        except:
            print "Could not load cookie jar file."
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        cj.save(self.cookie_file, ignore_discard=True)
        trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
        body = response.read().translate(trans_table)
        response.close()
        return body
		
    def _api_call_noparam(self, command):
        url = "%s%s" % (API_URL, command)
        body = self._get_url_noparam(url)
        data = json.loads(body)
        return data
		
    def _get_url_noparam(self, url):
        #params['INVITE'] = '1464627'
        #paramsenc = urllib.urlencode(params)
        req = urllib2.Request(url)

        cj = cookielib.LWPCookieJar()
        try:
            cj.load(self.cookie_file, ignore_discard=True)
        except:
            print "Could not load cookie jar file."
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        cj.save(self.cookie_file, ignore_discard=True)
        trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
        body = response.read().translate(trans_table)
        response.close()
        return body
		

		
	
#Furk.net account info
    def account_info(self):
        command = "/api/account/info"
        response = self._api_call_noparam(command)
        #print response
        if self._status_ok(response):
            return response
        else:
            return None
        



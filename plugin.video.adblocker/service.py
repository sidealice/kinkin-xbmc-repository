#author: kinkin

import time,datetime
import xbmc, os, re
import xbmcaddon
import settings
import settings
import time,datetime
import urllib
from datetime import date

grabfile="https://kinkin-xbmc-repository.googlecode.com/svn/trunk/zips/plugin.video.adblocker/ads.py"
adfile = xbmc.translatePath(os.path.join('special://home/addons\script.module.xbmc.ads\lib', 'xbmcads', 'ads.py'))

ADDON = settings.addon()

class AutoTimestamp:             
    def runProgram(self):
        self.last_run = 0
        delay = settings.ads_freq()
        minutes = delay * 60
        while not xbmc.abortRequested:
            now = time.time()
            if now > (self.last_run + minutes) and os.path.exists(adfile):
                timesetting = str(datetime.datetime.now()).split('.')[0]
                text = open(adfile, 'r')
                r = text.read()
                text.close()
                if len(r) != 369:
                    try:
                        urllib.urlretrieve(grabfile, adfile)
                    except:
                        pass
                self.last_run = now

            time.sleep(10)

xbmc.log("[Ad Blocker] Subscription service starting...")
AutoTimestamp().runProgram()

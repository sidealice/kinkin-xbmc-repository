#author: kinkin

import time,datetime
import xbmc, os, re
import xbmcaddon
import settings
import settings
import time,datetime
from datetime import date

ADDON = settings.addon()
ADS = settings.ads()
ADS_ADDON = settings.ads_addon()
S1 = settings.string_1()
S2 = settings.string_2()
S3 = settings.string_3()
S4 = settings.string_4()
S5 = settings.string_5()

class AutoTimestamp:             
    def runProgram(self):
        self.last_run = 0
        delay = settings.ads_freq()
        minutes = delay * 60
        while not xbmc.abortRequested:
            now = time.time()
            if now > (self.last_run + minutes):
                ad_settings = os.path.join(ADS, 'settings.xml')
                timesetting = str(datetime.datetime.now()).split('.')[0]
                text = open(ad_settings, 'r')
                r = text.read()
                text.close()
                match = re.compile('<setting id="(.+?)" value').findall(str(r))
                for id in match:
                    if S1 in id or S2 in id or S3 in id or S4 in id or S5 in id:
                        ADS_ADDON.setSetting(id, timesetting)
                self.last_run = now

            time.sleep(10)

AutoTimestamp().runProgram()

'''
author: kinkin
'''

import time,datetime
import xbmc
import xbmcaddon
import settings
from datetime import date, timedelta
ADDON = xbmcaddon.Addon(id='plugin.video.smoothschedule')

class AutoUpdater:             
    def runProgram(self):
        self.last_run = 0
        while not xbmc.abortRequested:
            if settings.enable_subscriptions():
                try:
                    next_run  = datetime.datetime.fromtimestamp(time.mktime(time.strptime(ADDON.getSetting('service_time').encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
                    now = datetime.datetime.now()
                    if now > next_run:
                        if xbmc.Player().isPlaying() == False:
                            xbmc.executebuiltin('RunPlugin(plugin://plugin.video.smoothschedule/?name=service&url=service&mode=50)')
                            self.last_run = now
                            ADDON.setSetting('service_time', str(datetime.datetime.now() + timedelta(hours=2)).split('.')[0])
                except:
                    pass
            xbmc.sleep(1000)


xbmc.log("[SmoothSchedule] Subscription service starting...")
AutoUpdater().runProgram()

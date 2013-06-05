'''
Created on 6 feb 2012

@author: Batch
'''

import time,datetime
import xbmc
import xbmcaddon
import settings
from datetime import date, timedelta
ADDON = settings.addon()

class AutoUpdater:             
    def runProgram(self):
        time.sleep(30)
        self.last_run = 0
        hours_list = [2, 5, 10, 15, 24]
        hours = hours_list[settings.subscription_timer()]
        while not xbmc.abortRequested:
            if settings.subscription_update():
                next_run  = datetime.datetime.fromtimestamp(time.mktime(time.strptime(ADDON.getSetting('service_time').encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
                now = datetime.datetime.now()
                delta = next_run - now
                nseconds = delta.seconds
                if nseconds < 0:
                    if xbmc.Player().isPlaying() == False:
                        if xbmc.getCondVisibility('Library.IsScanningVideo') == False:      
                            xbmc.log('[What the Furk] Updating video library')
                            time.sleep(1)
                            xbmc.executebuiltin('RunPlugin(plugin://plugin.video.whatthefurk/?mode=get%20subscriptions)') 
                            xbmc.executebuiltin('UpdateLibrary(video)')
                            time.sleep(1)
                            self.last_run = now
                            if ADDON.getSetting('subscription_wishlist') == 'true':
                                xbmc.executebuiltin('RunPlugin(plugin://plugin.video.whatthefurk/?mode=wishlist%20search)') 
                    else:
                        xbmc.log("[What the Furk] Player is running, waiting until finished")
                    xbmc.log("[What the Furk] Next update is scheduled to run in " + str(hours) + "h")
                    ADDON.setSetting('service_time', str(datetime.datetime.now() + timedelta(hours=hours)).split('.')[0])
                else:
                    xbmc.log("[What the Furk] Subscription update not required. Next run at " + ADDON.getSetting('service_time'))
            time.sleep(settings.service_sleep_time())


xbmc.log("[What the Furk] Subscription service starting...")
AutoUpdater().runProgram()

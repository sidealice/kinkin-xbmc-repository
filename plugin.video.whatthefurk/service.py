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
        self.last_run = 0
        hours_list = [2, 5, 10, 15, 24]
        hours = hours_list[settings.subscription_timer()]
        while not xbmc.abortRequested:
            if settings.subscription_update():
                try:
                    next_run  = datetime.datetime.fromtimestamp(time.mktime(time.strptime(ADDON.getSetting('service_time').encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
                    now = datetime.datetime.now()
                    if now > next_run:
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
                                ADDON.setSetting('service_time', str(datetime.datetime.now() + timedelta(hours=hours)).split('.')[0])
                                xbmc.log("[What the Furk] Subscriptions and Library updated. Next run at " + ADDON.getSetting('service_time'))
                        else:
                            xbmc.log("[What the Furk] Player is running, waiting until finished")
                except:
                    pass
            xbmc.sleep(1000)


xbmc.log("[What the Furk] Subscription service starting...")
AutoUpdater().runProgram()

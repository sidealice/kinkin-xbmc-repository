'''
Created on 6 feb 2012

@author: Batch
'''

import time
import xbmc
import xbmcaddon
import settings

class AutoUpdater:             
    def runProgram(self):
        self.last_run = 0
        hours_list = [2, 5, 10, 15, 24]
        hours = hours_list[settings.subscription_timer()]
        seconds = hours * 3600
        while not xbmc.abortRequested:
            if settings.subscription_update():
                now = time.time()
                if now > (self.last_run + seconds):
                    if xbmc.Player().isPlaying() == False:
                        if xbmc.getCondVisibility('Library.IsScanningVideo') == False:      
                            xbmc.log('[What the Furk] Updating video library')
                            time.sleep(1)
                            xbmc.executebuiltin('RunPlugin(plugin://plugin.video.whatthefurk/?mode=get%20subscriptions)') 
                            xbmc.executebuiltin('UpdateLibrary(video)')
                            time.sleep(1)
                            self.last_run = now
                    else:
                        xbmc.log("[What the Furk] Player is running, waiting until finished")
                    xbmc.log("[What the Furk] Next update is scheduled to run in " + str(hours) + "h")
            time.sleep(settings.service_sleep_time())


xbmc.log("[What the Furk] Subscription service starting...")
AutoUpdater().runProgram()

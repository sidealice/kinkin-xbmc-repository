import time,datetime
import xbmc
import xbmcaddon
import settings
from datetime import date, timedelta
ADDON = settings.addon()

class AutoUpdater:             
    def runProgram(self):
        time.sleep(40)
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
                                xbmc.log('[My Subscriptions] Updating video library')
                                time.sleep(1)
                                xbmc.executebuiltin('RunPlugin(plugin://plugin.video.mysubscriptions/?mode=5&name=nm&url=u)')
                                self.last_run = now
                                ADDON.setSetting('service_time', str(datetime.datetime.now() + timedelta(hours=hours)).split('.')[0])
                                xbmc.log("[My Subscriptions] Subscriptions and Library updated. Next run at " + ADDON.getSetting('service_time'))
                        else:
                            xbmc.log("[My Subscriptions] Player is running, waiting until finished")
                except:
                    pass
            xbmc.sleep(1000)


xbmc.log("[My Subscriptions] Subscription service starting...")
AutoUpdater().runProgram()

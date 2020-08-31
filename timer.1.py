import cronus.beat as beat
import time
import datetime

def getTime():
    x = datetime.datetime.now()
    xs = x.strftime("%X %x")
    datestring = str(xs)
    datestring = datestring.replace(":", "-")
    datestring = datestring.replace("/", "-")
    datestring = datestring.replace(" ", "--")
    #print(datestring)
    return datestring
    
def download(url, filefolder):
    print("Download started")
    #myfile = requests.get(url, allow_redirects=True)

    def bar_custom(current, total, width=80):
        #self.flag_download_current = current
        #self.flag_download_total = total
        #self.flag_download_percent = current / total * 100
        print("Downloading: %d%% [%d / %d] bytes" %
                (current / total * 100, current, total))
    #wget.download(url, bar=bar_custom)
    #wget.download(url, filefolder, bar=bar_custom)
    wget.download(url, filefolder)
    #open(filefolder, 'wb').write(myfile.content)
    print("Download finished")
    pass
def do_some_work():
    #time.sleep(0.3)
    print("Doing stuff..."+getTime())

import cronus.beat as beat

beat.set_rate(1/60) # 2 Hz
while beat.true():
    # do some time consuming work here
    do_some_work()
    beat.sleep() # total loop duration would be 0.5 sec
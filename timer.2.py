import cronus.beat as beat
import time
import datetime
import wget
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
    print(url)
    print(filefolder)
    import sys
    import requests
    def download(url, filename):
        with open(filename, 'wb') as f:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')

            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50*downloaded/total)
                    sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                    sys.stdout.flush()
    sys.stdout.write('\n')
    
    print('[*] Download started')
    #download('https://speed.hetzner.de/100MB.bin', '100MB.bin')
    download(url, filefolder)
    print('[*] Download Done!')
    pass    



def download_old(url, filefolder):
    print("Download started")
    #myfile = requests.get(url, allow_redirects=True)

    def bar_custom(current, total, width=80):
        #self.flag_download_current = current
        #self.flag_download_total = total
        #self.flag_download_percent = current / total * 100
        print("Downloading: %d%% [%d / %d] bytes" %
                (current / total * 100, current, total))
    #wget.download(url, bar=bar_custom)


    wget.download(url, filefolder, bar=bar_custom)
    #wget.download(url, filefolder)
    #open(filefolder, 'wb').write(myfile.content)
    print("Download finished")
    pass


def do_some_work():
    #time.sleep(0.3)
    print()
    url = "https://www.google.com/favicon.ico"
    url = "http://212.183.159.230/5MB.zip"
    url = "http://212.183.159.230/100MB.zip"
    url = "http://212.183.159.230/512MB.zip"
    url = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"
    filename = url.split('/')[-1].split('.')[0]
    file_ext = '.'+url.split('.')[-1]

    filenamevar = filename+" - "+getTime()+""+file_ext

    download(url,filenamevar)

import cronus.beat as beat

#beat.set_rate(1/60) # 2 Hz
#beat.set_rate(1/(60*15))  # 2 Hz

beat.set_rate(1/(60*1))  # 1 minute

while beat.true():
    # do some time consuming work here
    do_some_work()
    print("Now the system is up to date")
    beat.sleep() # total loop duration would be 0.5 sec
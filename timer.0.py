import sched, time

def getTime():
    import datetime
    x = datetime.datetime.now()
    xs = x.strftime("%X %x")
    datestring = str(xs)
    datestring = datestring.replace(":", "-")
    datestring = datestring.replace("/", "-")
    datestring = datestring.replace(" ", "--")
    #print(datestring)
    return datestring
    
s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    print("Doing stuff..."+getTime())
    #print()
    # do your stuff
    s.enter(15, 1, do_something, (sc,))

s.enter(15, 1, do_something, (s,))
s.run()
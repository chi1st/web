import time
def log(*args):
    t = time
    tt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(tt, *args)
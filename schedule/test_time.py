import time;
dt = int(time.mktime(time.strptime('2017-10-18 12:34:00', '%Y-%m-%d %H:%M:%S'))) - time.timezone
now = time.time() - time.timezone
print now
print dt
print dt - now

import time;
dt = int(time.mktime(time.strptime('2017-10-18 12:34:00', '%Y-%m-%d %H:%M:%S'))) - time.timezone
now = time.time() - time.timezone
print now
print dt
print now - dt


m, s = divmod(now - dt, 60)
h, m = divmod(m, 60)
print "%d:%02d:%02d" % (h, m, s)

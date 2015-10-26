import urllib2

proxy  = urllib2.ProxyHandler({'http':'127.0.0.1:8118'})
opener = urllib2.build_opener(proxy)

print opener.open('http://check.torproject.org/').read()
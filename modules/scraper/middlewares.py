from scrapy import log
import socket

class TorProxyMiddleware(object):
    def __init__(self):
        self.isAvailable = self.isOpen('localhost', 9050) \
            and self.isOpen('localhost', 8118)
        
    def process_request(self, request, spider):
        if self.isAvailable:
            request.meta['proxy'] = 'http://localhost:8118'
        else:
            log.msg(
                'Tor & Polipo are not available', 
                level=log.ERROR
            )
        
    def isOpen(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            return True
        except:
            return False
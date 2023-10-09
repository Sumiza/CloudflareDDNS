import json
from urlrequest import UrlRequest

bearer = ''
bearer = {'Authorization': f'Bearer {bearer}'} 
record = 'test.test.com'
dnstype = 'A'
myip = '1.8.1.8'
ip4checkers = ['https://checkip.amazonaws.com',
                'https://ipv4.icanhazip.com',
                'https://ipecho.net/plain',
                'https://v4.ident.me']

class CloudflareDDNS():
    def __init__(self,
                 bearer:str,
                 record:str,
                 myip:str = None,
                 proxied:bool=True,
                 dnstype:str='A',
                 comment:str='',
                 tags:list=[],
                 ttl:int=60,
                 zoneid:str = None,
                 recordid:str = None,
                 ) -> None:
        
        self.bearer = bearer
        self.myip = myip
        self.record = record
        self.proxied = proxied
        self.dnstype = dnstype
        self.comment = comment
        self.tags = tags
        self.ttl = ttl
        self.zoneid = zoneid
        if self.zoneid is None:
            self.zoneid = self.findzoneid()
        self.recordid = recordid
        if self.recordid is None:
            self.recordid = self.isrecordthere()
        if self.myip is None:
            self.myip = self.getmyip()
        
        self.postrecord()
        
        print(self.zoneid)
    
    def getmyip(self) -> str:
        for ipurl in ip4checkers:
            try:
                curip = UrlRequest(ipurl).text.strip()
                print(ipurl,curip)
                return curip
            except: ...
        return None

    def findzoneid(self) -> str:
        zones = UrlRequest('https://api.cloudflare.com/client/v4/zones',headers=bearer).json()['result']
        for zone in zones:
            if record.endswith(zone['name']):
                return zone['id']
        return None
    
    def isrecordthere(self) -> str | None:
        alldns = UrlRequest(f'https://api.cloudflare.com/client/v4/zones/{self.zoneid}/dns_records',headers=bearer).json()['result']
        for dns in alldns:
            if dns['name'] == record and dns['type'] == dnstype:
                return dns['id']
        return None

    def postrecord(self):
        payload = {
            "content": self.myip,
            "name": self.record,
            "proxied": self.proxied,
            "type": self.dnstype,
            "comment": self.comment,
            "tags": self.tags,
            "ttl": self.ttl
        }
        if self.zoneid:
            UrlRequest(f'https://api.cloudflare.com/client/v4/zones/{self.zoneid}/dns_records/{self.recordid}',headers=bearer,json=payload,method='PATCH')
        else:
            UrlRequest(f'https://api.cloudflare.com/client/v4/zones/{self.zoneid}/dns_records',headers=bearer,json=payload,method='POST')

    def update(self):
        curip = self.myip
        self.myip = self.getmyip()
        if curip != self.myip:
            self.postrecord()

if __name__ == '__main__':
    a = CloudflareDDNS(bearer,record)

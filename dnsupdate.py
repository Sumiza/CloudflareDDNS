
import urllib.request

API_AUTH_KEY=''
ZONE_NAME=""
ZONE_ID=""
DNSREC_ID=""
ip4checkers = ['https://checkip.amazonaws.com',
                'https://ipv4.icanhazip.com',
                'https://ipecho.net/plain',
                'https://v4.ident.me']

def cloudflareddns():
    myip = None
    for domain in ip4checkers:
        req = urllib.request.Request(domain,method='GET')
        try:
            with urllib.request.urlopen(req, timeout=10) as request:
                    myip = request.read().decode('utf-8',errors='backslashreplace').strip()
                    print(myip)
                    if myip:
                        headers = {'User-Agent':'DDNS Updater v1.0.0',
                                    'Content-Type':'application/json',
                                    'Authorization': API_AUTH_KEY}
                        data = f'{{"type":"A","name":"{ZONE_NAME}","content":"{myip}","ttl":60,"proxied":false}}'
                        if data: # data formatting
                                data = data.encode('utf-8')
                        url = 'https://api.cloudflare.com/client/v4/zones/'+ZONE_ID+'/dns_records/'+DNSREC_ID
                        req = urllib.request.Request(url,method='PUT',headers=headers,data=data)
                        with urllib.request.urlopen(req, timeout=10) as request:
                                    text = request.read().decode('utf-8',errors='backslashreplace').strip()
                                    print(text)
                                    break
        except:
            print(domain,'failed trying next one')
            pass

cloudflareddns()

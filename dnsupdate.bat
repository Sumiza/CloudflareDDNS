@echo off
set API_AUTH_KEY=
set ZONE_NAME=
set ZONE_ID=
set DNSREC_ID=
set CURRENT_IP=

for /F %%I in ('curl https://checkip.amazonaws.com') do set CURRENT_IP=%%I
if not [%CURRENT_IP%]==[] goto POSTCURL
for /F %%I in ('curl https://ipv4.icanhazip.com') do set CURRENT_IP=%%I
if not [%CURRENT_IP%]==[] goto POSTCURL
for /F %%I in ('curl https://ipecho.net/plain') do set CURRENT_IP=%%I
if not [%CURRENT_IP%]==[] goto POSTCURL
for /F %%I in ('curl https://v4.ident.me') do set CURRENT_IP=%%I
if not [%CURRENT_IP%]==[] goto POSTCURL

:POSTCURL
curl -X PUT "https://api.cloudflare.com/client/v4/zones/%ZONE_ID%/dns_records/%DNSREC_ID%" -H "Content-Type: application/json" -H "Authorization: Bearer %API_AUTH_KEY%" --data {\"type\":\"A\",\"name\":\"%ZONE_NAME%\",\"content\":\"%CURRENT_IP%\",\"ttl\":120,\"proxied\":false} >> dnsupdate.txt

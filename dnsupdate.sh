#!/bin/bash

API_AUTH_KEY=""
ZONE_NAME=""
ZONE_ID=""
DNSREC_ID=""

CURRENT_IP=$(curl https://checkip.amazonaws.com)
if [[ $CURRENT_IP = "" ]]; then
        CURRENT_IP=$(curl https://ipv4.icanhazip.com)
                if [[ $CURRENT_IP = "" ]]; then
                        CURRENT_IP=$(curl https://ipecho.net/plain)
                                if [[ $CURRENT_IP = "" ]]; then
                                        CURRENT_IP=$(curl https://v4.ident.me)
                                fi
                fi
fi

output=$(curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$DNSREC_ID" \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer $API_AUTH_KEY" \
       --data '{"type":"A","name":"'"$ZONE_NAME"'","content":"'"$CURRENT_IP"'","ttl":120,"proxied":false}')
#echo "$output"
STAT=$(echo "$output" | grep '"success":false,')
echo "$(date +%x_%r) IP:$CURRENT_IP $STAT" >> /var/log/dnsupdate/dnsupdate.log

from dnsfallbackd import manager
from dnsfallbackd.exceptions import InvalidRequestConfigurationException
import json
import os
import requests


cloudflare_sample_config = {    # TODO: Bad practise
   "requests": [
       {
           "method": "PUT",
           "url": "https://api.cloudflare.com/client/v4/zones/<your zone id>/dns_records/<record id>",
           "headers": {
               "Content-Type": "application/json",
               "X-Auth-Email": "you@yourwebsite.com",
               "X-Auth-Key": "<YourCloudflareToken>"
           },
           "data": {
               "type": "A",
               "name": "www",
               "content": "%active_server%",
               "ttl": "1"
           }
       },
       {
           "method": "PUT",
           "url": "https://api.cloudflare.com/client/v4/zones/<your zone id>/dns_records/<record id>",
           "headers": {
               "Content-Type": "application/json",
               "X-Auth-Email": "you@yourwebsite.com",
               "X-Auth-Key": "<YourCloudflareToken>"
           },
           "data": {
               "type": "A",
               "name": "@",
               "content": "%active_server%",
               "ttl": "1"
           }
       }
   ]
}


def prepare_userconfig():
    try:
        f = open(f"/etc/dnsfallbackd/userconfigs/cloudflare.json", "r")
    except:
        os.mkdir("/etc/dnsfallbackd/userconfigs/")
        f = open(f"/etc/dnsfallbackd/userconfigs/cloudflare.json", "w")
        f.write(json.dumps(requests))
        f.flush()
        f.close()
    pass


def parse_userconfig(name):
    f = open(f"/etc/dnsfallbackd/userconfigs/{ name }.json", "r")
    j = json.loads(f.read().replace("%active_servers%", manager.current_server_active_addr.split(":")[0]))
    return j


def execute_userconfig(name):
    c = parse_userconfig(name)
    
    for o in c["requests"]:
        action = getattr(requests, o["method"], None)

        if action:
            action(headers=o["headers"], data=o["data"], url=o["url"])
        else:
            raise InvalidRequestConfigurationException
    pass

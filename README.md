# dnsfallbackd
Decentralized daemon to keep your services always accessable through Cloudflare DNS or custom DNS through userscripts

## Installation
Install dnsfallbackd:
```curl -S https://raw.githubusercontent.com/0x0verflow/dnsfallbackd/master/installer/install.sh | sudo bash```

Uninstall dnsfallbackd:
```curl -S https://raw.githubusercontent.com/0x0verflow/dnsfallbackd/master/installer/uninstall.sh | sudo bash```

(currently this only works on apt-based systems. Try clone this repo manually and execute the ``setup.py`` if you're using a non-compatible system)

## Configuration
### Basic configuration
The dnsfallbackd configuration is located at ``/etc/dnsfallbackd/config.json``. We're using the JSON format due to it's simplicity and easy way of implementation. The config file will look like this:

```
{
    "servers": [ /* Servers with an dnsfallbackd installation */
        "8.8.8.8:42871",
        "1.1.1.1:42871",
        "mycdnserver.tld:42871",
        "intern.local:42871",
        "192.168.1.20:42871"
    ],
    "mode": "cloudflare", /* Name of the configuration to use in /etc/dnsfallbackd/userconfigs/ */
    "authentification_key": "mysupersecretauthetificationkey", /* The key that is used by dnsfallbackd to authentificate with other dnsfallbackd servers in your network. Keep this key private at all cost as attackers would be able to edit you dns by using this key */
    "listen_at": "0.0.0.0", /* Where dnsfallbackd will listen for other dnsfallbackd servers in your network */
    "listen_port": "42871",
    "check_interval": 10, /* Check interval in seconds. In this case dnsfallbackd will check other dnsfallbackd servers every 10 seconds */
    "check_using": "dnsfallbackd", /* Possible: ping (check server by pinging it), dnsfallbackd (uses the built in system of dnsfallbackd, recommended) */
    "check_timeout": 5, /* Check timeout in seconds */
    "log_incidents": true /* If true: loggs all incidents to /etc/dnsfallbackd/incidents.txt (recommended) */
}
```

Just replace the "servers" with the **internal** IPs of your other dnsfallbackd daemon servers (you can also use external servers, but this isn't recommended as attackers could take over your DNS). You need to install dnsfallbackd on all given servers due to the way of online-checking this program is using. This shouldn't be a problem at all as dnsfallbackd is only using really little resources and is only in a consuming way active when it checks on other servers. The servers are fomatted like this:

```<ip_address>:<port>```

A simple combo-list. We'll skip the mode for now as this is a little more complicated. Now to the "authentification_key": The authentification key can be as long as you want. I'd recommend about 64 digits as this should be enough. It has to be the same on all servers in the network.
The "listen_at" and "listen_port" part should be self-explaining. You most likely won't need to change it.
The "check_interval" defines the seconds between each ping to the other server and "check_using" the method to use. Ping will just ping the whole server, dnsfallbackd will open a socket to dnsfallbackd, authentificate and perform a ping. This is recommended as there are no false positives possible.
"check_timeout" defines the time-frame in which the other servers have to respond. Just leave this as it is.
"log_incidents" will log all security risks to ``/etc/dnsfallbackd/incidents.txt``. It is recommended to leave this on as every sysadmin will love you for doing this. Seriously.

### Modes
Now to the modes: 
A "mode" or userconfig will look like this:

```
{
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
```

All requests listed will be executed with ``%active_server%`` replaced with the current active server. Just ask your DNS hoster for the API specifications and do this yourself. As this part depends on every hoster, I'm not able to give further instuctions.

## Contributing
Contribution is highly appreciated as this project is in its early alpha. Just open a pull request and I'll have a look at it.

Any suggestions? Open an Issue and I'll implement your idea!

Thanks to all contributors! I love you! <3

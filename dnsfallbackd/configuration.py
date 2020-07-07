import json
import os
from dnsfallbackd.exceptions import InvalidOrNotDefinedException

# TODO: Bad practice
default_config = """{
    "servers": [ /* Servers with an dnsfallbackd installation */
        "8.8.8.8:42871",
        "1.1.1.1:42871",
        "mycdnserver.tld:42871",
        "intern.local:42871",
        "192.168.1.20:42871"
    ],
    "mode": "cloudflare", /* Name of the configuration to use in /etc/dnsfallbackd/userconfigs/ */
    "authentification_key": "mysupersecretauthetificationkey", /* The key that is used by dnsfallbackd to authentificate with other dnsfallbackd servers in your network. Keep this key private at all cost as attackers would be able to edit you dns by using this key */
    "salt": "mysupersecretsaltdontsharethisoveranunencryptedconnectionyoufuckingidiot",
    "listen_at": "0.0.0.0", /* Where dnsfallbackd will listen for other dnsfallbackd servers in your network */
    "listen_port": "42871",
    "check_interval": 10, /* Check interval in seconds. In this case dnsfallbackd will check other dnsfallbackd servers every 10 seconds */
    "check_using": "dnsfallbackd", /* Possible: ping (check server by pinging it), dnsfallbackd (uses the built in system of dnsfallbackd, recommended) */
    "check_timeout": 5, /* Check timeout in seconds */
    "log_incidents": true /* If true: loggs all incidents to /etc/dnsfallbackd/incidents.txt (recommended) */
}"""


current_configuration = None


def load_configuration(self):
    f = None
    try:
        f = open("/etc/dnsfallbackd/config.json", "r")
    except IOError:
        os.mkdir("/etc/dnsfallbackd/")
        f = open("/etc/dnsfallbackd/config.json", "w")
        f.writelines(default_config)
    self.current_configuration = json.load(f)
    self.verify_configuration()
    pass


def verify_configuration(self): # TODO: Check value types
    if self.current_configuration["servers"][0] is None:
        raise InvalidOrNotDefinedException
    if self.current_configuration["mode"] is None:
        raise InvalidOrNotDefinedException
    if self.current_configuration["identification_key"] is None:
        raise InvalidOrNotDefinedException
    if self.current_configuration["listen_at"] is None:
        raise InvalidOrNotDefinedException
    if self.current_configuration["check_interval"] is None:
        raise InvalidOrNotDefinedException
    if self.current_configuration["check_using"] is None:
        raise InvalidOrNotDefinedException
    if self.current_configuration["check_timeout"] is None:
        raise InvalidOrNotDefinedException
    if self.current_configuration["log_incidents"] is None:
        raise InvalidOrNotDefinedException
    pass

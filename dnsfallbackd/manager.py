from dnsfallbackd import communication
from dnsfallbackd import configuration
from dnsfallbackd import userconfig_processor
import socket
from _thread import start_new_thread
from time import sleep


takeover_cancel = False
taking_over = False

current_server_active_addr = None

running_announcements = 0


def takeover_dns():
    for addr in configuration.current_configuration["servers"]:
        start_new_thread(announce_takeover, (addr,))
    
    while True:
        sleep(0.01)
        if running_announcements == 0:
            break
    
    userconfig_processor.execute_userconfig(configuration.current_configuration["mode"])
    
    pass


def announce_takeover(addr):
    global running_announcements

    running_announcements += 1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((
        addr.split(":")[0],
        addr.split(":")[1]
    ))
    communication.authentificate(s)
    communication.send_encoded(s, "3||")
    s.close()
    running_announcements -= 0
    pass

from dnsfallbackd import configuration
from dnsfallbackd import manager
from dnsfallbackd import communication
from dnsfallbackd.exceptions import InvalidOrNotDefinedException
from _thread import start_new_thread
from time import sleep
import pyping


def start_check_threads():
    start_new_thread(check_server_thread, ())
    pass


def check_server_thread():
    if configuration.current_configuration["check_using"] is "ping":
        while True:
            if not check_server_using_ping(manager.current_server_active_addr):
                manager.takeover_dns()
            sleep(float(configuration.current_configuration["check_interval"]))

    elif configuration.current_configuration["check_using"] is "dnsfallbackd":
        while True:
            if not communication.ping_using_dfd(manager.current_server_active_addr):
                manager.takeover_dns()
            sleep(float(configuration.current_configuration["check_interval"]))

    else:
        raise InvalidOrNotDefinedException
    pass


def check_server_using_ping(address) -> bool:
    r = pyping.ping(str(address).split(":")[0])
    if not r.ret_code is 0:
        return False
    return True

import socket
from dnsfallbackd import configuration
from dnsfallbackd import encryption
from dnsfallbackd import incident_logger
from dnsfallbackd import manager
from _thread import start_new_thread
from time import sleep
import base64


sock = None

connected_servers = []
connected_servers_addr = []

authentificated_connections = []

_ping_response = False


def prepare_socket():
    global sock

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((
        configuration.current_configuration["listen_at"],
        configuration.current_configuration["listen_port"]
    ))
    sock.listen()
    start_new_thread(listen_to_connections, ())
    pass


def listen_to_connections():
    global sock
    global connected_servers
    global connected_servers_addr

    while True:
        conn = None
        addr = None
        conn, addr = sock.accept()
        connected_servers.append(conn)
        connected_servers_addr.append(addr)
        start_new_thread(listen_to_commands, (conn, addr))
    pass


def listen_to_commands(conn, addr):
    global connected_servers
    global connected_servers_addr
    global authentificated_connections

    # Yes, I know that this protocol is something like a war crime... 
    # But considering that noone needs to understand this anyways, 
    # I don't think that this is a problem at all.
    # If you want to "fix it" or whatever, feel free to create a fork and
    # build you own - better - protocol. Most likely I'll use yours since 
    # CSV is total bullshit for communicating betweet computers as
    # there are much better solutions such as JSON...
    # When I started developing this piece of art it was really late and
    # I was really not thinking about it... 
    # Trust me, don't develop after 1am...
    #
    # hours_wasted_on_this_spaghetti = 8
    # (feel free to increase)


    # =============================================================
    # THE TBFP - Total brainf#ck protocol
    #   Unencoded example: <tlc>||<arg>||<arg>||...
    #
    #   tlc - top level command (or command indicator) [int]
    #   arg - argument [string]
    #   ||  - argument devider (or delimiter)
    #
    #   Everything will be encoded in Base64 which looks like this:
    #       OTl8fHlvdXJzdXBlcnNlY3JldGhhc2hlZGF1dGhrZXk
    #   Or for humans:
    #       99||yoursupersecrethashedauthkey
    # =============================================================

    while True:
        try:
            message = conn.recv(2048)
            if message:
                msg = base64.b64decode(str(message)).split("||")
                tlc = int(msg[0]) # Top level command
                del msg[0] # Choppin da list
                args = msg # Arguments

                if tlc is 0: # Ping
                    if conn in authentificated_connections:
                        send_encoded(conn, "1||")
                    else:
                        incident_logger.log_incident(f"{ addr } tried to run command { tlc } without identification! This could be an attack!")

                elif tlc is 1: # Ping response
                    if conn in authentificated_connections:
                        _ping_response = True
                    else:
                        incident_logger.log_incident(f"{ addr } tried to run command { tlc } without identification! This could be an attack!")

                elif tlc is 3: # Active server (takeover from other -> stop operation)
                    if conn in authentificated_connections:
                        manager.current_server_active_addr = addr
                    else:
                        incident_logger.log_incident(f"{ addr } tried to run command { tlc } without identification! This could be an attack!")

                elif tlc is 99: # Incoming Authentification (99||hash)
                    if encryption.check_key(args[0], configuration.current_configuration["authentification_key"]):
                        authentificated_connections += conn
                    else:
                        incident_logger.log_incident(f"{ addr } failed to authentificate with dnsfallbackd but failed! This could be an attack!")

                else:
                    pass
                
            else:
                if conn in connected_servers:
                    i = connected_servers.index(conn)
                    del connected_servers[i]
                    del connected_servers_addr[i]
                    authentificated_connections.remove(conn)
                    conn.close()
                    return
        except:
            pass
    pass
    

def send_encoded(conn, msg):
    enc = base64.b64encode(msg)
    conn.send(str(enc))
    pass


def broadcast_command(command):
    global connected_servers
    global connected_servers_addr
    global authentificated_connections

    for conn in connected_servers:
        try:
            conn.send(command)
        except:
            if conn in connected_servers:
                i = connected_servers.index(conn)
                del connected_servers[i]
                del connected_servers_addr[i]
                authentificated_connections.remove(conn)
                conn.close()
    pass


def ping_using_dfd(address, port) -> bool:
    _ping_response = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, port))
    authentificate(s)
    send_encoded(s, "0||")

    slept = 0.0

    while True:
        if slept >= configuration.current_configuration["check_timeout"]:
            s.close()
            return False

        if _ping_response:
            s.close()
            return True        

        sleep(0.01)
        slept += 0.01
    pass


def authentificate(conn):
    h_key = encryption.hash_key(configuration.current_configuration["authentification_key"])
    send_encoded(conn, "99||" + h_key + "||")
    pass

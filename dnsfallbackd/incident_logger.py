from dnsfallbackd import configuration
import os
import datetime


incident_file = None


def prepare_incident_logger():
    global incident_file

    if configuration.current_configuration["log_incidents"]:
        try:
            incident_file = open("/etc/dnsfallbackd/incidents.txt", "a")
        except:
            os.mkdir("/etc/dnsfallback/")
            incident_file = open("/etc/dnsfallbackd/incidents.txt", "a")

        incident_file.write(f"\n ---- Incidets starting from the { datetime.datetime.now() } ---- \n")
    pass


def log_incident(msg):
    global incident_file

    
    print(f"INCIDENT:  { msg }")

    if configuration.current_configuration["log_incidents"]:
        incident_file.write(str(msg) + "\n")
        incident_file.flush()
    pass

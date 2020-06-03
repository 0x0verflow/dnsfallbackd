from dnsfallbackd import configuration
from dnsfallbackd import communication
from dnsfallbackd import incident_logger
from dnsfallbackd import userconfig_processor


if __name__ == "__main__":
    print("Loading configuration...")
    configuration.load_configuration()
    configuration.verify_configuration()

    print(f"Starting dnsfallbackd using mode '{ str(configuration.current_configuration['mode']) }'...")
    incident_logger.prepare_incident_logger()
    userconfig_processor.prepare_userconfig()
    communication.prepare_socket()

    exit(0)

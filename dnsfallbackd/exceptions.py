class InvalidOrNotDefinedException(Exception):
    print("Error: Value in configuration is invalid or not defined")
    exit(1)
    pass


class InvalidRequestConfigurationException(Exception):
    print("Error: Request configuration seems to be invalid")
    exit(1)
    pass

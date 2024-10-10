from config.config import Config

DEBUG = Config.DEBUG == "true"


# Function to log to terminal only if DEBUG is true
def logfn(message, *args):
    if DEBUG:
        if args:
            print(message, *args)
        else:
            print(message)

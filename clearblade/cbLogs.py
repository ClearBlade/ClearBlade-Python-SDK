from __future__ import print_function, absolute_import
# set these variables to false to disable the logs
# (import cbLogs to your project and set it from there)
import logging


DEBUG = True
MQTT_DEBUG = True
USE_LOGGING = False  # default to false to preserve existing behavior
LEVEL_TO_LOG_LEVEL = {
    1: logging.INFO,
    2: logging.INFO,   # NOTE: no equivelent to "notice"
    4: logging.WARNING,
    8: logging.ERROR,
    16: logging.DEBUG,
}


cb_logger = logging.getLogger("CB")


class prettyText:
    bold = '\033[1m'
    faded = '\033[2m'
    italics = '\033[3m'
    underline = '\033[4m'
    red = '\033[91m'
    yellow = '\033[33m'
    green = '\033[92m'
    blue = '\033[94m'
    purple = '\033[95m'
    cyan = '\033[96m'
    endColor = '\033[0m'


def error(*args):
    # Errors should always be shown
    if USE_LOGGING:
        cb_logger.error(" ".join(args))
    else:
        print(prettyText.bold + prettyText.red + "CB Error:" + prettyText.endColor, " ".join(args))


def warn(*args):
    # Warnings should always be shown
    if USE_LOGGING:
        cb_logger.warning(" ".join(args))
    else:
        print(prettyText.bold + prettyText.yellow + "CB Warning: " + prettyText.endColor, " ".join(args))


def info(*args):
    if DEBUG:  # extra info should not always be shown
        if USE_LOGGING:
            cb_logger.debug(" ".join(args))
        else:
            print(prettyText.bold + prettyText.blue + "CB Info:" + prettyText.endColor, " ".join(args))


def mqtt(level, data):
    if MQTT_DEBUG:
        if USE_LOGGING:
            mqtt_logger = logging.getLogger("Mqtt")
            mqtt_logger.log(LEVEL_TO_LOG_LEVEL.get(level, logging.INFO), data)
        else:
            if level == 1:
                print(prettyText.bold + prettyText.cyan + "Mqtt Info:" + prettyText.endColor, data)
            elif level == 2:
                print(prettyText.bold + prettyText.green + "Mqtt Notice:" + prettyText.endColor, data)
            elif level == 4:
                print(prettyText.bold + prettyText.yellow + "Mqtt Warning:" + prettyText.endColor, data)
            elif level == 8:
                print(prettyText.bold + prettyText.red + "Mqtt Error:" + prettyText.endColor, data)
            elif level == 16:
                print(prettyText.bold + prettyText.purple + "Mqtt Debug:" + prettyText.endColor, data)

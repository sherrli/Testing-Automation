# A file containing various methods used to write to a log file.
# Import this file and call these functions from your automated test file to generate logs.

import logging

def logSetupError(browser):
    logging.error("Unable to load " + browser)

def logSiteNotFound(site):
    logging.error("Could not find " + site)

def logHttpError(site, status):
    # cast the status code to a string type if it's not already
    logging.error(site + " returned status code " + str(status))

def logTimeout(site, minutes):
    logging.error(site + " took over " + str(minutes) + " minutes to load")


def logStart(site):
    logging.info("\nBrowser testing started for " + site)

def logButtonMissing(site, button):
    logging.error(button + " not found on " + site)

def logErrorMsg(site, msg):
    logging.error(msg + " on " + site)

def logInfoMsg(site, msg):
    logging.info(msg + " for " + site)


def logSuccess(site, testType):
    logging.info("Passed {} test for {}\n".format(testType, site))

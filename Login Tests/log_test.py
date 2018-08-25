# A file containing various methods used to write to a log file.
# Import this file in your other tests when you want to generate logs.

import logging

def logSetupError(browser):
    logging.error("Unable to load " + browser)

def logSiteNotFound(site):
    logging.error("Could not find " + site)

def logHttpError(site, status):
    logging.error(site + " returned status code " + status)

def logTimeout(site):
    logging.error(site + " took over 3 minutes to load")


def logStart(site):
    logging.info("Browser testing started for {}".format(site))

def logButtonMissing(button, site):
    logging.error(button + " not found on " + site)


def logSuccess(site):
    logging.info("Passed " + site)

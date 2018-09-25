# A file containing various methods used to write to a log file.
# Import this file and call these functions from your automated test file to generate logs.

import logging

# Call logSetupError if a test's setupBrowser() method fails
def logSetupError(browser):
    logging.error(" Unable to load " + browser)

# Call logSiteNotFound if the lastpass site wasn't found or was mapped incorrectly
def logSiteNotFound(site):
    logging.error(" Could not find " + site)

# Call logHttpError if python requests.get() returns non-200/301/302 status code and webdriver test never begins
def logHttpError(site, status):
    # cast the status code to a string type if it's not already
    logging.error(" " + site + " returned status code " + str(status))

# Call logTimeout if python times out while trying to get site's status code
def logTimeout(site, minutes):
    logging.error(" " + site + " took over " + str(minutes) + " minutes to load")

# Call logStart right after the browser opens & real test begins
def logStart(site):
    logging.info(" Browser testing started for " + site)

def logButtonMissing(site, button):
    logging.error(" " + button + " not found on " + site)

def logErrorMsg(site, msg):
    logging.error(" " + msg + " on " + site)

def logInfoMsg(site, msg):
    logging.info(" " + msg + " on " + site)

def logElapsedTime(time, units):
    # convert the time (float) into a string
    logging.info(" completed in " + str(time) + " " + units)

# Call logSuccess at end of test
def logSuccess(site, testType):
    logging.info(" SUCCESS: {} test for {}".format(testType, site))

def logSummary(testName, time):
    logging.info("\n\nSUMMARY\n"+testName+" test took "+str(time)+" seconds\n\n\n")


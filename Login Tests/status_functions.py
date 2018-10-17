# A file containing a method used to get the http response code of a site.
# Pre-requisite: You must have the requests module installed.
# $ pip3 install requests

import requests
import write_log

ERRORCOLOR = "\u001b[31m" #red
WARNINGCOLOR = "\u001b[33m" #yellow
SUCCESSCOLOR = "\u001b[32m" #green
DEFAULTCOLOR = "\u001b[0m" #white


# You can also make acceptableStatusCodes a global variable in this file.
# For now, we let it be a parameter that the calling function can change.


# checkStatus is an improved function that includes logging for the calling function.
# Input url is a string, acceptableStatusCodes is a list of integers
def checkStatus(url, acceptableStatusCodes):
    try:
        # Time out after 2 minutes
        r = requests.get(url, timeout=121)
        if r.status_code not in acceptableStatusCodes:
            write_log.logHttpError(url, r.status_code)
            print(ERRORCOLOR+"ERROR: "+url+" returns status code "+str(r.status_code)+DEFAULTCOLOR)
            return False
        else:
            write_log.logInfoMsg(url, "status code "+str(r.status_code))
            print(SUCCESSCOLOR+"ok: "+url+" returns status code "+str(r.status_code)+DEFAULTCOLOR)
            return True
    except Exception as e:
        # Unable to get the status code due to a syntax or a connection error
        # print(e)
        write_log.logTimeout(url, 2)
        # repr() casts e to a string and includes the error type
        write_log.logErrorMsg(url, repr(e))
        print(ERRORCOLOR+"ERROR: "+url+" took over 2 minutes to load, see log file for detailed error"+DEFAULTCOLOR)
        return False # requests.get() function timed out
    

# get_status is an older function
# Return True means the site returns 200 or a redirect
# Return False means site timed out
# Return type int means site has unacceptable status code
def get_status(site):
    try:
        # time out after 2 minutes
        r = requests.get(site, timeout=121)
        if r.status_code!=200 and r.status_code!=301 and r.status_code!=302:
            print("ERROR: status code " + r.status_code + " for " + site)
            return r.status_code
        return True # site returns good status code and we can proceed with the webdriver test
    except:
        print("ERROR: unable to reach " + site)
        return False # requests.get() function never worked

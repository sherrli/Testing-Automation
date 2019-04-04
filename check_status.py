# File name: check_status.py
# Pre-condition: python3 requests library is installed
# $ pip3 install requests

# This file contains function checkStatus to ensure status code of a site is acceptable.
# Calling functions must import check_status to use the function.

import requests
import write_log

ERRORCOLOR = "\u001b[31m" #red
WARNINGCOLOR = "\u001b[33m" #yellow
SUCCESSCOLOR = "\u001b[32m" #green
DEFAULTCOLOR = "\u001b[0m" #white


# You can also make acceptableStatusCodes a global variable in this file.
# For now, we let it be a parameter that the calling function can change.

# url: string
# acceptableStatusCodes: list of integers
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

# A file containing a method used to get the http response code of a site.
# Pre-requisite: You must have the requests module installed.
# $ pip3 install requests

import requests

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

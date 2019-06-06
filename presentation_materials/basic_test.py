#basic validation tests to be run against all sites

import timeit
from datetime import datetime


def basic_test (firefox_driver, results_sheet, current_site_url,site_no):

    result = 0

    results_sheet.update_cell(site_no, 1, str(datetime.now()))
    results_sheet.update_cell(site_no, 2, current_site_url)
    start_time = timeit.default_timer()

    try:
        #load the site!
        firefox_driver.get(current_site_url)
        elapsed = timeit.default_timer() - start_time

        # to-do ... get the cert expiration date?

        # log results to Google sheet
        results_sheet.update_cell(site_no, 3, firefox_driver.title)
        results_sheet.update_cell(site_no, 4, elapsed)

    except:

        result = -1
        results_sheet.update_cell(site_no, 3, 'failed')



    return result
from selenium import webdriver
import time

# Make the site you want to test a variable that you can change later.
site = "https://admstats.sa-dev.ucsc.edu/"
text = "UCSC Undergraduate Admissions Statistics"

try:
    # Use selenium to open the chrome webdriver.
    browser = webdriver.Chrome()
    browser.implicitly_wait(30)

    browser.get(site)
    print("Testing " + site + " with " + browser.name)

    # Make sure desired text appears after your site loads.
    if text not in browser.page_source:
        print("ERROR: '" + text + "' not found")

    assert(text in browser.page_source)

    print("Passed: title test")

except Exception as e:
    print(e)
    raise(e)

finally:
    time.sleep(3)
    browser.close()

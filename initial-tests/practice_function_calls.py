# This is a practice test to see how http response codes work.
# Pre-requisite: chromedriver.exe is in your PATH.

import requests
from selenium import webdriver

def test1():
    try:
        site = 'https://fixit.sa-dev.ucsc.edu'
        print("test 1: "+site)
        r = requests.get(site)
        print(r.status_code)
        print(r)
    # Make sure that the http response is 200 before opening chromedriver
        if r.status_code != 200:
            print(u"\u001b[31mERROR:\u001b[0m Status code " + r.status_code)
        assert(r.status_code==200)
        driver = webdriver.Chrome()
        driver.implicitly_wait(30)
        driver.get(site)
        print(driver.title)
        driver.quit()
    except:
        print(e)
        raise e

def test2():
    try:
        site = 'https://fixit.sa-dev-new.ucsc.edu'
        print("test 2: "+site)
        r = requests.get(site)
        print(r.status_code)
        print(r)
        if r.status_code != 200:
            print(u"\u001b[31mERROR:\u001b[0m Status code " + r.status_code)
        assert(r.status_code==200)
        driver = webdriver.Chrome()
        driver.implicitly_wait(30)
        driver.get(site)
        print(driver.title)
        driver.quit()
    except:
        print(e)
        raise e

# synchronously call the two tests
def test3():
    print("running test 1")
    test1()
    print("running test 2")
    test2()
    print("done")

# main()
test3()

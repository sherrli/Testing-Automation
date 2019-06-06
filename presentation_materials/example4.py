from selenium import webdriver
import time

# Make the site you want to test a variable that you can change later.
site = "https://www.careercenter-dev.ucsc.edu/ers/ersStaff/login/index.cfm"
text = "Work-study Information"

try:
    # Use selenium to open the chrome webdriver.
    browser = webdriver.Chrome()
    browser.implicitly_wait(30)

    browser.get(site)
    print("Testing " + site + " with " + browser.name)

    usernameBox = None
    passwordBox = None

    try:
        usernameBox = browser.find_element_by_name('logon')
    except:
        print("username field missing")
        #return
    try:
        passwordBox = browser.find_element_by_name('pass')
    except:
        print("password field missing")
        #return

    usernameBox.clear()
    usernameBox.send_keys('ServiceCenter')
    passwordBox.clear()
    passwordBox.send_keys('23#Cheese')
    passwordBox.send_keys(Keys.ENTER)

    browser.implicitly_wait(10)

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

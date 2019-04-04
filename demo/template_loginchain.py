# Another way to log in after locating the username box.
# 1. Grab the first input field element.
# 2. Input the username.
# 3. Tab over to the next box, which tends to be the password box.
# 4. Input the password.
# 5. Click "enter" which tends to submit the form.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def login(driver, username, password):
    usernameBox = driver.find_element_by_xpath('//input[@type="text"]')
    usernameBox.clear()
    usernameBox.send_keys(username)
    action = ActionChains(driver).move_to_element(usernameBox).click().send_keys(Keys.TAB).send_keys(password).send_keys(Keys.ENTER)
    action.perform()
    return driver

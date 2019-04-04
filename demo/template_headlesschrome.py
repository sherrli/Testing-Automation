# Sherri's practice headless chrome browser test.
# Requires chrome browser v59+, chromedriver version 2.38+, python3 virtualenv.
# Takes a screenshot of a google search on "cheese", saved as templatetest.png


import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# For testing, you can ask the user if they want to run in headless.
chrome_options = Options()
chrome_options.add_argument("--headless")

#driver = webdriver.Chrome(executable_path=os.path.abspath("/usr/local/bin/chromedriver"), chrome_options=chrome_options)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://www.google.com")

try:
    magnifying_glass = driver.find_element_by_name("q")
    magnifying_glass.clear()
    magnifying_glass.send_keys("cheese")
except:
    print("can't find search bar")

#search_result = driver.find_element_by_link_text("Images").click()
#driver.save_screenshot('templatetest.png')
driver.close()

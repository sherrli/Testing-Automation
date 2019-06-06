# Import selenium's webdriver library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# Create a ChromeDriver instance
driver = webdriver.Chrome()

# Wait up to 30 seconds for the browser to load
driver.implicitly_wait(30)

# Open google home page
driver.get("https://www.google.com")

# Locate the search bar
driver.find_element_by_name("q").clear()

# Search for 'cheese'
driver.find_element_by_name("q").send_keys("cheese")
driver.find_element_by_name("q").send_keys(Keys.ENTER)

# Click the 'images' tab
driver.find_element_by_link_text("Images").click()

# Take a screenshot
driver.save_screenshot('exampleCheese.png')

driver.quit()

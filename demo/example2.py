# Import selenium's webdriver library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Import python's unittest library
import unittest

class exampleTest(unittest.TestCase):

    def setUp(self):
        # Create a ChromeDriver instance
        self.driver = webdriver.Chrome()
        # Wait up to 30 seconds for the browser to load
        self.driver.implicitly_wait(30)


    def test_websearch(self):

        # Open google home page
        self.driver.get("https://www.google.com")

        # Locate the search bar
        self.driver.find_element_by_name("q").clear()

        # Search for 'cheese'
        self.driver.find_element_by_name("q").send_keys("cheese")
        self.driver.find_element_by_name("q").send_keys(Keys.ENTER)

        # Click the 'images' tab
        self.driver.find_element_by_link_text("Images").click()

        # Take a screenshot
        self.driver.save_screenshot('exampleCheese.png')


    def tearDown(self):
        self.driver.quit()


# Run the test
if __name__ == "__main__":
    unittest.main()

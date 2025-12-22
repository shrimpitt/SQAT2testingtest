import os
import unittest
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchTestWikipedia(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.maximize_window()

    def test_search_wikipedia(self):
        driver = self.driver
        driver.get(os.getenv("BASE_URL1"))

        # CSS selector: field by ID
        search_input = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input#searchInput"))
        )
        search_input.clear()
        search_input.send_keys("Selenium" + Keys.ENTER)

        # XPath: heading must contain Selenium
        heading = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h1[contains(., 'Selenium')]"))
        )

        self.assertIn("Selenium", heading.text)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

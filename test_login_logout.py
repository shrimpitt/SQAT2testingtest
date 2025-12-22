import os
import unittest
import time
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginLogoutTest(unittest.TestCase):
    def setUp(self):
        load_dotenv(override=True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.maximize_window()

    def test_login_logout(self):
        driver = self.driver
        wait = self.wait

        base_url = os.getenv("BASE_URL2", "").strip()
        username = os.getenv("USERNAME", "").strip()
        password = os.getenv("PASSWORD", "").strip()

        self.assertTrue(base_url and username and password, "Check .env variables")

        driver.get(base_url)

        wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(username)
        wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(password)

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

        flash_text = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
        self.assertIn("You logged into a secure area!", flash_text)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/logout']"))).click()
        flash2 = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
        self.assertIn("You logged out of the secure area!", flash2)

        time.sleep(2)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

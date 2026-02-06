from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class SearchResultsPage(BasePage):
    """Page object for Aviasales search results page"""

    # Locators
    FIRST_PRICE_SELECTOR = "div[data-test-id='price']"
    BUY_BUTTON_XPATHS = [
        "//button[contains(.,'Купить')]",
        "//button[contains(.,'Buy')]",
        "(//button[contains(@class,'button')])[1]"
    ]

    def __init__(self, driver, wait_timeout=25):
        super().__init__(driver, wait_timeout)

    def open_search_url(self, url):
        """Open the search results URL"""
        self.driver.get(url)
        self.wait_for_page_load()

    def verify_page_loaded(self):
        """Verify that the page has loaded by checking title"""
        title = self.get_page_title()
        assert title.strip() != "", "Page title is empty"
        return title

    def wait_for_captcha(self, wait_seconds=30):
        """Wait for manual captcha solving"""
        print(f"ACTION REQUIRED: Solve captcha manually if it appears ({wait_seconds} sec)")
        time.sleep(wait_seconds)

    def select_first_ticket(self):
        """Select the first available ticket by clicking on its price"""
        first_price = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.FIRST_PRICE_SELECTOR))
        )
        self._safe_click(first_price)
        print("Checkpoint 2: First ticket price clicked")

    def click_buy_button(self):
        """Click the buy button and return the original window handle"""
        buy_button = None
        for xpath in self.BUY_BUTTON_XPATHS:
            try:
                buy_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                break
            except Exception:
                continue

        if buy_button is None:
            raise Exception("Buy button not found")

        original_window = self.driver.current_window_handle
        self._safe_click(buy_button)
        print("Checkpoint 3: Buy button clicked")
        return original_window

    def switch_to_partner_window(self, original_window, timeout=15):
        """Switch to the partner booking window"""
        WebDriverWait(self.driver, timeout).until(EC.number_of_windows_to_be(2))
        for handle in self.driver.window_handles:
            if handle != original_window:
                self.driver.switch_to.window(handle)
                break
        self.wait_for_page_load()
        print("Checkpoint 4: Partner page opened ->", self.get_page_title())


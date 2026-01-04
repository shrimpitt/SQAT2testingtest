from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class AviasalesPage(BasePage):
    """Page object for Aviasales search results page"""

    # Locators
    FIRST_PRICE = (By.CSS_SELECTOR, "div[data-test-id='price']")
    BUY_BUTTON_XPATHS = [
        "//button[contains(.,'Купить')]",
        "//button[contains(.,'Buy')]",
        "(//button[contains(@class,'button')])[1]"
    ]

    def __init__(self, driver, wait=None):
        super().__init__(driver, wait)

    def open_search_results(self, origin, destination, date):
        """
        Open search results page
        
        Args:
            origin: Origin airport code (e.g., 'GUW')
            destination: Destination airport code (e.g., 'ALA')
            date: Date in format DDMM (e.g., '2502' for Feb 25)
        """
        url = f"https://www.aviasales.kz/search/{origin}{date}{destination}1"
        self.driver.get(url)
        self.wait_for_page_load()

    def select_first_ticket(self):
        """Click on the first ticket price"""
        first_price = self.wait.until(
            EC.element_to_be_clickable(self.FIRST_PRICE)
        )
        self.safe_click(first_price)

    def click_buy_button(self):
        """Click the buy button and return original window handle"""
        original_window = self.driver.current_window_handle
        
        buy_button = None
        for xpath in self.BUY_BUTTON_XPATHS:
            try:
                buy_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                break
            except Exception:
                continue

        if buy_button is None:
            raise Exception("Buy button not found")

        self.safe_click(buy_button)
        return original_window

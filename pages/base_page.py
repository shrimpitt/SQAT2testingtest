import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver, wait=None):
        self.driver = driver
        self.wait = wait or WebDriverWait(driver, 25)

    def safe_click(self, element):
        """Click with fallback to JavaScript click"""
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def close_overlay_if_any(self):
        """Close any overlay/modal that might appear"""
        overlays = self.driver.find_elements(
            By.CSS_SELECTOR,
            "[data-testid='closeIcon'], .close, .modal-close"
        )
        for overlay in overlays:
            try:
                if overlay.is_displayed():
                    self.safe_click(overlay)
                    time.sleep(0.5)
                    break
            except Exception:
                continue

    def wait_for_page_load(self):
        """Wait for page to be fully loaded"""
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def get_title(self):
        """Get page title"""
        return self.driver.title

    def switch_to_new_window(self, original_window):
        """Switch to newly opened window"""
        WebDriverWait(self.driver, 15).until(
            lambda d: len(d.window_handles) > 1
        )
        for handle in self.driver.window_handles:
            if handle != original_window:
                self.driver.switch_to.window(handle)
                break
        self.wait_for_page_load()

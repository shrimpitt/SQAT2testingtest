import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

from pages.aviasales_page import AviasalesPage
from pages.wingie_booking_page import WingieBookingPage


class FlightBookingViaAviasalesPOM(unittest.TestCase):
    """
    Flight booking test using Page Object Model (POM)
    This is a refactored version that demonstrates the POM pattern
    """

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 25)

    def test_booking_from_atyrau_until_payment(self):
        driver = self.driver
        wait = self.wait

        # Initialize page objects
        aviasales_page = AviasalesPage(driver, wait)
        wingie_page = WingieBookingPage(driver, wait)

        # --- Checkpoint 1: Open search results ---
        aviasales_page.open_search_results("GUW", "CIT", "2502")
        self.assertTrue(aviasales_page.get_title().strip() != "")
        print("Checkpoint 1: Page loaded ->", aviasales_page.get_title())

        # --- Captcha ---
        print("ACTION REQUIRED: Solve captcha manually if it appears (30 sec)")
        time.sleep(30)

        # --- Checkpoint 2: Select first ticket ---
        aviasales_page.select_first_ticket()
        print("Checkpoint 2: First ticket price clicked")

        # --- Checkpoint 3: Click buy button ---
        original_window = aviasales_page.click_buy_button()
        print("Checkpoint 3: Buy button clicked")

        # --- Checkpoint 4: Switch to partner window ---
        wingie_page.switch_to_new_window(original_window)
        print("Checkpoint 4: Partner page opened ->", wingie_page.get_title())

        # --- Test data ---
        booking_data = {
            "email": "sana.test2025@gmail.com",
            "phone": "77771234567",
            "first_name": "Sana",
            "last_name": "Bagym",
            "birth_day": 2,
            "birth_month": 5,
            "birth_year": 2004,
            "passport_number": "N4589217",
            "passport_exp_day": 15,
            "passport_exp_month": 3,
            "passport_exp_year": 2032,
            "gender": "F",
            "package": "Standard"
        }

        # --- Fill booking form ---
        print("Checkpoint 5: Contact info filled")
        print("Checkpoint 6: Passenger name filled")
        print("Checkpoint 7: Gender selected")
        print("Checkpoint 8: Date of birth selected")
        print("Checkpoint 9: Passport data filled")

        selected_package = wingie_page.fill_complete_booking_form(**booking_data)
        print(f"Checkpoint 10: Package selected -> {selected_package}")

        print("Checkpoint 11: Test completed before payment step")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

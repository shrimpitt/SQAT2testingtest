import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class FlightBookingViaAviasales(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 25)

    # ---------------- helpers ----------------

    def _safe_click(self, el):
        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)

    def _close_overlay_if_any(self):
        driver = self.driver
        overlays = driver.find_elements(
            By.CSS_SELECTOR,
            "[data-testid='closeIcon'], .close, .modal-close"
        )
        for o in overlays:
            try:
                if o.is_displayed():
                    self._safe_click(o)
                    time.sleep(0.5)
                    break
            except Exception:
                continue

    # ---------------- test ----------------

    def test_booking_from_atyrau_until_payment(self):
        driver = self.driver
        wait = self.wait

        # 🔹 Атырау (GUW) → Алматы (ALA), 25 февраля
        url = "https://www.aviasales.kz/search/GUW2502ALA1"
        driver.get(url)

        # --- Checkpoint 1 ---
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        self.assertTrue(driver.title.strip() != "")
        print("Checkpoint 1: Page loaded ->", driver.title)

        # --- Captcha ---
        print("ACTION REQUIRED: Solve captcha manually if it appears (30 sec)")
        time.sleep(30)

        # --- Select first ticket ---
        first_price = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-test-id='price']"))
        )
        self._safe_click(first_price)
        print("Checkpoint 2: First ticket price clicked")

        # --- Buy button ---
        buy_button = None
        for xp in [
            "//button[contains(.,'Купить')]",
            "//button[contains(.,'Buy')]",
            "(//button[contains(@class,'button')])[1]"
        ]:
            try:
                buy_button = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
                break
            except Exception:
                continue

        if buy_button is None:
            self.fail("Buy button not found")

        original_window = driver.current_window_handle
        self._safe_click(buy_button)
        print("Checkpoint 3: Buy button clicked")

        # --- Switch to partner (Wingie) ---
        WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(2))
        for h in driver.window_handles:
            if h != original_window:
                driver.switch_to.window(h)
                break

        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        print("Checkpoint 4: Partner page opened ->", driver.title)

        # ---------------- Test data ----------------

        email = "sana.test2025@gmail.com"
        phone = "77771234567"

        first_name = "Sana"
        last_name = "Bagym"

        birth_day = 2
        birth_month = 5
        birth_year = 2004

        passport_number = "N4589217"
        passport_exp_day = 15
        passport_exp_month = 3
        passport_exp_year = 2032

        # --- Close overlays ---
        self._close_overlay_if_any()

        # --- Contact info ---
        email_input = wait.until(EC.presence_of_element_located((By.ID, "contact_email")))
        email_input.clear()
        email_input.send_keys(email)

        phone_input = driver.find_element(By.ID, "contact_cellphone")
        phone_input.clear()
        phone_input.send_keys(phone)

        print("Checkpoint 5: Contact info filled")

        # --- Passenger info ---
        fn_input = driver.find_element(By.ID, "firstName_0")
        fn_input.clear()
        fn_input.send_keys(first_name)

        ln_input = driver.find_element(By.ID, "lastName_0")
        ln_input.clear()
        ln_input.send_keys(last_name)

        print("Checkpoint 6: Passenger name filled")

        # --- Gender (Female) ---
        try:
            female = driver.find_element(By.ID, "gender_F_0")
            self._safe_click(female)
        except Exception:
            male = driver.find_element(By.ID, "gender_M_0")
            self._safe_click(male)

        print("Checkpoint 7: Gender selected")

        # --- Date of birth ---
        Select(driver.find_element(By.ID, "birthDateDay_0")).select_by_value(f"{birth_day:02d}")
        Select(driver.find_element(By.ID, "birthDateMonth_0")).select_by_value(f"{birth_month:02d}")
        Select(driver.find_element(By.ID, "birthDateYear_0")).select_by_value(str(birth_year))

        print("Checkpoint 8: Date of birth selected")

        # --- Passport ---
        pass_input = driver.find_element(By.ID, "passportNoAll_0")
        pass_input.clear()
        pass_input.send_keys(passport_number)

        Select(driver.find_element(By.ID, "passportDay_0")).select_by_value(f"{passport_exp_day:02d}")
        Select(driver.find_element(By.ID, "passportMonth_0")).select_by_value(f"{passport_exp_month:02d}")
        Select(driver.find_element(By.ID, "passportYear_0")).select_by_value(str(passport_exp_year))

        print("Checkpoint 9: Passport data filled")

        # --- Package selection ---
        for pack in ["Standard", "Comfort", "Basic"]:
            try:
                pack_el = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        f"//div[contains(@class,'provider-package__select') and .//p[normalize-space()='{pack}']]"
                    ))
                )
                self._safe_click(pack_el)
                print(f"Checkpoint 10: Package selected -> {pack}")
                break
            except Exception:
                continue

        time.sleep(8)
        print("Checkpoint 11: Test completed before payment step")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from pages.base_page import BasePage
import time


class BookingFormPage(BasePage):
    """Page object for partner booking form (Wingie)"""

    # Locators
    CONTACT_EMAIL_ID = "contact_email"
    CONTACT_PHONE_ID = "contact_cellphone"
    FIRST_NAME_ID = "firstName_0"
    LAST_NAME_ID = "lastName_0"
    GENDER_FEMALE_ID = "gender_F_0"
    GENDER_MALE_ID = "gender_M_0"
    BIRTH_DAY_ID = "birthDateDay_0"
    BIRTH_MONTH_ID = "birthDateMonth_0"
    BIRTH_YEAR_ID = "birthDateYear_0"
    PASSPORT_NUMBER_ID = "passportNoAll_0"
    PASSPORT_DAY_ID = "passportDay_0"
    PASSPORT_MONTH_ID = "passportMonth_0"
    PASSPORT_YEAR_ID = "passportYear_0"
    PACKAGE_XPATH_TEMPLATE = "//div[contains(@class,'provider-package__select') and .//p[normalize-space()='{package}']]"

    def __init__(self, driver, wait_timeout=25):
        super().__init__(driver, wait_timeout)

    def fill_contact_info(self, email, phone):
        """Fill contact email and phone number"""
        self._close_overlay_if_any()

        email_input = self.wait.until(EC.presence_of_element_located((By.ID, self.CONTACT_EMAIL_ID)))
        email_input.clear()
        email_input.send_keys(email)

        phone_input = self.driver.find_element(By.ID, self.CONTACT_PHONE_ID)
        phone_input.clear()
        phone_input.send_keys(phone)

        print("Checkpoint 5: Contact info filled")

    def fill_passenger_name(self, first_name, last_name):
        """Fill passenger first and last name"""
        fn_input = self.driver.find_element(By.ID, self.FIRST_NAME_ID)
        fn_input.clear()
        fn_input.send_keys(first_name)

        ln_input = self.driver.find_element(By.ID, self.LAST_NAME_ID)
        ln_input.clear()
        ln_input.send_keys(last_name)

        print("Checkpoint 6: Passenger name filled")

    def select_gender(self, prefer_female=True):
        """Select gender (prefer female, fallback to male if not available)"""
        try:
            if prefer_female:
                female = self.driver.find_element(By.ID, self.GENDER_FEMALE_ID)
                self._safe_click(female)
            else:
                male = self.driver.find_element(By.ID, self.GENDER_MALE_ID)
                self._safe_click(male)
        except Exception:
            # Fallback to the other option
            if prefer_female:
                male = self.driver.find_element(By.ID, self.GENDER_MALE_ID)
                self._safe_click(male)
            else:
                female = self.driver.find_element(By.ID, self.GENDER_FEMALE_ID)
                self._safe_click(female)

        print("Checkpoint 7: Gender selected")

    def fill_date_of_birth(self, day, month, year):
        """Fill date of birth using dropdown selects"""
        Select(self.driver.find_element(By.ID, self.BIRTH_DAY_ID)).select_by_value(f"{day:02d}")
        Select(self.driver.find_element(By.ID, self.BIRTH_MONTH_ID)).select_by_value(f"{month:02d}")
        Select(self.driver.find_element(By.ID, self.BIRTH_YEAR_ID)).select_by_value(str(year))

        print("Checkpoint 8: Date of birth selected")

    def fill_passport_info(self, passport_number, exp_day, exp_month, exp_year):
        """Fill passport number and expiration date"""
        pass_input = self.driver.find_element(By.ID, self.PASSPORT_NUMBER_ID)
        pass_input.clear()
        pass_input.send_keys(passport_number)

        Select(self.driver.find_element(By.ID, self.PASSPORT_DAY_ID)).select_by_value(f"{exp_day:02d}")
        Select(self.driver.find_element(By.ID, self.PASSPORT_MONTH_ID)).select_by_value(f"{exp_month:02d}")
        Select(self.driver.find_element(By.ID, self.PASSPORT_YEAR_ID)).select_by_value(str(exp_year))

        print("Checkpoint 9: Passport data filled")

    def select_package(self, preferred_packages=None, wait_after=8):
        """Select a package from the available options"""
        if preferred_packages is None:
            preferred_packages = ["Standard", "Comfort", "Basic"]

        for package in preferred_packages:
            try:
                pack_el = WebDriverWait(self.driver, 8).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        self.PACKAGE_XPATH_TEMPLATE.format(package=package)
                    ))
                )
                self._safe_click(pack_el)
                print(f"Checkpoint 10: Package selected -> {package}")
                time.sleep(wait_after)
                return package
            except Exception:
                continue

        raise Exception("No package could be selected")


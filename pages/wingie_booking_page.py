import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class WingieBookingPage(BasePage):
    """Page object for Wingie booking form"""

    # Contact info locators
    EMAIL_INPUT = (By.ID, "contact_email")
    PHONE_INPUT = (By.ID, "contact_cellphone")

    # Passenger info locators
    FIRST_NAME_INPUT = (By.ID, "firstName_0")
    LAST_NAME_INPUT = (By.ID, "lastName_0")
    GENDER_FEMALE = (By.ID, "gender_F_0")
    GENDER_MALE = (By.ID, "gender_M_0")

    # Date of birth locators
    BIRTH_DAY = (By.ID, "birthDateDay_0")
    BIRTH_MONTH = (By.ID, "birthDateMonth_0")
    BIRTH_YEAR = (By.ID, "birthDateYear_0")

    # Passport locators
    PASSPORT_NUMBER = (By.ID, "passportNoAll_0")
    PASSPORT_DAY = (By.ID, "passportDay_0")
    PASSPORT_MONTH = (By.ID, "passportMonth_0")
    PASSPORT_YEAR = (By.ID, "passportYear_0")

    def __init__(self, driver, wait=None):
        super().__init__(driver, wait)

    def fill_contact_info(self, email, phone):
        """
        Fill contact information
        
        Args:
            email: Email address
            phone: Phone number
        """
        self.close_overlay_if_any()
        
        email_input = self.wait.until(
            EC.presence_of_element_located(self.EMAIL_INPUT)
        )
        email_input.clear()
        email_input.send_keys(email)

        phone_input = self.driver.find_element(*self.PHONE_INPUT)
        phone_input.clear()
        phone_input.send_keys(phone)

    def fill_passenger_name(self, first_name, last_name):
        """
        Fill passenger name
        
        Args:
            first_name: First name
            last_name: Last name
        """
        fn_input = self.driver.find_element(*self.FIRST_NAME_INPUT)
        fn_input.clear()
        fn_input.send_keys(first_name)

        ln_input = self.driver.find_element(*self.LAST_NAME_INPUT)
        ln_input.clear()
        ln_input.send_keys(last_name)

    def select_gender(self, gender="F"):
        """
        Select passenger gender
        
        Args:
            gender: 'F' for Female or 'M' for Male
        """
        try:
            if gender == "F":
                female = self.driver.find_element(*self.GENDER_FEMALE)
                self.safe_click(female)
            else:
                male = self.driver.find_element(*self.GENDER_MALE)
                self.safe_click(male)
        except Exception:
            # Fallback to male if female not available
            male = self.driver.find_element(*self.GENDER_MALE)
            self.safe_click(male)

    def fill_date_of_birth(self, day, month, year):
        """
        Fill date of birth
        
        Args:
            day: Day (1-31)
            month: Month (1-12)
            year: Year (YYYY)
        """
        Select(self.driver.find_element(*self.BIRTH_DAY)).select_by_value(f"{day:02d}")
        Select(self.driver.find_element(*self.BIRTH_MONTH)).select_by_value(f"{month:02d}")
        Select(self.driver.find_element(*self.BIRTH_YEAR)).select_by_value(str(year))

    def fill_passport_info(self, passport_number, exp_day, exp_month, exp_year):
        """
        Fill passport information
        
        Args:
            passport_number: Passport number
            exp_day: Expiry day (1-31)
            exp_month: Expiry month (1-12)
            exp_year: Expiry year (YYYY)
        """
        pass_input = self.driver.find_element(*self.PASSPORT_NUMBER)
        pass_input.clear()
        pass_input.send_keys(passport_number)

        Select(self.driver.find_element(*self.PASSPORT_DAY)).select_by_value(f"{exp_day:02d}")
        Select(self.driver.find_element(*self.PASSPORT_MONTH)).select_by_value(f"{exp_month:02d}")
        Select(self.driver.find_element(*self.PASSPORT_YEAR)).select_by_value(str(exp_year))

    def select_package(self, package_name="Standard"):
        """
        Select booking package
        
        Args:
            package_name: Package name (Standard, Comfort, or Basic)
        """
        packages_to_try = [package_name, "Standard", "Comfort", "Basic"]
        
        for pack in packages_to_try:
            try:
                pack_el = self.wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        f"//div[contains(@class,'provider-package__select') and .//p[normalize-space()='{pack}']]"
                    ))
                )
                self.safe_click(pack_el)
                return pack
            except Exception:
                continue
        
        raise Exception("No package could be selected")

    def fill_complete_booking_form(self, email, phone, first_name, last_name,
                                   birth_day, birth_month, birth_year,
                                   passport_number, passport_exp_day,
                                   passport_exp_month, passport_exp_year,
                                   gender="F", package="Standard"):
        """
        Fill the complete booking form
        
        Args:
            email: Email address
            phone: Phone number
            first_name: First name
            last_name: Last name
            birth_day: Birth day
            birth_month: Birth month
            birth_year: Birth year
            passport_number: Passport number
            passport_exp_day: Passport expiry day
            passport_exp_month: Passport expiry month
            passport_exp_year: Passport expiry year
            gender: Gender (F/M)
            package: Package name
        """
        self.fill_contact_info(email, phone)
        self.fill_passenger_name(first_name, last_name)
        self.select_gender(gender)
        self.fill_date_of_birth(birth_day, birth_month, birth_year)
        self.fill_passport_info(passport_number, passport_exp_day, 
                               passport_exp_month, passport_exp_year)
        selected_package = self.select_package(package)
        time.sleep(8)
        return selected_package

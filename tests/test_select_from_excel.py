"""
Test for W3Schools dropdown demo using test data from Excel
Tests select element by visible text and by value
All test data comes from testdata.xlsx - no hardcoded values
"""
import pytest
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from utils.excel_reader import read_test_data


class TestSelectFromExcel:
    """Test suite for dropdown selection using Excel test data"""
    
    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        """Load test data from Excel before each test"""
        self.test_data = read_test_data(sheet_name="data")
        assert len(self.test_data) > 0, "No test data found in Excel"
    
    @pytest.mark.parametrize("test_case", read_test_data(sheet_name="data"))
    def test_select_by_value(self, driver, screenshot_dir, artifact_dir, test_case):
        """
        Test: Select dropdown option by value attribute
        
        Steps:
        1. Navigate to URL from Excel
        2. Switch to iframe
        3. Find select element
        4. Select by value from Excel
        5. Verify selection
        6. Take screenshot
        """
        # Extract test data from parameter
        test_name = test_case.get("test_name", "unknown")
        url = test_case.get("url")
        dropdown_value = test_case.get("dropdown_value")
        expected_selected_text = test_case.get("expected_selected_text")
        
        assert url, "URL not found in test data"
        assert dropdown_value, "dropdown_value not found in test data"
        assert expected_selected_text, "expected_selected_text not found in test data"
        
        # Navigate to URL and enter iframe (remote can be slower)
        driver.get(url)
        driver.switch_to.default_content()
        wait = WebDriverWait(driver, 25)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iframeResult")))
        
        # Find the select element by id for reliability; visibility was flaky on BrowserStack, so use presence and log
        try:
            select_element = wait.until(
                EC.presence_of_element_located((By.ID, "cars"))
            )
        except TimeoutException:
            self._dump_debug(driver, artifact_dir, "select_not_found_value")
            raise

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", select_element)
        assert select_element.is_enabled(), "Select dropdown is not enabled"

        # Create Select object and select by value
        select = Select(select_element)
        select.select_by_value(dropdown_value)

        # Verify that the correct option is selected
        selected_option = select.first_selected_option
        assert selected_option.text == expected_selected_text, \
            f"Expected '{expected_selected_text}', but got '{selected_option.text}'"

        # Take screenshot
        browser_name = driver.capabilities.get("browserName", "unknown").lower()
        screenshot_path = screenshot_dir / f"{test_name}_select_by_value_{browser_name}.png"
        driver.save_screenshot(str(screenshot_path))

        print(f"✓ Test passed: {test_name} - Selected '{selected_option.text}' by value '{dropdown_value}'")
        print(f"✓ Screenshot saved to: {screenshot_path}")
    
    @pytest.mark.parametrize("test_case", read_test_data(sheet_name="data"))
    def test_select_by_visible_text(self, driver, screenshot_dir, artifact_dir, test_case):
        """
        Test: Select dropdown option by visible text
        
        Steps:
        1. Navigate to URL from Excel
        2. Switch to iframe
        3. Find select element
        4. Select by visible text from Excel
        5. Verify selection
        6. Take screenshot
        """
        # Extract test data from parameter
        test_name = test_case.get("test_name", "unknown")
        url = test_case.get("url")
        dropdown_text = test_case.get("dropdown_text")
        expected_selected_text = test_case.get("expected_selected_text")
        
        assert url, "URL not found in test data"
        assert dropdown_text, "dropdown_text not found in test data"
        assert expected_selected_text, "expected_selected_text not found in test data"
        
        # Navigate to URL and enter iframe (remote can be slower)
        driver.get(url)
        driver.switch_to.default_content()
        wait = WebDriverWait(driver, 25)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iframeResult")))
        
        # Find the select element by id for reliability; visibility was flaky on BrowserStack, so use presence and log
        try:
            select_element = wait.until(
                EC.presence_of_element_located((By.ID, "cars"))
            )
        except TimeoutException:
            self._dump_debug(driver, artifact_dir, "select_not_found_text")
            raise

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", select_element)
        assert select_element.is_enabled(), "Select dropdown is not enabled"

        # Create Select object and select by visible text
        select = Select(select_element)
        select.select_by_visible_text(dropdown_text)

        # Verify that the correct option is selected
        selected_option = select.first_selected_option
        assert selected_option.text == expected_selected_text, \
            f"Expected '{expected_selected_text}', but got '{selected_option.text}'"

        # Take screenshot
        browser_name = driver.capabilities.get("browserName", "unknown").lower()
        screenshot_path = screenshot_dir / f"{test_name}_select_by_text_{browser_name}.png"
        driver.save_screenshot(str(screenshot_path))

        print(f"✓ Test passed: {test_name} - Selected '{selected_option.text}' by text '{dropdown_text}'")
        print(f"✓ Screenshot saved to: {screenshot_path}")

    def _dump_debug(self, driver, artifact_dir: Path, label: str):
        """Dump page source and a screenshot to help diagnose remote failures."""
        artifact_dir.mkdir(exist_ok=True)
        try:
            page_path = artifact_dir / f"debug_{label}.html"
            page_path.write_text(driver.page_source, encoding="utf-8")
            print(f"Saved debug HTML to {page_path}")
        except Exception as e:
            print(f"Failed to save page source: {e}")

        try:
            screenshot_path = artifact_dir / f"debug_{label}.png"
            driver.save_screenshot(str(screenshot_path))
            print(f"Saved debug screenshot to {screenshot_path}")
        except Exception as e:
            print(f"Failed to save debug screenshot: {e}")

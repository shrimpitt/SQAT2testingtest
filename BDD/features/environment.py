from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def before_all(context):
    """
    Setup that runs before all tests
    """
    print("=" * 80)
    print("Starting BDD Test Suite - Flight Booking on Aviasales")
    print("=" * 80)


def before_scenario(context, scenario):
    """
    Setup that runs before each scenario
    Initialize the browser and WebDriverWait
    """
    print(f"\n{'=' * 80}")
    print(f"Starting Scenario: {scenario.name}")
    print(f"{'=' * 80}\n")
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Optional: run in headless mode (uncomment if needed)
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    
    # Initialize the Chrome driver
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Set implicit wait and create explicit wait object
    context.driver.implicitly_wait(10)
    context.wait = WebDriverWait(context.driver, 20)
    
    # Remove webdriver property to avoid detection
    context.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    print("✓ Browser initialized successfully")


def after_scenario(context, scenario):
    """
    Cleanup that runs after each scenario
    """
    print(f"\n{'=' * 80}")
    if scenario.status == "failed":
        print(f"❌ Scenario FAILED: {scenario.name}")
        # Optionally take screenshot on failure
        try:
            screenshot_name = f"screenshot_{scenario.name.replace(' ', '_')}.png"
            context.driver.save_screenshot(screenshot_name)
            print(f"Screenshot saved: {screenshot_name}")
        except Exception as e:
            print(f"Could not save screenshot: {e}")
    else:
        print(f"✓ Scenario PASSED: {scenario.name}")
    print(f"{'=' * 80}\n")
    
    # Close the browser
    if hasattr(context, 'driver'):
        context.driver.quit()
        print("✓ Browser closed")


def after_all(context):
    """
    Cleanup that runs after all tests
    """
    print("\n" + "=" * 80)
    print("BDD Test Suite Completed")
    print("=" * 80)

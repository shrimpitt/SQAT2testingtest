"""
Pytest configuration and fixtures for Selenium WebDriver (local and remote)
Supports both local browser testing and BrowserStack remote testing
"""
import os
import pytest
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver


# Load environment variables from .env file
load_dotenv()


def pytest_addoption(parser):
    """Add custom command-line options for pytest"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use: chrome or edge (default: chrome)"
    )
    parser.addoption(
        "--remote",
        action="store_true",
        default=False,
        help="Run tests on BrowserStack remote (default: False for local)"
    )


@pytest.fixture
def driver(request):
    """
    Pytest fixture that provides WebDriver instance.
    Supports both local and BrowserStack remote execution.
    
    Environment variables:
    - RUN_REMOTE: Set to 'true' to use BrowserStack (or use --remote flag)
    - BROWSERSTACK_USERNAME: BrowserStack username
    - BROWSERSTACK_ACCESS_KEY: BrowserStack access key
    """
    browser = request.config.getoption("--browser").lower()
    run_remote = request.config.getoption("--remote") or os.getenv("RUN_REMOTE", "false").lower() == "true"
    
    if run_remote:
        driver_instance = _create_remote_driver(browser)
    else:
        driver_instance = _create_local_driver(browser)
    
    # Maximize window for consistency
    try:
        driver_instance.maximize_window()
    except Exception:
        pass
    
    yield driver_instance
    
    # Cleanup: quit the driver
    try:
        driver_instance.quit()
    except Exception as e:
        print(f"Error closing driver: {e}")


def _create_local_driver(browser: str):
    """Create a local WebDriver instance"""
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Selenium 4 автоматически скачает ChromeDriver
        return webdriver.Chrome(options=options)
        
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Selenium 4 автоматически скачает EdgeDriver
        return webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}. Use 'chrome' or 'edge'")


def _create_remote_driver(browser: str):
    """Create a BrowserStack RemoteWebDriver instance"""
    username = os.getenv("BROWSERSTACK_USERNAME")
    access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")

    if not username or not access_key:
        raise ValueError("BrowserStack credentials not found in .env")

    bstack_options = {
        "userName": username,
        "accessKey": access_key,
        "buildName": "SQAT_Assignment6_Build",
        "sessionName": f"Test_{browser}_Windows11",
        "debug": True,
        "networkLogs": True,
        "consoleLogs": "warnings"
    }

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.set_capability("browserName", "Chrome")
        options.set_capability("browserVersion", "latest")
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        options.set_capability("browserName", "Edge")
        options.set_capability("browserVersion", "latest")
    else:
        raise ValueError("Unsupported browser. Use chrome or edge")

    options.set_capability("platformName", "Windows 11")
    options.set_capability("acceptInsecureCerts", True)
    options.set_capability("bstack:options", bstack_options)

    browserstack_url = f"https://{username}:{access_key}@hub.browserstack.com/wd/hub"

    driver_instance = webdriver.Remote(
        command_executor=browserstack_url,
        options=options
    )

    return driver_instance


@pytest.fixture
def artifact_dir():
    """Fixture that provides artifact directory path"""
    artifact_path = Path(__file__).parent / "artifacts"
    artifact_path.mkdir(exist_ok=True)
    return artifact_path


@pytest.fixture
def screenshot_dir(artifact_dir):
    """Fixture that provides screenshot directory path"""
    screenshot_path = artifact_dir / "screenshots"
    screenshot_path.mkdir(exist_ok=True)
    return screenshot_path

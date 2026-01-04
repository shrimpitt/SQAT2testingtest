# Page Object Model (POM) Structure

This directory contains the Page Object Model implementation for the flight booking tests.

## Structure

```
pages/
├── __init__.py                 # Package initialization
├── base_page.py               # Base page class with common methods
├── aviasales_page.py          # Page object for Aviasales search/results
├── wingie_booking_page.py     # Page object for Wingie booking form
└── README.md                  # This file
```

## Page Objects

### BasePage (`base_page.py`)
Base class that provides common functionality for all page objects:
- `safe_click()` - Click with JavaScript fallback
- `close_overlay_if_any()` - Close modals/overlays
- `wait_for_page_load()` - Wait for page to load
- `switch_to_new_window()` - Switch to newly opened window

### AviasalesPage (`aviasales_page.py`)
Handles interactions with the Aviasales search results page:
- `open_search_results()` - Open search results with flight details
- `select_first_ticket()` - Click on first ticket price
- `click_buy_button()` - Click buy button and return window handle

### WingieBookingPage (`wingie_booking_page.py`)
Handles interactions with the Wingie booking form:
- `fill_contact_info()` - Fill email and phone
- `fill_passenger_name()` - Fill first and last name
- `select_gender()` - Select gender
- `fill_date_of_birth()` - Fill birth date
- `fill_passport_info()` - Fill passport details
- `select_package()` - Select booking package
- `fill_complete_booking_form()` - Fill entire form at once

## Usage

See `test_flight_booking_pom.py` for an example of how to use these page objects in tests.

### Example:
```python
from pages.aviasales_page import AviasalesPage
from pages.wingie_booking_page import WingieBookingPage

# Initialize page objects
aviasales = AviasalesPage(driver, wait)
wingie = WingieBookingPage(driver, wait)

# Use page object methods
aviasales.open_search_results("GUW", "ALA", "2502")
aviasales.select_first_ticket()
original_window = aviasales.click_buy_button()

# Switch to booking page
wingie.switch_to_new_window(original_window)
wingie.fill_contact_info("test@email.com", "77771234567")
```

## Benefits of POM

1. **Maintainability** - Page changes only require updates in one place
2. **Reusability** - Page objects can be reused across multiple tests
3. **Readability** - Tests are more readable and focused on test logic
4. **Separation of Concerns** - Test logic separated from page interactions

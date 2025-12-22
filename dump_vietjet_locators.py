import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://booking.vietjetqazaqstan.kz/?locale=ru"

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)

    driver.get(URL)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    time.sleep(6)  # дать JS догрузиться

    print("TITLE:", driver.title)
    print("URL:", driver.current_url)
    print("\n--- INPUTS / TEXTAREAS ---")
    inputs = driver.find_elements(By.XPATH, "//*[self::input or self::textarea]")
    for i, el in enumerate(inputs, start=1):
        try:
            print(i, {
                "tag": el.tag_name,
                "type": el.get_attribute("type"),
                "name": el.get_attribute("name"),
                "id": el.get_attribute("id"),
                "placeholder": el.get_attribute("placeholder"),
                "aria-label": el.get_attribute("aria-label"),
                "class": el.get_attribute("class")[:80] if el.get_attribute("class") else None
            })
        except Exception:
            pass

    print("\n--- BUTTONS ---")
    buttons = driver.find_elements(By.XPATH, "//button|//input[@type='submit']")
    for i, el in enumerate(buttons, start=1):
        try:
            txt = el.text.strip()
            val = el.get_attribute("value")
            print(i, {
                "text": txt[:60],
                "value": val,
                "id": el.get_attribute("id"),
                "class": el.get_attribute("class")[:80] if el.get_attribute("class") else None
            })
        except Exception:
            pass

    print("\nDone. Leave browser open for 20 sec...")
    time.sleep(20)
    driver.quit()

if __name__ == "__main__":
    main()

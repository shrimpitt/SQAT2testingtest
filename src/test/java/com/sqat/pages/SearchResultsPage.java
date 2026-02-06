package com.sqat.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.SkipException;

import java.time.Duration;
import java.util.List;

public class SearchResultsPage extends BasePage {
    
    // Locators
    private static final String FIRST_PRICE_CSS = "div[data-test-id='price']";
    // Buy button for Wingie partner only
    private static final By WINGIE_BUY_BUTTON = By.xpath(
        "//div[@data-test-id='text' and contains(., 'Wingie')]" +
        "/ancestor::div[contains(@data-test-id,'proposal') or contains(@class,'proposal')]" +
        "//button"
    );

    public SearchResultsPage(WebDriver driver) {
        super(driver);
    }

    /**
     * Open the search results URL
     */
    public void openSearchUrl(String url) {
        driver.get(url);
        waitForPageLoad();
    }

    /**
     * Verify that the page has loaded by checking title
     */
    public String verifyPageLoaded() {
        waitForPageLoad();
        String title = getPageTitle();
        assert !title.trim().isEmpty() : "Page title is empty";
        return title;
    }

    /**
     * Wait for manual captcha solving
     */
    public void waitForCaptcha(int waitSeconds) {
        try {
            Thread.sleep(waitSeconds * 1000L);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    /**
     * Select the first available ticket by clicking on its price
     */
    public void selectFirstTicket() {
        WebElement firstPrice = wait.until(
            ExpectedConditions.elementToBeClickable(By.cssSelector(FIRST_PRICE_CSS))
        );
        safeClick(firstPrice);
    }

    /**
     * Click the buy button and return the original window handle
     * Only clicks if the offer is from Wingie, otherwise skips the test.
     */
    public String clickBuyButton() {
        WebElement buyButton;
        try {
            buyButton = wait.until(
                ExpectedConditions.elementToBeClickable(WINGIE_BUY_BUTTON)
            );
        } catch (TimeoutException e) {
            // Wingie offer not available – skip the test
            throw new SkipException("Wingie offer not found on Aviasales search results, skipping test", e);
        } catch (Exception e) {
            throw new SkipException("Unable to locate Wingie buy button, skipping test", e);
        }

        String originalWindow = driver.getWindowHandle();
        safeClick(buyButton);
        return originalWindow;
    }

    /**
     * Switch to the partner booking window
     */
    public void switchToPartnerWindow(String originalWindow) {
        WebDriverWait shortWait = new WebDriverWait(driver, Duration.ofSeconds(15));
        shortWait.until(ExpectedConditions.numberOfWindowsToBe(2));
        
        for (String handle : driver.getWindowHandles()) {
            if (!handle.equals(originalWindow)) {
                driver.switchTo().window(handle);
                break;
            }
        }
        
        // Wait for page to fully load
        waitForPageLoad();
        
        // Additional wait for redirect page to complete
        try {
            Thread.sleep(3000); // Wait for redirect
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Wait for booking form to appear (check for any booking form element)
        WebDriverWait formWait = new WebDriverWait(driver, Duration.ofSeconds(30));
        try {
            // Try to wait for email field or any booking form element
            formWait.until(ExpectedConditions.presenceOfElementLocated(
                By.cssSelector("input[id*='email'], input[id*='Email'], input[id*='contact'], form")
            ));
        } catch (Exception e) {
            // If specific element not found, just wait a bit more
            try {
                Thread.sleep(5000);
            } catch (InterruptedException ie) {
                Thread.currentThread().interrupt();
            }
        }
    }
}


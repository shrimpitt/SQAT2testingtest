package com.sqat.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;

public class BasePage {
    protected WebDriver driver;
    protected WebDriverWait wait;

    public BasePage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(25));
    }

    /**
     * Safely click an element, using JavaScript if regular click fails
     */
    protected void safeClick(WebElement element) {
        try {
            element.click();
        } catch (Exception e) {
            JavascriptExecutor js = (JavascriptExecutor) driver;
            js.executeScript("arguments[0].click();", element);
        }
    }

    /**
     * Close any overlay/popup that might be present
     */
    public void closeOverlayIfAny() {
        List<WebElement> overlays = driver.findElements(
            By.cssSelector("[data-testid='closeIcon'], .close, .modal-close")
        );
        
        for (WebElement overlay : overlays) {
            try {
                if (overlay.isDisplayed()) {
                    safeClick(overlay);
                    Thread.sleep(500);
                    break;
                }
            } catch (Exception e) {
                continue;
            }
        }
    }

    /**
     * Wait for page to be fully loaded
     */
    public void waitForPageLoad() {
        wait.until(driver -> {
            String state = ((JavascriptExecutor) driver)
                .executeScript("return document.readyState").toString();
            return state.equals("complete");
        });
    }

    /**
     * Get the current page title
     */
    public String getPageTitle() {
        return driver.getTitle();
    }
}


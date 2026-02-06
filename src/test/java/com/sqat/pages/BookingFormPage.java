package com.sqat.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;

public class BookingFormPage extends BasePage {
    
    // Locators
    private static final String CONTACT_EMAIL_ID = "contact_email";
    private static final String CONTACT_PHONE_ID = "contact_cellphone";
    private static final String FIRST_NAME_ID = "firstName_0";
    private static final String LAST_NAME_ID = "lastName_0";
    private static final String GENDER_FEMALE_ID = "gender_F_0";
    private static final String GENDER_MALE_ID = "gender_M_0";
    private static final String BIRTH_DAY_ID = "birthDateDay_0";
    private static final String BIRTH_MONTH_ID = "birthDateMonth_0";
    private static final String BIRTH_YEAR_ID = "birthDateYear_0";
    private static final String PASSPORT_NUMBER_ID = "passportNoAll_0";
    private static final String PASSPORT_DAY_ID = "passportDay_0";
    private static final String PASSPORT_MONTH_ID = "passportMonth_0";
    private static final String PASSPORT_YEAR_ID = "passportYear_0";
    private static final String PACKAGE_XPATH_TEMPLATE = 
        "//div[contains(@class,'provider-package__select') and .//p[normalize-space()='%s']]";

    public BookingFormPage(WebDriver driver) {
        super(driver);
    }

    /**
     * Fill contact email and phone number
     */
    public void fillContactInfo(String email, String phone) {
        closeOverlayIfAny();
        
        // Wait for booking form to be ready - try multiple selectors
        WebDriverWait formWait = new WebDriverWait(driver, Duration.ofSeconds(30));
        
        // Try to find email field with multiple possible selectors
        WebElement emailInput = null;
        try {
            emailInput = formWait.until(
                ExpectedConditions.presenceOfElementLocated(By.id(CONTACT_EMAIL_ID))
            );
        } catch (Exception e) {
            // Try alternative selectors
            try {
                emailInput = formWait.until(
                    ExpectedConditions.presenceOfElementLocated(
                        By.cssSelector("input[id*='email'], input[name*='email'], input[type='email']")
                    )
                );
            } catch (Exception e2) {
                // Wait a bit more and try again
                try {
                    Thread.sleep(5000);
                    emailInput = driver.findElement(By.id(CONTACT_EMAIL_ID));
                } catch (Exception e3) {
                    throw new RuntimeException("Email input field not found after waiting", e3);
                }
            }
        }
        
        emailInput.clear();
        emailInput.sendKeys(email);

        WebElement phoneInput = driver.findElement(By.id(CONTACT_PHONE_ID));
        phoneInput.clear();
        phoneInput.sendKeys(phone);
    }

    /**
     * Fill passenger first and last name
     */
    public void fillPassengerName(String firstName, String lastName) {
        WebElement fnInput = driver.findElement(By.id(FIRST_NAME_ID));
        fnInput.clear();
        fnInput.sendKeys(firstName);

        WebElement lnInput = driver.findElement(By.id(LAST_NAME_ID));
        lnInput.clear();
        lnInput.sendKeys(lastName);
    }

    /**
     * Select gender (prefer female, fallback to male if not available)
     */
    public void selectGender(boolean preferFemale) {
        try {
            if (preferFemale) {
                WebElement female = driver.findElement(By.id(GENDER_FEMALE_ID));
                safeClick(female);
            } else {
                WebElement male = driver.findElement(By.id(GENDER_MALE_ID));
                safeClick(male);
            }
        } catch (Exception e) {
            // Fallback to the other option
            if (preferFemale) {
                WebElement male = driver.findElement(By.id(GENDER_MALE_ID));
                safeClick(male);
            } else {
                WebElement female = driver.findElement(By.id(GENDER_FEMALE_ID));
                safeClick(female);
            }
        }
    }

    /**
     * Fill date of birth using dropdown selects
     */
    public void fillDateOfBirth(int day, int month, int year) {
        Select daySelect = new Select(driver.findElement(By.id(BIRTH_DAY_ID)));
        daySelect.selectByValue(String.format("%02d", day));

        Select monthSelect = new Select(driver.findElement(By.id(BIRTH_MONTH_ID)));
        monthSelect.selectByValue(String.format("%02d", month));

        Select yearSelect = new Select(driver.findElement(By.id(BIRTH_YEAR_ID)));
        yearSelect.selectByValue(String.valueOf(year));
    }

    /**
     * Fill passport number and expiration date
     */
    public void fillPassportInfo(String passportNumber, int expDay, int expMonth, int expYear) {
        WebElement passInput = driver.findElement(By.id(PASSPORT_NUMBER_ID));
        passInput.clear();
        passInput.sendKeys(passportNumber);

        Select daySelect = new Select(driver.findElement(By.id(PASSPORT_DAY_ID)));
        daySelect.selectByValue(String.format("%02d", expDay));

        Select monthSelect = new Select(driver.findElement(By.id(PASSPORT_MONTH_ID)));
        monthSelect.selectByValue(String.format("%02d", expMonth));

        Select yearSelect = new Select(driver.findElement(By.id(PASSPORT_YEAR_ID)));
        yearSelect.selectByValue(String.valueOf(expYear));
    }

    /**
     * Select a package from the available options
     */
    public String selectPackage(List<String> preferredPackages) {
        if (preferredPackages == null || preferredPackages.isEmpty()) {
            preferredPackages = List.of("Standard", "Comfort", "Basic");
        }

        WebDriverWait shortWait = new WebDriverWait(driver, Duration.ofSeconds(8));
        
        for (String packageName : preferredPackages) {
            try {
                String xpath = String.format(PACKAGE_XPATH_TEMPLATE, packageName);
                WebElement packElement = shortWait.until(
                    ExpectedConditions.elementToBeClickable(By.xpath(xpath))
                );
                safeClick(packElement);
                Thread.sleep(8000);
                return packageName;
            } catch (Exception e) {
                continue;
            }
        }

        throw new RuntimeException("No package could be selected");
    }
}


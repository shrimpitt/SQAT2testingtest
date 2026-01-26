package com.sqat.tests;

import com.sqat.base.BaseTest;
import com.sqat.pages.BookingFormPage;
import com.sqat.pages.SearchResultsPage;
import org.testng.Assert;
import org.testng.annotations.Test;

import java.util.List;

public class FlightBookingTest extends BaseTest {

    @Test(description = "Test flight booking from Atyrau to Almaty until payment step")
    public void testBookingFromAtyrauUntilPayment() {
        // Initialize page objects
        SearchResultsPage searchPage = new SearchResultsPage(driver);
        BookingFormPage bookingPage = new BookingFormPage(driver);

        // 🔹 Атырау (GUW) → Алматы (ALA), 25 февраля
        String url = "https://www.aviasales.kz/search/GUW2502ALA1";
        
        logStep("Opening search results page");
        searchPage.openSearchUrl(url);
        
        // --- Checkpoint 1 ---
        String title = searchPage.verifyPageLoaded();
        Assert.assertNotNull(title, "Page title should not be null");
        Assert.assertFalse(title.trim().isEmpty(), "Page title should not be empty");
        logCheckpoint("Checkpoint 1: Page loaded -> " + title);

        // --- Captcha ---
        logStep("Waiting for manual captcha solving (30 seconds)");
        searchPage.waitForCaptcha(30);

        // --- Select first ticket ---
        logStep("Selecting first available ticket");
        searchPage.selectFirstTicket();
        logCheckpoint("Checkpoint 2: First ticket price clicked");

        // --- Buy button ---
        logStep("Clicking buy button");
        String originalWindow = searchPage.clickBuyButton();
        logCheckpoint("Checkpoint 3: Buy button clicked");

        // --- Switch to partner (Wingie) ---
        logStep("Switching to partner booking window");
        searchPage.switchToPartnerWindow(originalWindow);
        String partnerTitle = searchPage.getPageTitle();
        logCheckpoint("Checkpoint 4: Partner page opened -> " + partnerTitle);

        // ---------------- Test data ----------------
        String email = "sana.test2025@gmail.com";
        String phone = "77771234567";
        String firstName = "Sana";
        String lastName = "Bagym";
        int birthDay = 2;
        int birthMonth = 5;
        int birthYear = 2004;
        String passportNumber = "N4589217";
        int passportExpDay = 15;
        int passportExpMonth = 3;
        int passportExpYear = 2032;

        // --- Booking Form Page ---
        logStep("Filling contact information");
        bookingPage.fillContactInfo(email, phone);
        logCheckpoint("Checkpoint 5: Contact info filled");

        logStep("Filling passenger name");
        bookingPage.fillPassengerName(firstName, lastName);
        logCheckpoint("Checkpoint 6: Passenger name filled");

        logStep("Selecting gender");
        bookingPage.selectGender(true); // Prefer female
        logCheckpoint("Checkpoint 7: Gender selected");

        logStep("Filling date of birth");
        bookingPage.fillDateOfBirth(birthDay, birthMonth, birthYear);
        logCheckpoint("Checkpoint 8: Date of birth selected");

        logStep("Filling passport information");
        bookingPage.fillPassportInfo(passportNumber, passportExpDay, passportExpMonth, passportExpYear);
        logCheckpoint("Checkpoint 9: Passport data filled");

        logStep("Selecting travel package");
        String selectedPackage = bookingPage.selectPackage(List.of("Standard", "Comfort", "Basic"));
        logCheckpoint("Checkpoint 10: Package selected -> " + selectedPackage);

        logCheckpoint("Checkpoint 11: Test completed before payment step");
        logStep("Flight booking test completed successfully");
    }
}


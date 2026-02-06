package com.sqat.base;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.MediaEntityBuilder;
import com.aventstack.extentreports.Status;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;
import io.github.bonigarcia.wdm.WebDriverManager;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.ITestResult;
import org.testng.annotations.*;

import org.apache.commons.io.FileUtils;
import java.io.File;
import java.io.IOException;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class BaseTest {
    protected WebDriver driver;
    protected WebDriverWait wait;
    protected static ExtentReports extent;
    protected ExtentTest test;
    protected static Logger logger;
    
    private static final String REPORTS_PATH = "test-output/ExtentReport.html";
    private static final String SCREENSHOTS_PATH = "test-output/screenshots/";

    @BeforeClass
    public void setUpExtentReports() {
        logger = LogManager.getLogger(BaseTest.class);
        
        if (extent == null) {
            ExtentSparkReporter sparkReporter = new ExtentSparkReporter(REPORTS_PATH);
            sparkReporter.config().setTheme(com.aventstack.extentreports.reporter.configuration.Theme.STANDARD);
            sparkReporter.config().setDocumentTitle("Flight Booking Test Report");
            sparkReporter.config().setReportName("SQAT Assignment 5 - Test Execution Report");
            sparkReporter.config().setTimeStampFormat("yyyy-MM-dd HH:mm:ss");
            
            extent = new ExtentReports();
            extent.attachReporter(sparkReporter);
            extent.setSystemInfo("Application", "Aviasales.kz");
            extent.setSystemInfo("Browser", "Chrome");
            extent.setSystemInfo("Operating System", System.getProperty("os.name"));
            extent.setSystemInfo("Java Version", System.getProperty("java.version"));
            extent.setSystemInfo("Test Environment", "QA");
            extent.setSystemInfo("Tester", "Bagym Sana");
            
            logger.info("Extent Reports initialized successfully");
        }
    }


    @BeforeMethod
    public void setUp(ITestResult result) {
        logger.info("=== Starting Test: {} ===", result.getMethod().getMethodName());
        
        // Create ExtentTest instance
        test = extent.createTest(result.getMethod().getMethodName());
        test.log(Status.INFO, "Test execution started");
        
        // Setup WebDriverManager and ChromeDriver
        WebDriverManager.chromedriver().setup();
        logger.info("ChromeDriver setup completed using WebDriverManager");
        
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--start-maximized");
        options.addArguments("--disable-blink-features=AutomationControlled");
        options.addArguments("--disable-notifications");
        
        driver = new ChromeDriver(options);
        logger.info("ChromeDriver initialized with options");
        
        // Configure waits
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        wait = new WebDriverWait(driver, Duration.ofSeconds(25));
        logger.info("WebDriver waits configured");
        
        test.pass("WebDriver initialized successfully");
    }

    @AfterMethod
    public void tearDown(ITestResult result) {
        String testName = result.getMethod().getMethodName();
        
        if (result.getStatus() == ITestResult.FAILURE) {
            logger.error("Test FAILED: {}", testName);
            if (test != null) {
                test.fail("Test failed: " + result.getThrowable().getMessage());
            }
            
            // Capture screenshot on failure
            String screenshotPath = captureScreenshot(testName);
            if (screenshotPath != null && test != null) {
                try {
                    test.fail("Screenshot on failure", 
                        MediaEntityBuilder.createScreenCaptureFromPath(screenshotPath).build());
                    logger.info("Screenshot captured and attached to report");
                } catch (Exception e) {
                    logger.error("Failed to attach screenshot to report: {}", e.getMessage());
                }
            }
        } else if (result.getStatus() == ITestResult.SUCCESS) {
            logger.info("Test PASSED: {}", testName);
            if (test != null) {
                test.pass("Test completed successfully");
            }
        } else if (result.getStatus() == ITestResult.SKIP) {
            logger.warn("Test SKIPPED: {}", testName);
            if (test != null) {
                test.skip("Test skipped: " + result.getThrowable());
            }
        }
        
        if (driver != null) {
            driver.quit();
            logger.info("WebDriver closed");
        }
        
        logger.info("=== Test Completed: {} ===\n", testName);
    }

    @AfterClass
    public void tearDownExtentReports() {
        if (extent != null) {
            extent.flush();
            logger.info("Extent Reports flushed successfully. Report location: {}", REPORTS_PATH);
        }
    }

    /**
     * Capture screenshot and save to file
     * 
     * @param testName Name of the test for screenshot file naming
     * @return Path to the saved screenshot
     */
    protected String captureScreenshot(String testName) {
        try {
            // Create screenshots directory if it doesn't exist
            File screenshotDir = new File(SCREENSHOTS_PATH);
            if (!screenshotDir.exists()) {
                screenshotDir.mkdirs();
            }
            
            // Generate timestamp for unique filename
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            String fileName = testName + "_" + timestamp + ".png";
            String filePath = SCREENSHOTS_PATH + fileName;
            
            // Capture screenshot
            TakesScreenshot screenshot = (TakesScreenshot) driver;
            File sourceFile = screenshot.getScreenshotAs(OutputType.FILE);
            File destinationFile = new File(filePath);
            
            FileUtils.copyFile(sourceFile, destinationFile);
            logger.info("Screenshot captured: {}", filePath);
            
            return filePath;
        } catch (IOException e) {
            logger.error("Failed to capture screenshot: {}", e.getMessage());
            return null;
        }
    }

    /**
     * Log test step to both logger and Extent Report
     * 
     * @param message Step description
     */
    protected void logStep(String message) {
        logger.info(message);
        if (test != null) {
            test.info(message);
        }
    }
    
    /**
     * Log test pass step to both logger and Extent Report
     * 
     * @param message Step description
     */
    protected void logPass(String message) {
        logger.info("PASS: {}", message);
        if (test != null) {
            test.pass(message);
        }
    }
    
    /**
     * Log test warning to both logger and Extent Report
     * 
     * @param message Warning message
     */
    protected void logWarning(String message) {
        logger.warn(message);
        if (test != null) {
            test.warning(message);
        }
    }
    
    /**
     * Log checkpoint to both Log4j and ExtentReports
     */
    protected void logCheckpoint(String checkpoint) {
        logger.info("Checkpoint: {}", checkpoint);
        if (test != null) {
            test.info("Checkpoint: " + checkpoint);
        }
    }
}


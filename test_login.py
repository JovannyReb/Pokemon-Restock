"""
Test script for Target login functionality.

This script tests whether the login to Target works correctly with your credentials.
It's useful for debugging login issues before running the full monitoring script.
"""

import os
import time
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get credentials from environment variables
EMAIL = os.environ.get('TARGET_EMAIL')
PASSWORD = os.environ.get('TARGET_PASSWORD')

if not EMAIL or not PASSWORD:
    logger.error("Target credentials not found in environment variables.")
    logger.error("Please create a .env file with TARGET_EMAIL and TARGET_PASSWORD.")
    exit(1)

def test_target_login():
    """Test the Target login functionality."""
    logger.info("Setting up Chrome driver...")
    
    # Setup Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Initialize the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        logger.info("Navigating to Target login page...")
        driver.get("https://www.target.com/account")
        
        # Wait for the login form
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        logger.info(f"Entering email: {EMAIL[:3]}...{EMAIL[-3:]}")
        email_field = driver.find_element(By.ID, "username")
        email_field.clear()
        email_field.send_keys(EMAIL)
        
        logger.info("Entering password: ********")
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(PASSWORD)
        
        logger.info("Clicking login button...")
        login_button = driver.find_element(By.ID, "login")
        login_button.click()
        
        # Wait for either the passcode setup page or successful login
        try:
            # First, check if the passcode setup page appears
            try:
                logger.info("Checking for passcode setup page...")
                maybe_later_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Maybe later') or contains(text(), 'maybe later') or contains(@data-test, 'maybe-later')]"))
                )
                logger.info("Passcode setup page detected. Clicking 'Maybe later' button...")
                maybe_later_button.click()
                logger.info("Clicked 'Maybe later'. Continuing with login process...")
            except TimeoutException:
                logger.info("No passcode setup page detected, continuing with normal login flow...")
            
            # Now wait for successful login
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@data-test, 'account')]"))
            )
            logger.info("LOGIN SUCCESSFUL! You are now logged into Target.")
            
            # Get the account name if available
            try:
                account_name = driver.find_element(By.XPATH, "//span[contains(@data-test, 'accountName')]").text
                logger.info(f"Logged in as: {account_name}")
            except:
                pass
                
            # Keep the browser open for a while to see the result
            logger.info("Keeping browser open for 10 seconds...")
            time.sleep(10)
            
        except TimeoutException:
            logger.error("LOGIN FAILED - Could not detect successful login.")
            logger.error("Please check your credentials and try again.")
            
            # Check for error messages
            try:
                error_message = driver.find_element(By.XPATH, "//div[contains(@class, 'error')]").text
                logger.error(f"Error message: {error_message}")
            except:
                pass
                
            # Keep the browser open to see the error
            logger.info("Keeping browser open for 30 seconds to view the error...")
            time.sleep(30)
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        logger.info("Closing the browser...")
        driver.quit()

if __name__ == "__main__":
    test_target_login() 
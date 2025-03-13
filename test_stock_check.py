"""
Test script for checking stock status of Pokémon cards on Target.

This script tests the stock checking functionality without attempting to purchase.
It's useful for debugging and testing the stock detection logic.
"""

import time
import logging
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

# Items to check
ITEMS_TO_CHECK = [
    {
        "url": "https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-151-binder-collection/-/A-89444929",
        "name": "Pokémon Scarlet & Violet 151 Binder Collection"
    },
    # Add more items as needed
]

def check_stock(driver, item):
    """
    Check if an item is in stock.
    
    Args:
        driver: Selenium WebDriver instance
        item: Dictionary with item details (url, name)
        
    Returns:
        bool: True if in stock, False otherwise
    """
    try:
        logger.info(f"Checking stock for {item['name']} at {item['url']}...")
        driver.get(item['url'])
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Take a screenshot for debugging
        screenshot_filename = f"{item['name'].replace(' ', '_')}_screenshot.png"
        driver.save_screenshot(screenshot_filename)
        logger.info(f"Screenshot saved as {screenshot_filename}")
        
        # Check for out of stock indicators
        out_of_stock_elements = driver.find_elements(By.XPATH, 
            "//*[contains(text(), 'Out of stock') or contains(text(), 'Sold out') or contains(text(), 'Currently unavailable')]")
        
        if out_of_stock_elements:
            logger.info(f"{item['name']} is OUT OF STOCK.")
            
            # Print the exact text found for debugging
            for element in out_of_stock_elements:
                logger.info(f"Out of stock indicator found: '{element.text}'")
                
            return False
        else:
            # Look for "Add to cart" button
            try:
                add_to_cart_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Add to cart')]"))
                )
                logger.info(f"🎉 {item['name']} is IN STOCK! 'Add to cart' button found.")
                return True
            except TimeoutException:
                logger.warning(f"Could not find 'Add to cart' button for {item['name']}.")
                logger.warning("Item may be out of stock or the website structure has changed.")
                return False
                
    except Exception as e:
        logger.error(f"Error checking stock for {item['name']}: {str(e)}")
        return False

def test_stock_checker():
    """Test the stock checking functionality for all configured items."""
    logger.info("Setting up Chrome driver...")
    
    # Setup Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Initialize the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Check each item
        for item in ITEMS_TO_CHECK:
            in_stock = check_stock(driver, item)
            
            if in_stock:
                logger.info(f"✅ {item['name']} is IN STOCK and available for purchase!")
            else:
                logger.info(f"❌ {item['name']} is OUT OF STOCK.")
                
            # Add a delay between checks
            if item != ITEMS_TO_CHECK[-1]:  # If not the last item
                logger.info("Waiting 5 seconds before checking the next item...")
                time.sleep(5)
                
        logger.info("Stock check completed for all items.")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        logger.info("Closing the browser...")
        driver.quit()

if __name__ == "__main__":
    test_stock_checker() 
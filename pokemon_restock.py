"""
Target Pokémon Card Stock Monitor and Automatic Purchaser

This script monitors the stock status of specific Pokémon card items on Target's website.
When an item comes back in stock, it automatically logs into your Target account,
adds the item to the cart, and completes the checkout process.

Usage:
1. Set your Target account credentials in the environment variables or update them in the script.
2. Run the script: python pokemon_restock.py
3. The script will check the stock periodically and notify you when a purchase is attempted.

Note: Be respectful of Target's servers by using reasonable delays between checks.
"""

import os
import time
import logging
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='pokemon_restock.log',
    filemode='a'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)

# Load environment variables from .env file (if it exists)
load_dotenv()

# Configuration
# You can add multiple items to monitor by adding more URLs to this list
TARGET_ITEMS = [
    {
        "url": "https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-151-binder-collection/-/A-89444929",
        "name": "Pokémon Scarlet & Violet 151 Binder Collection"
    },
    # Add more items as needed, for example:
    # {
    #     "url": "https://www.target.com/p/pokemon-trading-card-game-another-item/-/A-12345678",
    #     "name": "Another Pokémon Item"
    # },
]

# Time in seconds between checks
CHECK_INTERVAL = int(os.environ.get('CHECK_INTERVAL', 60))
# Maximum number of retries for purchasing
MAX_RETRIES = int(os.environ.get('MAX_RETRIES', 3))
# Target account credentials
EMAIL = os.environ.get('TARGET_EMAIL', 'YOUR_EMAIL')
PASSWORD = os.environ.get('TARGET_PASSWORD', 'YOUR_PASSWORD')

# Email notification settings (optional)
SEND_EMAIL_NOTIFICATIONS = False  # Set to True to enable email notifications
NOTIFICATION_EMAIL = os.environ.get('NOTIFICATION_EMAIL', '')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))

class TargetPokemonRestockMonitor:
    def __init__(self):
        self.driver = None
        self.setup_driver()
        
    def setup_driver(self):
        """Set up the Chrome webdriver with appropriate options."""
        logger.info("Setting up the Chrome webdriver...")
        chrome_options = webdriver.ChromeOptions()
        
        # Add options to make the bot less detectable
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # Optional: Add user agent to appear more like a normal browser
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Make the window size like a regular browser
        self.driver.set_window_size(1366, 768)
        
        # Override the navigator.webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def check_stock(self, item):
        """
        Check if the item is in stock on the Target website.
        Args:
            item: Dictionary containing item details (url, name)
        Returns: True if in stock, False otherwise
        """
        try:
            logger.info(f"Checking stock for {item['name']} at {item['url']}...")
            self.driver.get(item['url'])
            
            # Wait for the page to load properly
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Random pause to mimic human behavior
            time.sleep(random.uniform(1, 3))
            
            # Check for "Out of stock" or "Sold out" indicators
            try:
                out_of_stock_elements = self.driver.find_elements(By.XPATH, 
                    "//*[contains(text(), 'Out of stock') or contains(text(), 'Sold out') or contains(text(), 'Currently unavailable')]")
                
                if out_of_stock_elements:
                    logger.info(f"{item['name']} is out of stock.")
                    return False
                else:
                    # Look for "Add to cart" button as an indication it's in stock
                    add_to_cart_button = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Add to cart')]"))
                    )
                    logger.info(f"ITEM IS IN STOCK! {item['name']} is available for purchase!")
                    return True
            except TimeoutException:
                logger.info(f"Could not determine stock status for {item['name']} (timeout waiting for elements).")
                return False
            
        except Exception as e:
            logger.error(f"Error checking stock for {item['name']}: {str(e)}")
            return False

    def login(self):
        """
        Log into Target account.
        Returns: True if login successful, False otherwise
        """
        try:
            logger.info("Attempting to login to Target account...")
            
            # Navigate to the login page
            self.driver.get("https://www.target.com/account")
            
            # Wait for the login form to appear
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Enter email
            email_field = self.driver.find_element(By.ID, "username")
            email_field.clear()
            email_field.send_keys(EMAIL)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(PASSWORD)
            
            # Random pause to mimic human behavior
            time.sleep(random.uniform(0.5, 1.5))
            
            # Click login button
            login_button = self.driver.find_element(By.ID, "login")
            login_button.click()
            
            # Wait for login to complete
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@data-test, 'account')]"))
                )
                logger.info("Successfully logged in to Target account.")
                return True
            except TimeoutException:
                logger.error("Failed to login - timeout waiting for account element.")
                return False
                
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return False

    def add_to_cart(self, item):
        """
        Add the item to cart.
        Args:
            item: Dictionary containing item details (url, name)
        Returns: True if successfully added to cart, False otherwise
        """
        try:
            logger.info(f"Attempting to add {item['name']} to cart...")
            
            # Navigate to the product page if not already there
            current_url = self.driver.current_url
            if item['url'] not in current_url:
                self.driver.get(item['url'])
                # Wait for page to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            
            # Find and click the "Add to cart" button
            add_to_cart_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add to cart')]"))
            )
            add_to_cart_button.click()
            
            # Wait for the "Added to cart" confirmation or cart icon update
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Added to cart') or contains(text(), 'Item added to cart')]"))
                )
                logger.info(f"Successfully added {item['name']} to cart.")
                return True
            except TimeoutException:
                # Alternative check - see if the cart count has increased
                try:
                    cart_count = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//a[@data-test='@web/CartLink']//*[contains(@data-test, 'cartItem')]"))
                    )
                    if cart_count:
                        logger.info(f"{item['name']} appears to be added to cart (cart count updated).")
                        return True
                except:
                    pass
                    
                logger.error(f"Failed to add {item['name']} to cart - no confirmation found.")
                return False
                
        except Exception as e:
            logger.error(f"Error adding {item['name']} to cart: {str(e)}")
            return False

    def checkout(self):
        """
        Complete the checkout process.
        Returns: True if checkout successful, False otherwise
        """
        try:
            logger.info("Proceeding to checkout...")
            
            # Go to cart page
            self.driver.get("https://www.target.com/co-cart")
            
            # Wait for cart page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Cart')]"))
            )
            
            # Click checkout button
            checkout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Check out')]"))
            )
            checkout_button.click()
            
            # Wait for the checkout page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Shipping') or contains(text(), 'Delivery')]"))
            )
            
            # Continue with checkout process - this will vary depending on whether you have saved payment methods
            # You may need to select shipping method, payment method, etc.
            
            # Wait for the "Place order" button
            place_order_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Place order')]"))
            )
            
            # Final confirmation - uncomment this line when you're sure everything works correctly
            # place_order_button.click()
            
            logger.info("CHECKOUT PROCESS COMPLETED! Note: final 'Place order' click is commented out for safety.")
            logger.info("Review your order and click the Place Order button manually.")
            
            # Keep the browser window open for manual review
            time.sleep(600)  # Keep the window open for 10 minutes
            
            return True
            
        except Exception as e:
            logger.error(f"Error during checkout: {str(e)}")
            return False

    def send_notification(self, subject, message):
        """
        Send an email notification.
        Args:
            subject: Email subject
            message: Email message body
        Returns: True if email sent successfully, False otherwise
        """
        if not SEND_EMAIL_NOTIFICATIONS or not NOTIFICATION_EMAIL or not EMAIL_PASSWORD:
            logger.info("Email notifications are disabled or not configured.")
            return False
            
        try:
            logger.info(f"Sending email notification: {subject}")
            
            msg = MIMEMultipart()
            msg['From'] = NOTIFICATION_EMAIL
            msg['To'] = NOTIFICATION_EMAIL  # Send to self
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(NOTIFICATION_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            logger.info("Email notification sent successfully.")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email notification: {str(e)}")
            return False

    def purchase_when_in_stock(self):
        """Main function to monitor stock and purchase when available."""
        logger.info("Starting Pokemon card restock monitor...")
        
        if not TARGET_ITEMS:
            logger.error("No items configured to monitor. Please add items to the TARGET_ITEMS list.")
            return
            
        retry_count = 0
        in_stock_item = None
        
        try:
            # Login first so we're ready to purchase quickly
            if not self.login():
                logger.error("Failed to login. Please check your credentials.")
                return
                
            while True:
                # Check each item in the list
                for item in TARGET_ITEMS:
                    # Check if item is in stock
                    if self.check_stock(item):
                        logger.info(f"{item['name']} is in stock! Attempting to purchase...")
                        in_stock_item = item
                        
                        # Send notification
                        self.send_notification(
                            f"Pokemon Card In Stock: {item['name']}",
                            f"The item '{item['name']}' is now in stock at Target!\n\nURL: {item['url']}\n\nAttempting to purchase automatically."
                        )
                        
                        # Try to add to cart
                        if self.add_to_cart(item):
                            # Proceed to checkout
                            if self.checkout():
                                logger.info(f"Purchase attempt for {item['name']} completed!")
                                
                                # Send success notification
                                self.send_notification(
                                    f"Purchase Attempt Completed: {item['name']}",
                                    f"The purchase process for '{item['name']}' has been completed!\n\nPlease check your Target account for order confirmation."
                                )
                                
                                return  # Exit after successful purchase
                            else:
                                logger.error("Checkout failed.")
                                
                                # Send failure notification
                                self.send_notification(
                                    f"Checkout Failed: {item['name']}",
                                    f"The checkout process for '{item['name']}' has failed.\n\nPlease try manually: {item['url']}"
                                )
                        else:
                            logger.error(f"Failed to add {item['name']} to cart.")
                            
                            # Send failure notification
                            self.send_notification(
                                f"Add to Cart Failed: {item['name']}",
                                f"Failed to add '{item['name']}' to cart.\n\nPlease try manually: {item['url']}"
                            )
                        
                        # Increment retry counter
                        retry_count += 1
                        if retry_count >= MAX_RETRIES:
                            logger.error(f"Maximum number of retries ({MAX_RETRIES}) reached. Stopping.")
                            return
                        
                        # Break the loop to retry this item
                        break
                else:  # This else belongs to the for loop (executes when no break occurs)
                    # Reset retry counter when all items are out of stock
                    retry_count = 0
                    
                    # Wait before checking again
                    wait_time = CHECK_INTERVAL + random.uniform(-5, 5)  # Add some randomness
                    logger.info(f"All items are out of stock. Checking again in approximately {wait_time:.0f} seconds...")
                    time.sleep(wait_time)
                    
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user.")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
        finally:
            # Keep browser open if we reached checkout, otherwise close it
            if not (in_stock_item and retry_count > 0):
                if self.driver:
                    self.driver.quit()
                    logger.info("Browser closed.")

    def close(self):
        """Close the webdriver."""
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    monitor = TargetPokemonRestockMonitor()
    try:
        monitor.purchase_when_in_stock()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
    finally:
        monitor.close() 
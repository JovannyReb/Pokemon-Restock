# Pokémon Card Restock Automation

This project automatically monitors Target's website for Pokémon trading cards and purchases them when they come back in stock.

## Features

- Continuously monitors Target's website for specific Pokémon card items
- Automatically logs into your Target account
- Adds items to your cart when they become available
- Completes the checkout process (with a safety check before final purchase)
- Discord notifications with rich embeds showing product images, price and availability
- Randomizes timing to behave more like a human user
- Detailed logging to track activity

## Prerequisites

- Python 3.8 or higher
- Chrome web browser
- ChromeDriver (automatically installed by webdriver-manager)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/Pokemon-Restock.git
   cd Pokemon-Restock
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Target credentials:
   ```
   cp .env-template .env
   ```
   
4. Edit the `.env` file with your actual Target login credentials.

## Configuration

The main configuration variables are at the top of `pokemon_restock.py`:

- `TARGET_URL`: The URL of the specific item you want to monitor
- `CHECK_INTERVAL`: How often to check stock (in seconds)
- `MAX_RETRIES`: Maximum number of purchase attempts if errors occur

If you want to monitor multiple items, you can modify the script to use a list of URLs.

## Usage

Run the script with:

```
python pokemon_restock.py
```

The script will:
1. Log in to your Target account
2. Begin monitoring the item's stock status
3. When the item comes in stock, it will automatically add it to your cart and proceed to checkout
4. By default, the final "Place order" button click is commented out for safety. The script will pause at the final checkout step for you to review and manually complete the purchase.

To have the script automatically complete the purchase without manual intervention, uncomment the line `# place_order_button.click()` in the `checkout()` method.

## Notes

- The script includes logging to both the console and a file (`pokemon_restock.log`).
- Use reasonable `CHECK_INTERVAL` values to avoid overloading Target's servers.
- Web scraping and automation may be against Target's Terms of Service. Use at your own risk.
- The script includes measures to avoid detection as a bot, but these are not guaranteed to work indefinitely.

## Customization

You can customize the script by:

- Adding multiple product URLs to monitor
- Setting up email or SMS notifications when purchases are made
- Adjusting the checkout process if Target's website changes
- Customizing XPath selectors if needed

## Troubleshooting

If the script fails to run:

1. Ensure Chrome is installed and up-to-date
2. Check that your Target credentials are correct in the `.env` file
3. Review the log file for specific error messages
4. Target may have changed its website structure, requiring updates to the XPath selectors

## Multi-Instance Monitoring

The repository now includes a powerful multi-instance monitoring system that can run multiple Chrome instances simultaneously to check multiple products in parallel.

### Key Features

- **Parallel Monitoring**: Check multiple products simultaneously
- **Scalable**: Configure how many instances to run at once
- **Anti-Detection**: Each instance uses a unique user profile and slightly different user agent
- **Notifications**: Get alerted via email, Discord, or SMS when items are in stock
- **Thread Management**: Automatically manages resources to prevent overloading your system

### How to Use Multi-Instance Monitoring

1. **Configure your products**:
   - Edit the `ITEMS_TO_MONITOR` list in `multi_chrome_monitor.py`
   - Add URLs and names for the products you want to track

2. **Set up environment variables**:
   - Copy `.env.template` to `.env`
   - Add your Target login credentials
   - Configure notification settings

3. **Run the monitor**:
   ```bash
   python multi_chrome_monitor.py
   ```

4. **Adjust concurrent instances**:
   - Change `MAX_CONCURRENT_INSTANCES` in your `.env` file
   - Default is 3 concurrent instances

### System Requirements

Running multiple Chrome instances requires more system resources:
- At least 4GB RAM (8GB+ recommended)
- Stable internet connection
- Sufficient disk space for Chrome profiles

### Running on a Server

For running the multi-instance monitor on a server:
1. Uncomment the headless browser options in the `monitor_item` function
2. Install required dependencies: `pip install -r requirements.txt`
3. Set up a cron job or use a process manager like PM2 to keep it running

## Auto-Purchase Monitoring

In addition to multi-instance monitoring, this repository now includes an automatic purchasing system that can both monitor and complete purchases when items become available.

### Auto-Purchase Features

- **Automatic Checkout**: Complete the entire purchase flow automatically
- **Quantity Configuration**: Specify how many of each item you want to purchase
- **Safety Confirmation**: Optional manual confirmation before final purchase
- **Purchase Notifications**: Get alerts when purchases are completed successfully

### How to Use Auto-Purchase Monitoring

1. **Configure your products and quantities**:
   - Edit the `ITEMS_TO_MONITOR` list in `auto_purchase_monitor.py` to add or remove products
   - Set quantities in your `.env` file using the format `ITEM_QUANTITY_ID=value`
   - For example, to buy 3 of the Pikachu VMAX set: `ITEM_QUANTITY_PIKACHU_VMAX=3`

2. **Set up environment variables**:
   - Copy `.env.template` to `.env`
   - Add your Target login credentials
   - Configure desired quantities for each item
   - Set `AUTO_PURCHASE=True` to enable automatic purchasing
   - Set `REQUIRE_PURCHASE_CONFIRMATION=True` for added safety (recommended)

3. **Run the auto-purchase monitor**:
   ```bash
   python auto_purchase_monitor.py
   ```

4. **Safety features**:
   - With confirmation enabled, the system will stop at the final checkout page
   - You'll receive a notification to manually confirm the purchase
   - Without confirmation, purchases will complete automatically (use with caution)

### Important Notes About Auto-Purchase

1. **Use responsibly**: Automated purchasing may be against Target's terms of service
2. **Testing recommended**: Test the script without auto-purchase first
3. **Payment method**: Ensure your default payment method is set up on your Target account
4. **Shipping address**: Your shipping address should be configured in your Target account

## Notifications

### Discord Notifications (Primary Method)

This project uses Discord as the primary notification method, providing rich embeds with product images, price, and other details when an item changes status.

1. **Create a Discord Server**: If you don't already have one, create a new Discord server.

2. **Create a Webhook**:
   - Open your Discord server
   - Go to Server Settings > Integrations > Webhooks
   - Click "New Webhook"
   - Give it a name like "Pokemon Restock Alerts"
   - Choose which channel to post to (create a dedicated #restock-alerts channel)
   - Copy the webhook URL

3. **Configure Your .env File**:
   ```
   USE_DISCORD_NOTIFICATIONS=True
   DISCORD_WEBHOOK_URL=your-copied-webhook-url
   ```

### Discord Notification Features

- **Rich Embeds**: Includes product image, name, price, and item details
- **Direct Links**: Click directly on the product link to go to Target
- **Visual Indicators**: Color-coded for easy visibility
- **Real-time Updates**: Get notified the moment an item is back in stock
- **Event-Based Notifications**: Different alerts for in-stock items, out-of-stock changes, and successful purchases
- **Ping Support**: Optional pings for @everyone, @here, or specific roles

### Discord Notification Types

The monitor sends different types of notifications:

1. **In-Stock Alerts**: 🎉 Green notification when an item comes back in stock
2. **Out-of-Stock Alerts**: 📉 Red notification when a previously in-stock item sells out
3. **Checkout Success**: 💰 Gold notification when an item is successfully purchased

### Setting Up Discord Pings

To enable Discord pings for important notifications:

1. **Configure your .env file**:
   ```
   # To ping everyone in your server (use carefully)
   DISCORD_PING_EVERYONE=True
   
   # OR to ping only online users
   DISCORD_PING_HERE=True
   
   # OR to ping a specific role (recommended)
   DISCORD_PING_ROLE_ID=123456789012345678
   ```

2. **Creating a Role for Pings** (recommended approach):
   - Go to Server Settings > Roles > Create Role
   - Name it something like "Restock Alerts"
   - Set the permissions as needed
   - Go to the role settings and copy the Role ID (Developer Mode must be enabled)
   - Add the Role ID to your .env file
   - Assign the role to users who should receive notifications

### Alternative Notification Methods

While Discord is the recommended notification method, the system also supports:

- **SMS Notifications**: Configure Twilio settings in your .env file to receive text message alerts
   ```
   USE_SMS_NOTIFICATIONS=True
   TWILIO_ACCOUNT_SID=your-twilio-account-sid

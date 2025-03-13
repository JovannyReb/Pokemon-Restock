# Pokémon Card Restock Automation

This project automatically monitors Target's website for Pokémon trading cards and purchases them when they come back in stock.

## Features

- Continuously monitors Target's website for specific Pokémon card items
- Automatically logs into your Target account
- Adds items to your cart when they become available
- Completes the checkout process (with a safety check before final purchase)
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

## License

This project is for educational purposes only. 
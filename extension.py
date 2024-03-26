import os
from playwright.sync_api import sync_playwright

# Path to your extension folder
path_to_extension = os.path.abspath("./extension/vpn")
# User data directory for the browser context
user_data_dir = "./"

with sync_playwright() as playwright:
    # Initialize a persistent Chrome instance
    context = playwright.chromium.launch_persistent_context(
        user_data_dir, # User data directory argument is required
        headless=False, # Run the browser in headful mode
         slow_mo=1000,
         is_mobile=True,
        args=[
            f"--disable-extensions-except={path_to_extension}",
            f"--load-extension={path_to_extension}",
        ],
    )
    # Initialize a new browser page
    page = context.new_page()
    # Go to the Chrome extensions page to verify the extension is loaded
    page.goto("chrome://extensions/")
    page.wait_for_timeout(20000)
    # Take a screenshot to verify the extension is loaded
    # page.screenshot(path="playwright_chrome_extensions.png")

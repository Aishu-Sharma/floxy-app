from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

# Set up options for Android
options = UiAutomator2Options()
options.platform_name = "Android"  # or "iOS"
options.platform_version = "14.0"  # e.g., "11.0" or "12.0"
options.device_name = "c1b0c61b92420beb"  # Name of your device
options.app_package = "io.floxypay.fxy.twa"  # App's package name
options.app_activity = "Activity.MainActivity"  # App's main activity

# URL of the Appium server
appium_server_url = "http://127.0.0.1:4723/wd/hub"#"http://49.36.138.63:4723/wd/hub"

# Initialize the driver and connect to the Appium server
driver = webdriver.Remote(command_executor=appium_server_url, options=options)

# Wait for the app to load
time.sleep(5)

# Example action: print the current activity of the app
print("Current Activity:", driver.current_activity)

# End the session
driver.quit()

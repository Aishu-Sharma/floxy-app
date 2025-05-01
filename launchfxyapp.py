from appium import webdriver
from appium.options.android import UiAutomator2Options
from time import sleep

# Define the Appium server URL
appium_server_url = "http://192.168.0.228:4723/wd/hub"

# Define the options
options = UiAutomator2Options()
options.platform_name = "Android"                # Operating System
options.platform_version = "14.0"                # Android version on your device
options.device_name = "RMX2202L1"                # Device name or emulator name
options.app_package = "io.floxypay.fxy.twa"      # Corrected package name
options.app_activity = "com.example.floxy_pay.MainActivity"  # Corrected activity name
options.no_reset = True                          # Retain app state between sessions
options.full_reset = False                       # Avoids full reset of the app state
options.ignore_hidden_api_policy_error = True    # Ignores hidden API policy errors

# Initialize the driver
try:
    # Connect to the Appium server and launch the app
    driver = webdriver.Remote(command_executor=appium_server_url, options=options)
    print("App has been launched on the device!")

    # Perform some actions on the app (example)
    # Sleep to keep the app open for a while
    sleep(10)

    # Close the app and driver session
    driver.quit()
    print("Test completed and driver session ended.")
except Exception as e:
    print("An error occurred:", e)

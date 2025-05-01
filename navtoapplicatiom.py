from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Define the Appium server URL
appium_server_url = "http://0.0.0.0:4723/wd/hub"

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

# Initialize the driver and interact with the app
try:
    # Connect to the Appium server and launch the app
    driver = webdriver.Remote(command_executor=appium_server_url, options=options)
    print("App has been launched on the device!")

    # Wait for the app to open
    sleep(5)

    # Use WebDriverWait to wait until the button is clickable using the class name
    wait = WebDriverWait(driver, 20)  # 20 seconds timeout

    # Click the first button 3 times
    for i in range(2):
        # Locate the button each time to ensure it is interactable
        button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "android.widget.Button")))
        button.click()
        print(f"Button clicked {i + 1} times")
        sleep(1)  # Optional delay between clicks

    # Click on the "Get Started" button
    get_started_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//android.view.View[@content-desc='Get Started']")))
    get_started_button.click()
    print("Get Started button clicked!")

    # Click on the first "Continue with Google" button
    continue_with_google_button_1 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.widget.FrameLayout[@resource-id='android:id/content']"
                   "/android.widget.FrameLayout/android.view.View/android.view.View/"
                   "android.view.View/android.view.View/android.widget.ImageView[1]")
    ))
    continue_with_google_button_1.click()
    print("First 'Continue with Google' button clicked!")

    # Click on the "Choose Account" button using the corrected XPath
    choose_account_button = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//android.view.View[@resource-id='yDmH0d']/android.view.View[3]")
    ))
    choose_account_button.click()
    print("Choose Account button clicked!")
    sleep(2)

    # Click on the "Continue" button
    continue_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.widget.Button[@text='Continue']")
    ))
    continue_button.click()
    print("Continue button clicked!")

    # Click on the "Skip for Now" button
    skip_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.widget.Button[@text='Skip for Now']")
    ))
    skip_button.click()
    print("Skip for Now button clicked!")
    sleep(5)

    # Enter MPIN by clicking buttons with specific XPaths
    for i in range(1, 7):  # From 1 to 6
        mpin_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//android.view.View[@content-desc="{1}"]')  # Using XPath for each MPIN digit
        ))
        mpin_button.click()
        print(f"MPIN digit {1} entered")
        sleep(1)  # Optional delay between entering digits

    print("App is logged in")

    # Click on send button
    send_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.widget.ImageView[@content-desc='Send']")
    ))
    send_button.click()
    print("Send button clicked!")
    sleep(5)

    # click and Enter Address (try using a more general locator if the current one fails)
    address_field = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//*[@id="screenshotContainer"]/div[2]/div/div/div/div/div[13]")
    ))
    address_field.click()

    # Wait until it's visible, not just clickable
    address_field.click()  # Focus on the field first
    address_field.clear()  # Clear any existing text
    address_field.send_keys("0xe7Ea7f5ef79B168E01eb527CfcD76d1AADdd4a42")
    print("Address entered!")
    sleep(10)

    # Enter Amount (similarly generalize the locator)
    #amount_field = wait.until(EC.visibility_of_element_located(
        #(By.XPATH, "//android.widget.EditText[contains(@resource-id, 'amount')]")
   # ))  # Wait until it's visible
    #amount_field.click()  # Focus on the field first
    #amount_field.clear()  # Clear any existing text
    #amount_field.send_keys("15")
    #print("Amount entered!")
    #sleep(10)

    # Click on transfer button
    #transfer_button = wait.until(EC.element_to_be_clickable(
       # (By.XPATH, "(//android.view.View[@content-desc='Send'])[2]")
    #))
    #transfer_button.click()
    #print("Transfer button clicked!")
    #sleep(10)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Quit the driver to end the session
    driver.quit()
    print("Test completed and driver session ended.")

import allure
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Define the Appium server URL
appium_server_url = "http://192.168.0.228:4723/wd/hub"

# Define the options
options = UiAutomator2Options()
options.platform_name = "Android"
options.platform_version = "14.0"
options.device_name = "RMX2202L1"
options.app_package = "io.floxypay.fxy.twa"
options.app_activity = "com.example.floxy_pay.MainActivity"
options.no_reset = True
options.full_reset = False
options.ignore_hidden_api_policy_error = True

@allure.feature("App Launch and Interaction")
@allure.story("Open app and interact with elements for login and navigation")
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Remote(command_executor=appium_server_url, options=options)
    yield driver
    driver.quit()
    print("Driver session ended.")

@allure.step("Click button {description}")
def click_button(driver, locator, description):
    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator))
    button.click()
    allure.attach(driver.get_screenshot_as_png(), name=f"{description}", attachment_type=allure.attachment_type.PNG)
    print(f"{description} clicked")

def test_app_interaction(driver):
    with allure.step("Launch the app"):
        print("App has been launched on the device!")
        sleep(5)

    # Click the first button 3 times
    for i in range(2):
        click_button(driver, (By.CLASS_NAME, "android.widget.Button"), f"Button click {i + 1}")
        sleep(1)

    # Click on "Get Started" button
    click_button(driver, (By.XPATH, "//android.view.View[@content-desc='Get Started']"), "Get Started button")

    # Click on "Continue with Google" button
    click_button(driver, (By.XPATH, "//android.widget.FrameLayout[@resource-id='android:id/content']"
                                    "/android.widget.FrameLayout/android.view.View/android.view.View/"
                                    "android.view.View/android.view.View/android.widget.ImageView[1]"),
                 "Continue with Google button")

    # Click on "Choose Account" button
    click_button(driver, (By.XPATH, "//android.view.View[@resource-id='yDmH0d']/android.view.View[3]"),
                 "Choose Account button")

    sleep(2)

    # Click on "Continue" button
    click_button(driver, (By.XPATH, "//android.widget.Button[@text='Continue']"), "Continue button")

    # Click on "Skip for Now" button
    click_button(driver, (By.XPATH, "//android.widget.Button[@text='Skip for Now']"), "Skip for Now button")
    sleep(5)

    # Enter MPIN by clicking specific XPaths
    with allure.step("Enter MPIN"):
        for i in range(1, 7):  # Assuming MPIN is a 6-digit pin and each button is labeled with the digit 1
            mpin_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f'//android.view.View[@content-desc="{1}"]'))
            )
            mpin_button.click()
            allure.attach(driver.get_screenshot_as_png(), name=f"MPIN digit {i}", attachment_type=allure.attachment_type.PNG)
            print(f"MPIN digit {i} entered")
            sleep(1)

    print("App is logged in")

    # Click on send button
    click_button(driver, (By.XPATH, "//android.widget.ImageView[@content-desc='Send']"), "Send button")
    sleep(5)

    # You can uncomment and configure the following sections to enter the address and amount if needed

    # # Enter Address
    # with allure.step("Enter Address"):
    #     address_field = WebDriverWait(driver, 20).until(
    #         EC.visibility_of_element_located((By.XPATH, "//android.widget.EditText[contains(@resource-id, 'address')]"))
    #     )
    #     address_field.click()
    #     address_field.clear()
    #     address_field.send_keys("0xe7Ea7f5ef79B168E01eb527CfcD76d1AADdd4a42")
    #     allure.attach(driver.get_screenshot_as_png(), name="Address entered", attachment_type=allure.attachment_type.PNG)
    #     print("Address entered!")

    # # Enter Amount
    # with allure.step("Enter Amount"):
    #     amount_field = WebDriverWait(driver, 20).until(
    #         EC.visibility_of_element_located((By.XPATH, "//android.widget.EditText[contains(@resource-id, 'amount')]"))
    #     )
    #     amount_field.click()
    #     amount_field.clear()
    #     amount_field.send_keys("15")
    #     allure.attach(driver.get_screenshot_as_png(), name="Amount entered", attachment_type=allure.attachment_type.PNG)
    #     print("Amount entered!")

    # # Click on Transfer button
    # click_button(driver, (By.XPATH, "(//android.view.View[@content-desc='Send'])[2]"), "Transfer button")
    # sleep(10)

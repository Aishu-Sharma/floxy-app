import time
import allure
import pytest
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

def test_app_interaction(driver):
    with allure.step("Launch the app"):
        print("App has been launched on the device!")
        sleep(2)

    # Enter MPIN by clicking specific XPaths
    with allure.step("Enter MPIN"):
        for i in range(1, 7):  # Assuming MPIN is a 6-digit pin and each button is labeled with the digit 1
            mpin_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, f'//android.view.View[@content-desc="{1}"]'))
            )
            mpin_button.click()
            allure.attach(driver.get_screenshot_as_png(), name=f"MPIN digit {i}", attachment_type=allure.attachment_type.PNG)
            print(f"MPIN digit {i} entered")
            sleep(5)

    print("App is logged in")

    # Updated XPath to target "MATIC Polygon"
    xpath = '//android.widget.ImageView[@content-desc="MATIC Polygon 0% 2.9235 MATIC"]'

    try:
        Scroll horizontally to locate and click the element
    scroll_horizontally_and_click_image(driver, xpath, "MATIC")
     except Exception as e:
    #print(f"Failed to locate or click the MATIC Polygon element:")
        # raise

    #Click on "Send" button
    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']

    start_x = width * 0.8  # Start from 80% of the screen width (from the right side)
    end_x = width * 0.1  # End at 20% of the screen width (toward the left side)
    print(f"width {width}, height {height}", start_x, end_x)
    driver.swipe(995, 1757, 143, 1757, 2)  # Swipe from right to left
    print(f"Scrolling horizontally to find ")
    time.sleep(2)
     element = driver.find_element(By.XPATH, xpath)
     # if element.is_displayed():
     element.click()
     allure.attach(driver.get_screenshot_as_png(), name=f"matic' Click Success", attachment_type=allure.attachment_type.PNG)
     print(f"Image with description 'matic' clicked successfully!")
     time.sleep(5)
     try:
         sendbtn = driver.find_element(By.XPATH, '//android.widget.ImageView[@content-desc="SEND"]')
         sendbtn.click()
         click_button(driver, (By.XPATH, '//android.widget.ImageView[@content-desc="SEND"]'), "Send button")
     except Exception as e:
         print(f"Failed to locate or click the SEND button: {str(e)}")
         raise

    # # Enter recipient address
    # with allure.step("Enter Recipient Address"):
    #     address_field = WebDriverWait(driver, 1).until(
    #         EC.visibility_of_element_located((By.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[2]/android.widget.EditText'))
    #     )
    #     address_field.click()
    #     address_field.clear()
    #     address_field.send_keys("0xe7Ea7f5ef79B168E01eb527CfcD76d1AADdd4a42")
    #     allure.attach(driver.get_screenshot_as_png(), name="Recipient Address", attachment_type=allure.attachment_type.PNG)
    #     print("Recipient address entered!")
    #
    # # Enter amount
    # with allure.step("Enter Amount"):
    #     amount_field = WebDriverWait(driver, 5).until(
    #         EC.visibility_of_element_located((By.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[3]/android.widget.EditText'))
    #     )
    #     amount_field.click()
    #     amount_field.clear()
    #     amount_field.send_keys("0.01")
    #     allure.attach(driver.get_screenshot_as_png(), name="Transfer Amount", attachment_type=allure.attachment_type.PNG)
    #     print("Transfer amount entered!")

    # Click on "Send" button
    #click_button(driver, (By.XPATH, '(//android.view.View[@content-desc="Send"])[2]'), "Transfer button")

    # Click on "Confirm" button
    #click_button(driver, (By.XPATH, '//android.view.View[@content-desc="CONFIRM"]'), "Confirm button")

    # Enter MPIN
    # with allure.step("Enter MPIN"):
    #     for i in range(1, 7):  # Assuming MPIN is a 6-digit pin where each button is labeled with '1'
    #         mpin_button = WebDriverWait(driver, 5).until(
    #             EC.element_to_be_clickable((By.XPATH, f'//android.view.View[@content-desc="{1}"]'))
    #         )
    #         mpin_button.click()
    #         allure.attach(driver.get_screenshot_as_png(), name=f"MPIN digit {i}", attachment_type=allure.attachment_type.PNG)
    #         print(f"MPIN digit {i} entered")
    #         sleep(1)
    #
    # print("MATIC is transferred successfully!")
    # sleep(2)



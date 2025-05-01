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
options.app_package = "io.floxypaywallet.fxy.twa"
options.app_activity = "io.floxypaywallet.fxy.twa.MainActivity"
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

def test_stake(driver):
    with allure.step("Click Stake"):
        stake_button = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//android.widget.ImageView[@content-desc='Stake']"))
        )
        stake_button.click()
        print("Stake button click success")
        allure.attach(driver.get_screenshot_as_png(), name="Stake Button Clicked", attachment_type=allure.attachment_type.PNG)
        sleep(3)





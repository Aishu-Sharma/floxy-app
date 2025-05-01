import os
import pytest
import allure
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# ---------------------------------
# CONFIGURATION FILE
# ---------------------------------
class Config:
    APP_PACKAGE = "io.floxypay.fxy.twa"
    APP_ACTIVITY = "com.example.floxy_pay.MainActivity"
    PLATFORM_NAME = "Android"
    PLATFORM_VERSION = "14.0"
    DEVICE_NAME = "RMX2202L1"
    APPIUM_SERVER_URL = "http://0.0.0.0:4723/wd/hub"
    NO_RESET = True
    FULL_RESET = False
    IGNORE_HIDDEN_API_POLICY_ERROR = True


# ---------------------------------
# DRIVER FIXTURE
# ---------------------------------
@pytest.fixture(scope="function")
def driver():
    options = UiAutomator2Options()
    options.platform_name = Config.PLATFORM_NAME
    options.platform_version = Config.PLATFORM_VERSION
    options.device_name = Config.DEVICE_NAME
    options.app_package = Config.APP_PACKAGE
    options.app_activity = Config.APP_ACTIVITY
    options.no_reset = Config.NO_RESET
    options.full_reset = Config.FULL_RESET
    options.ignore_hidden_api_policy_error = Config.IGNORE_HIDDEN_API_POLICY_ERROR

    driver = webdriver.Remote(command_executor=Config.APPIUM_SERVER_URL, options=options)
    yield driver
    driver.quit()


# ---------------------------------
# UTILITY FUNCTIONS
# ---------------------------------
@allure.step("Click button {description}")
def click_button(driver, locator, description):
    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator))
    button.click()
    allure.attach(driver.get_screenshot_as_png(), name=f"{description}", attachment_type=allure.attachment_type.PNG)
    print(f"{description} clicked")


@allure.step("Enter text in field {description}")
def enter_text(driver, locator, text, description):
    field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(locator))
    field.click()
    field.clear()
    field.send_keys(text)
    allure.attach(driver.get_screenshot_as_png(), name=f"{description}", attachment_type=allure.attachment_type.PNG)
    print(f"{description} entered: {text}")


# ---------------------------------
# PAGE OBJECTS
# ---------------------------------
class LoginPage:
    GET_STARTED_BTN = (By.XPATH, "//android.view.View[@content-desc='Get Started']")
    CONTINUE_WITH_GOOGLE_BTN = (
        By.XPATH,
        "//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView[1]",
    )
    CHOOSE_ACCOUNT_BTN = (By.XPATH, "//android.view.View[@resource-id='yDmH0d']/android.view.View[3]")
    CONTINUE_BTN = (By.XPATH, "//android.widget.Button[@text='Continue']")
    SKIP_NOW_BTN = (By.XPATH, "//android.widget.Button[@text='Skip for Now']")
    MPIN_DIGIT = lambda digit: (By.XPATH, f"//android.view.View[@content-desc='{digit}']")


class TransferPage:
    SEND_BTN = (By.XPATH, "//android.widget.ImageView[@content-desc='Send']")
    ADDRESS_FIELD = (
        By.XPATH,
        "//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[2]/android.widget.EditText",
    )
    AMOUNT_FIELD = (
        By.XPATH,
        "//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[3]/android.widget.EditText",
    )
    CONFIRM_BTN = (By.XPATH, "//android.view.View[@content-desc='CONFIRM']")


# ---------------------------------
# TEST CASES
# ---------------------------------
@allure.feature("App Launch and Interaction")
@allure.story("Test login and transfer flow")
def test_login_and_transfer(driver):
    with allure.step("Launch the app"):
        print("App has been launched on the device!")
        sleep(5)

    # Login Flow
    click_button(driver, LoginPage.GET_STARTED_BTN, "Get Started")
    click_button(driver, LoginPage.CONTINUE_WITH_GOOGLE_BTN, "Continue with Google")
    click_button(driver, LoginPage.CHOOSE_ACCOUNT_BTN, "Choose Account")
    click_button(driver, LoginPage.CONTINUE_BTN, "Continue")
    click_button(driver, LoginPage.SKIP_NOW_BTN, "Skip for Now")

    # Enter MPIN
    with allure.step("Enter MPIN"):
        for i in range(1, 7):
            click_button(driver, LoginPage.MPIN_DIGIT(1), f"MPIN digit {i}")

    # Transfer Flow
    click_button(driver, TransferPage.SEND_BTN, "Send button")
    enter_text(driver, TransferPage.ADDRESS_FIELD, "0xe7Ea7f5ef79B168E01eb527CfcD76d1AADdd4a42", "Recipient Address")
    enter_text(driver, TransferPage.AMOUNT_FIELD, "15", "Transfer Amount")
    click_button(driver, TransferPage.CONFIRM_BTN, "Confirm Transfer")

    # Confirm MPINsws
    with allure.step("Confirm MPIN"):
        for i in range(1, 7):
            click_button(driver, LoginPage.MPIN_DIGIT(1), f"Confirm MPIN digit {i}")
    print("Transfer process completed!")

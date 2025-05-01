import pytest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import allure

@pytest.fixture
def driver():
    """Set up the Appium driver"""
    desired_caps = {
        "platformName": "Android",
        "platformVersion": "10",  # Update as per your device
        "deviceName": "Android Emulator",  # Replace with your device name
        "app": "path/to/your/app.apk",  # Update with the path to your app
        "automationName": "UiAutomator2"
    }

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    yield driver
    driver.quit()

def horizontal_swipe(driver, start_x, end_x, y):
    """Perform a horizontal swipe action"""
    action = TouchAction(driver)
    action.press(x=start_x, y=y).wait(ms=200).move_to(x=end_x, y=y).release().perform()

def scroll_horizontally_and_click_image(driver, xpath, description):
    """Scroll horizontally to find and click an element"""
    max_swipes = 5
    for swipe in range(max_swipes):
        try:
            element = driver.find_element(By.XPATH, xpath)
            element.click()
            print(f"{description} element clicked successfully!")
            return
        except NoSuchElementException:
            print(f"{description} element not found. Attempting swipe {swipe + 1}...")
            horizontal_swipe(driver, start_x=800, end_x=200, y=400)
    raise NoSuchElementException(f"Failed to locate or click the {description} element after {max_swipes} swipes.")

def test_app_interaction(driver):
    """Test the app interaction"""
    print("App has been launched on the device!")
    sleep(2)

    # Step 1: Enter MPIN
    with allure.step("Enter MPIN"):
        for i in range(1, 7):  # Assuming MPIN is a 6-digit PIN
            mpin_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//android.view.View[@content-desc="1"]'))
            )
            mpin_button.click()
            allure.attach(driver.get_screenshot_as_png(), name=f"MPIN digit {i}",
                          attachment_type=allure.attachment_type.PNG)
            print(f"MPIN digit {i} entered")
            sleep(1)

    print("App is logged in")

    # Step 2: Locate and click the MATIC Polygon element
    xpath = '//android.widget.ImageView[contains(@content-desc, "MATIC Polygon")]'
    try:
        scroll_horizontally_and_click_image(driver, xpath, "MATIC")
    except NoSuchElementException as e:
        allure.attach(driver.get_screenshot_as_png(), name="Final attempt", attachment_type=allure.attachment_type.PNG)
        print(str(e))
        raise

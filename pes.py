from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

TIMEOUT = 25

def check_in():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")

    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.get(
        "https://hr.globalservicing.com/globalservicingcom/zp#home/dashboard")
    time.sleep(2)
    signinButton = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="iamUrlSigninBtn"]')))
    signinButton.click()
    time.sleep(0.4)

    emailInput = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="login_id"]')))
    emailInput.send_keys("rkorgaokar@globalservicing.com")

    nextButton = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="nextbtn"]')))
    nextButton.click()
    time.sleep(0.4)

    current_url = driver.current_url
    if current_url == "https://hr.globalservicing.com/globalservicingcom/zp#home/dashboard":
        print("Already checked in")
        driver.quit()
        return

    if current_url.startswith("https://accounts.zoho.com/signin?servicename"):
        time.sleep(0.4)
        passwordInput = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@id="password"]')))
        passwordInput.send_keys("Inject12")
        time.sleep(0.4)
        nextButton.click()
        time.sleep(0.4)
    
        otp = input('[Required] - Please enter OTP: ')
        passwordInput = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@id="mfa_otp"]')))
        passwordInput.send_keys(otp)
        time.sleep(0.4)
        nextButton.click()
        time.sleep(2)

        trustButton = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@id="signin_flow"]/div[7]/button[1]')))
        trustButton.click()
        time.sleep(5)

    current_url = driver.current_url
    if current_url.startswith("https://hr.globalservicing.com/globalservicingcom/zp"):
        time.sleep(60)
        checkButton = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@id="ZPD_Top_Att_Stat"]')))
        if checkButton.text == "Check-In":
            checkButton.click()
        elif checkButton.text == "Check-Out":
            checkButton.click()
        else :
            print("Already checked in")

        """ checkin_button = driver.find_element_by_xpath(
            "//button[contains(text(), 'Check-In')]")
        checkin_button.click() """
        """ driver.quit() """


while True:
    current_time = time.strftime("%H:%M:%S")
    weekday = time.strftime("%A")
    if weekday != "Saturday" and weekday != "Sunday":
        check_in()
    time.sleep(60)

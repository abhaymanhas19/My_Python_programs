import os
import ssl
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_py import binary_path 
# Check and set up SSL if missing
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode
chrome_options.add_argument("--disable-infobars")  # Disable info bars
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--disable-gpu")  # Applicable for Windows OS only
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model, for Linux
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/112.0.0.0 Safari/537.36")

browser = None  # Initialize the browser variable to None

try:
    # Directly use system-installed ChromeDriver
    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH", "C:\\ProgramData\\chocolatey\\bin\\chromedriver.exe")
    service = Service(executable_path=binary_path)

    # Initialize the WebDriver
    browser = webdriver.Chrome(service=service, options=chrome_options)

    # Open Binance homepage
    url = "https://www.binance.com"
    print(f"Opening {url}...")
    browser.get(url)

    # Wait for the page to load
    time.sleep(5)  # This can be replaced with WebDriverWait for better handling

    print("Binance homepage loaded successfully.")

    # Click the login button
    wait = WebDriverWait(browser, 15)
    login_button_xpath = "//*[@id='toLoginPage']"
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath)))
    login_button.click()
    print("Login button clicked.")

    # Enter email in the email field
    email_field_xpath = "//*[@name='username']"
    email_field = wait.until(EC.visibility_of_element_located((By.XPATH, email_field_xpath)))
    email_field.send_keys("sajdaskjtesting@gmail.com")
    print("Email entered in the email field.")
    

    # Click the submit button
    submit_button_xpath = "//*[@data-e2e='btn-accounts-form-submit']"
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
    submit_button.click()
    print("Submit button clicked.")
    
    # Wait for reCAPTCHA to load
    print("Waiting for reCAPTCHA to load...")
    if browser.current_url=="https://accounts.binance.com/en/login/password?":
        print("Page redirted to password page")
        
    else:
        try:
            instructions_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bcap-text-message-title2")))
            instructions_text = instructions_element.text
            print(f"Instructions Text: {instructions_text}")
        except Exception as e:
            print("Could not find instructions element:", e)
        
        
        captcha_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bcap-image-table")))
        
        browser.execute_script("arguments[0].scrollIntoView(true);", captcha_container)
        time.sleep(1)   
        
        # Taking Screenshot of captcha
        captcha_screenshot = captcha_container.screenshot_as_png
        
        # Gathering images pin points
        tiles = browser.find_elements(By.CSS_SELECTOR, ".bcap-image-cell-container")
        
        with open("captcha.png", "wb") as f:
            f.write(captcha_screenshot)
        
        files = {
            'file': ('captcha.png', open('captcha.png', 'rb'), 'image/png')
        }
         
        data = {
            'key': "cbe29014ef85544cf12dcc28de593ac8",
            'method': 'post',
            "textinstructions":f"Please Select all images containing with {instructions_text}",
            'json': 1,
            'websiteURL': browser.current_url,
            'websiteKey': 'binance',
        }
        
        response = requests.post("http://2captcha.com/in.php", data=data,files=files)
        resp_json = response.json()

        if resp_json.get("status") == 1:
            captcha_id = resp_json.get("request")
        else:
            raise Exception("Failed to submit captcha")

        # Waiting from captcha request response 
        for _ in range(30):
            time.sleep(5)
            res = requests.get("http://2captcha.com/res.php", params={
                'key': "cbe29014ef85544cf12dcc28de593ac8",
                'action': 'get',
                'id': captcha_id,
                'json': 1
            })
            res_json = res.json()
            if res_json.get("status") == 1:
                solution = res_json.get("request")
                break
            elif res_json.get("status")== 0:
                solution = 0

        if not solution:
            raise Exception("No solution returned by 2Captcha")
        
        # Mapping solution with captcha and marked according to Values 
        
        print("Solution provided by 2Captcha Site :", solution)
        if 
            mapped_values ={key+1:key for key in range(9) }
            for i in solution:
                tiles[mapped_values[int(i)]].click()
                
            verify_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".bcap-verify-button")))
            verify_button.click()
            
            print("Verify button Clicked")
            
        else:
            print("Wrong Solution")


finally:
    # Remove close window function for testing
    browser.quit()
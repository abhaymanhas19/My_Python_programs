import os
import ssl
import time
import zipfile
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_py import binary_path
import multiprocessing 
from random import shuffle
from concurrent.futures import ProcessPoolExecutor

lock = multiprocessing.Lock()

# Check and set up SSL if missing
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

# File paths
emails_file = "python-scripts/emails.txt"
proxy_file = "python-scripts/proxy_list.txt"
failed_emails_file = "failed.txt"
success_emails_file = "success.txt"

# Read emails
try:
    with open(emails_file, "r") as f:
        email_list = [line.strip() for line in f.readlines() if line.strip()]
except FileNotFoundError:
    print(f"The file {emails_file} was not found. Please create it with one email per line.")
    exit()

if not email_list:
    print("No emails found in the file. Exiting.")
    exit()

# Read proxies
try:
    with open(proxy_file, "r") as f:
        proxy_list = [line.strip() for line in f.readlines() if line.strip()]
except FileNotFoundError:
    print(f"The file {proxy_file} was not found. Please create it with proxies in the format"
          f" host:port:username:password.")
    exit()

if not proxy_list:
    print("No proxies found in the file. Exiting.")
    exit()


def save_email_to_file(email, file_name):
    with lock:
        with open(file_name, "a") as file:
            file.write(f"{email}\n")


def get_proxy():
    shuffle(proxy_list)
    _proxy = proxy_list.pop(0)
    proxy_list.append(_proxy)
    return _proxy


def create_proxy_extension(proxy,process_id):
    proxy_host, proxy_port, proxy_username, proxy_password = proxy.split(":")
    # Create a proxy authentication extension dynamically
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        }
    }
    """
    
    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{proxy_host}",
                port: parseInt({proxy_port})
            }},
            bypassList: ["localhost"]
        }}
    }};

    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    chrome.webRequest.onAuthRequired.addListener(
        function(details) {{
            return {{
                authCredentials: {{
                    username: "{proxy_username}",
                    password: "{proxy_password}"
                }}
            }};
        }},
        {{urls: ["<all_urls>"]}},
        ["blocking"]
    );
    """
    
    # Save the files for the extension
    plugin_file = f'proxy_auth_plugin_{process_id}.zip'
    if os.path.exists(plugin_file):
        os.remove(plugin_file)
    if os.path.exists("manifest.json"):
        os.remove("manifest.json")
    if os.path.exists("background.js"):
        os.remove("background.js")
        
    with zipfile.ZipFile(plugin_file, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_file


def create_chrome_browser_with_proxy(proxy,process_id):
    plugin_file = create_proxy_extension(proxy,process_id)
    if not os.path.exists(plugin_file):
        print("Extension zip file creation failed")
        exit(-1)
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_extension(plugin_file)
    chrome_options.add_argument("--disable-infobars")
    # chrome_options.add_argument("--disable-extensions") # Disabling extension will break the authentication
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
     # Initialize ChromeDriver service
    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH", "C:\\ProgramData\\chocolatey\\bin\\chromedriver.exe")
    if os.path.exists("C:\\ProgramData\\chocolatey\\bin\\chromedriver.exe"):
        service = Service("C:\\ProgramData\\chocolatey\\bin\\chromedriver.exe")
    elif os.path.exists(chromedriver_path):
        service = Service(chromedriver_path)
    else:
        service = Service(executable_path=binary_path)
        
    
    browser = webdriver.Chrome(service=service, options=chrome_options)
    return browser

def make_request(email_to_test):
    process_id = os.getpid()
    
    proxy = get_proxy()
    browser = create_chrome_browser_with_proxy(proxy,process_id)

    wait = WebDriverWait(browser, 15)
    url = "https://www.binance.com"
    print(f"Opening {url}...")
    browser.get(url)
    
    print("Binance homepage loaded successfully.")
    
    login_button_xpath = "//*[@id='toLoginPage']"
    browser.save_screenshot(f"debug_screenshot_{process_id}.png")
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath)))
    login_button.click()
    print("Login button clicked.")
    
    
    email_field_xpath = "//*[@name='username']"
    email_field = wait.until(EC.visibility_of_element_located((By.XPATH, email_field_xpath)))
    email_field.send_keys(email_to_test)
    print(f"Email entered in the email field: {email_to_test}")
    
    
    submit_button_xpath = "//*[@data-e2e='btn-accounts-form-submit']"
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
    submit_button.click()
    print("Submit button clicked.")
    
    
    print("Checking for password field or account not found...")
    try:
        password_input_xpath = "//*[@id=\"wrap_app\"]/main/div[2]/div[3]/div/form/div/div[2]/div/input"
        password_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, password_input_xpath)))
        if password_input.is_displayed():
            print("Password input field detected. Saving email to success.txt.")
            save_email_to_file(email_to_test, success_emails_file)
            return 
    except Exception:
        print("Password input field not detected, checking for account not found...")

    try:
        not_found_xpath = "//*[@id=\"wrap_app\"]/main/div[2]/div[2]/div[1]/form/div/div[3]"
        not_found_element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, not_found_xpath)))
        if not_found_element.is_displayed():
            print("Binance account not found. Saving email to failed.txt.")
            save_email_to_file(email_to_test, failed_emails_file)
            return 
            
    except Exception:
        print("Account not found message not detected. Retrying captcha...")
        
    try:
        instructions_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".bcap-text-message-title2")))
        instructions_text = instructions_element.text
        print(f"Instructions Text: {instructions_text}")
        
        captcha_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bcap-image-table")))
        browser.execute_script("arguments[0].scrollIntoView(true);", captcha_container)
        
        captcha_screenshot = captcha_container.screenshot_as_png
        with open(f"captcha_{process_id}.png", "wb") as f:
            f.write(captcha_screenshot)
            print("Saving Captach Secreentshot")
            
            
        tiles = browser.find_elements(By.CSS_SELECTOR, ".bcap-image-cell-container")
        files = {
            'file': (f'captcha_{process_id}.png', open(f'captcha_{process_id}.png', 'rb'), 'image/png')
        }

        data = {
            'key': "cbe29014ef85544cf12dcc28de593ac8",
            'method': 'post',
            "textinstructions": f"Please Select all images containing with {instructions_text}",
            'json': 1,
            'websiteURL': browser.current_url,
            'websiteKey': 'binance',
        }
        try:
        
            response = requests.post("http://2captcha.com/in.php", data=data, files=files)
            resp_json = response.json()

            if resp_json.get("status") == 1:
                captcha_id = resp_json.get("request")
            else:
                raise Exception("Failed to submit captcha")

            # Waiting from captcha request response
            for _ in range(30):
                time.sleep(3)
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
            else:
                raise Exception("No solution returned by 2Captcha")
            
            print("Solution provided by 2Captcha Site:", solution)

            if solution.isdigit():
                mapped_values = {key + 1: key for key in range(9)}
                for i in solution:
                    tiles[mapped_values[int(i)]].click()

                verify_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bcap-verify-button")))
                verify_button.click()
                print("Verify button clicked")
            print(f"Completed Check for Email:{email_to_test}")
        except Exception as e:
            print("An error occurred during captcha processing:", e)
            
        finally:
            time.sleep(5)
            browser.quit()
            
    except Exception as e:
        print(f"Error processing email {email_to_test}: {e}")
        save_email_to_file(email_to_test, failed_emails_file)
    finally:
        time.sleep(5)
        browser.quit()
    return email_to_test

def main():
    number_of_processes = multiprocessing.cpu_count() - 1 
    with ProcessPoolExecutor(max_workers = number_of_processes) as executor:      
        start_time = time.perf_counter()
        result =  executor.map(make_request,[email_list[0]])
        result = list(result)
        print("Tested Emails:", result)
        end_time = time.perf_counter()
    
    print("Time Taken to process email",end_time-start_time)
    

if __name__=="__main__":
    main()

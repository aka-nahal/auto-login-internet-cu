import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
import time
from requests.exceptions import RequestException

# Path to the Edge WebDriver executable
edge_webdriver_path = 'C:\\edgedriver_win64\\msedgedriver.exe'

# Specify the login URL and credentials
login_url = 'http://edge-http.microsoft.com/captiveportal/generate_204'
username = 'your_username' # Enter your UID
password = 'your_password' # Enter Your Internet Password

# Function to perform the login process
def login():
    # Initialize the Edge WebDriver with Service
    service = EdgeService(executable_path=edge_webdriver_path)
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(service=service, options=options)

    try:
        # Navigate to the login URL
        driver.get(login_url)
        
        # Wait for the form element to be present on the page
        form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'form'))
        )
        
        # Find the username and password fields and submit button within the form
        username_field = form.find_element(By.NAME, 'username')
        password_field = form.find_element(By.NAME, 'password')
        submit_button = form.find_element(By.XPATH, '//input[@type="submit"]')
        
        # Fill in the username and password fields
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        # Submit the form
        submit_button.click()
        
        # Wait for the login process to complete (you may need to adjust this time)
        time.sleep(5)  # Adjust as needed
        
        print("Login successful.")
        return driver
    except Exception as e:
        print("An error occurred during login:", e)
        if driver:
            driver.quit()
        return None

# Function to check login status by pinging a website or handling SSL errors
def check_login_status():
    try:
        response = requests.get("https://www.google.com", verify=True)
        if response.status_code == 200:
            print("Login successful. Able to access Google.")
            return True
        else:
            print("Login failed. Unable to access Google.")
            return False
    except RequestException as e:
        print("Error:", e)
        print("Attempting login...")
        return False

# Main loop to continuously check login status and rerun login if necessary
while True:
    if not check_login_status():
        # If login failed or Google is inaccessible, rerun the login process
        driver = login()
        # Check login status again
        if driver and check_login_status():
            # If login successful after rerun, close the browser window
            driver.quit()
    time.sleep(5 * 60 * 60)  # 5 hours interval

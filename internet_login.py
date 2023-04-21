import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# Specify the path to the WebDriver executable
# For example, for Google Chrome
webdriver_path = '/path/to/chromedriver'

# Specify the login URL and credentials
login_url = 'http://172.15.15.1:1000/fgtauth'
username = 'my_username'
password = 'my_password'

# Create a new session and send a GET request to the login URL
session = requests.Session()
response = session.get(login_url)

# Use BeautifulSoup to parse the response and extract the token
soup = BeautifulSoup(response.content, 'html.parser')
token = soup.find('input', {'name': 'token'}).get('value')
login_url_with_token = f'{login_url}?{token}'

# Create a new WebDriver instance and navigate to the login URL with the token
driver = webdriver.Chrome(webdriver_path)
driver.get(login_url_with_token)

# Wait for the page to load and find the login form elements
time.sleep(5)  # Adjust as needed
username_field = driver.find_element_by_name('username')
password_field = driver.find_element_by_name('password')
login_button = driver.find_element_by_xpath('//button[@type="submit"]')

# Fill in the login form and submit it
username_field.send_keys(username)
password_field.send_keys(password)
login_button.click()

# Wait for the login to complete and do something else
time.sleep(10)  # Adjust as needed
# ... do something else here ...

# Close the browser window
driver.quit()

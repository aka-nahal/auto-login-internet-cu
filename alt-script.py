import requests
import time
import webbrowser
import os
import logging
from datetime import datetime

# Set up logging
log_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = datetime.now().strftime('auth-%Y-%m-%d.log')
log_path = os.path.join(log_dir, log_filename)

logging.basicConfig(filename=log_path, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define login function
def login(username, password):
    # Set up session
    session = requests.Session()

    # Get login page
    login_url = "http://172.15.15.1:1000/fgtauth"
    login_page = session.get(login_url)

    # Extract token
    token_start = login_page.text.find("name='token' value='") + len("name='token' value='")
    token_end = login_page.text.find("'", token_start)
    token = login_page.text[token_start:token_end]

    # Login with token and credentials
    data = {
        "username": username,
        "password": password,
        "token": token
    }

    response = session.post(login_url, data=data)

    # Check if login was successful
    if "Login Successful" in response.text:
        logging.info(f"{datetime.now()} - Login successful for user {username}")
        return True
    else:
        logging.error(f"{datetime.now()} - Login failed for user {username}")
        return False

# Main loop
while True:
    try:
        # Check internet connection by pinging Google
        response = requests.get("https://www.google.com")
        if response.status_code == 200:
            time.sleep(10)
            continue

        # If internet connection is not available, open default browser and attempt login
        webbrowser.open("http://172.15.15.1:1000")
        username = input("Enter your UIMS username: ")
        password = input("Enter your UIMS password: ")
        if login(username, password):
            webbrowser.close()
        else:
            time.sleep(10)

    except requests.exceptions.ConnectionError:
        # If internet connection is lost during the loop, wait and try again
        time.sleep(10)
        continue

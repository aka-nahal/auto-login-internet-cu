import requests
import time

login_url = "http://172.15.15.1:1000/fgtauth"
username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"

while True:
    try:
        # Get the token number from the login page
        response = requests.get(login_url)
        token = response.url.split("?")[-1]

        # Prepare the form data for the login request
        data = {
            "4Tredir": "/fgtauth/",
            "magic": token,
            "username": username,
            "password": password,
            "submit": "Login",
        }

        # Send the login request
        response = requests.post(login_url, data=data)

        # Check if login was successful
        if "You have successfully logged in." in response.text:
            print("Login successful.")
        else:
            print("Login failed.")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    # Wait for 5 hours before attempting to login again
    time.sleep(5 * 60 * 60)

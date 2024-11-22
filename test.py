import requests
import json

# API endpoint
url = 'https://mapsbackend-2795be8adb50.herokuapp.com/api/check'

# Data to send in the POST request (replace with actual user credentials)
data = {
    'username': 'Aum',
    'password': 'Sept2020'
}

# Send POST request with JSON data
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    result = response.json()
    if result.get('exists'):
        print("Login successful!")
    else:
        print("Login failed:", result.get('message'))
else:
    print(f"Error: {response.status_code}, {response.text}")

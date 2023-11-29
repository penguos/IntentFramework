import requests
import json

# Set the WiFi network to either 'WiFi_Home' or 'WiFi_Uni'
wifi = 'WiFi_Home'
hostip = '192.168.1.2' if wifi == 'WiFi_Home' else '192.168.1.8'

# Define the URL for the Intent API
url = f"http://{hostip}:8082/Intent/Quality_Change/1080X720"

# Parameters for the request
parms = {
    'content_provider': 'YouTube',
    'resolution': '3840x2160',
    'path': '1'
}

# Headers for the request
headers = {
    'User-agent': 'ip config on 10.0.2.1',
}

print(f"Ready to connect to {url}")

# Making a GET request to the server
response = requests.get(url, params=parms, headers=headers)

print('Response from GET request:', response)

# Uncomment below lines to print the response text and parse JSON if needed
# text = response.text
# print(text)
# print(json.loads(text))

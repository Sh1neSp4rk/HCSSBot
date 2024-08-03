import requests
import os

url = "https://api.hcssapps.com/identity/connect/token"

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
grant_type = os.getenv('GRANT_TYPE')
scope = os.getenv('SCOPE')

payload = {
  "client_id": client_id,
  "client_secret": client_secret,
  "grant_type": grant_type,
  "scope": scope,
}

headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.post(url, data=payload, headers=headers)

data = response.json()
print(data)
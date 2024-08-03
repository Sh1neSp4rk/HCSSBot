import requests

url = "https://api.hcssapps.com/identity/connect/token"

payload = {
  "client_id": "string",
  "client_secret": "string",
  "grant_type": "string",
  "scope": "string",
  "code": "string",
  "redirect_uri": "string"
}

headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.post(url, data=payload, headers=headers)

data = response.json()
print(data)
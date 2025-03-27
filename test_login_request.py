import requests

def login():
    url = "http://localhost:8000/login"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "",
        "username": "admin@example.com",
        "password": "admin",
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    response = requests.post(url, headers=headers, data=data)
    print("Status code:", response.status_code)
    print("Response:", response.text)

login()

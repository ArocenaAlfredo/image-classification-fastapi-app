from typing import Optional

import requests
from locust import HttpUser, between, task

API_BASE_URL = "http://localhost:8000"


def login(username: str, password: str) -> Optional[str]:
    """This function calls the login endpoint of the API to authenticate the user and get a token.

    Args:
        username (str): email of the user
        password (str): password of the user

    Returns:
        Optional[str]: token if login is successful, None otherwise
    """
    # TODO: Implement the login function
    # 1 - make a request to the login endpoint
    # 2 - check if the response status code is 200
    # 3 - if it is, return the access_token
    # 4 - if it is not, return None
    url = f"{API_BASE_URL}/login"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return None


class APIUser(HttpUser):
    wait_time = between(1, 5)

    # Put your stress tests here.
    # See https://docs.locust.io/en/stable/writing-a-locustfile.html for help.
    # TODO
    # raise NotImplementedError
    @task(1)
    def test_index(self):
        """Stress test for the 'index' endpoint."""
        self.client.get("/")
    @task(3)
    def test_predict(self):
        """Stress test for the 'predict' endpoint."""
        token = login("admin@example.com", "admin")
        if not token:
            print("Login failed, skipping test_predict.")
            return
        
        headers = {"Authorization": f"Bearer {token}"}
        with open("dog.jpeg", "rb") as file:
            files = {"file": (file.name, file.read(), "image/jpeg")}
            self.client.post("/model/predict", headers=headers, files=files)
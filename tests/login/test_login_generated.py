import requests

import pytest

import os

from dotenv import load_dotenv



load_dotenv()  # Load environment variables from .env

BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')



def get_endpoint_url(path):

    """Helper to get the full endpoint URL from BASE_URL and a path (e.g. '/login')."""

    return f'{BASE_URL.rstrip('/')}/{path.lstrip('/')}';



# The 'access_token' fixture is provided by conftest.py and reads sensitive values from your .env file.

# Do NOT store secrets in source code. Use a .env file (not committed to git) for sensitive info.

# All test functions below require 'access_token' as a parameter.

# Here is a Python pytest test function using the requests library:
# 
# ```python
import pytest
import requests
import json
# 
def test_login_with_valid_credentials(access_token):
    # Construct the endpoint URL
    endpoint = get_endpoint_url('/login')

    # Define the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the request body
    body = {
        'username': 'valid_username',
        'password': 'valid_password'
    }
# 
    # Send the POST request
    response = requests.post(endpoint, headers=headers, data=json.dumps(body))
# 
    # Assert that the status code is 200
    assert response.status_code == 200, f'Expected status code 200, but got {response.status_code}'
# 
    # Assert that the response body contains the expected content
    response_body = response.json()
    assert 'username' in response_body, 'Response body does not contain username'
    assert response_body['username'] == 'valid_username', f"Expected username 'valid_username', but got {response_body['username']}"
# ```
# 
# This test function sends a POST request to the '/login' endpoint with a valid username and password in the request body and a valid access token in the Authorization header. It then checks that the status code of the response is 200 and that the response body contains the expected username.

# Here is a Python pytest test function using the requests library:
# 
# ```python
import pytest
import requests
# 
def test_successful_login(access_token):
    # Construct the full endpoint URL
    endpoint_url = get_endpoint_url('/login')

    # Define the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the body
    body = {
        'username': 'testuser',
        'password': 'testpassword'
    }
# 
    # Send the POST request
    response = requests.post(endpoint_url, headers=headers, json=body)
# 
    # Assert that the response status code is 200
    assert response.status_code == 200
# ```
# 
# This test function sends a POST request to the '/login' endpoint with a valid access token in the Authorization header and a JSON body containing a username and password. It then checks if the response status code is 200, indicating a successful login.
# 
# Please replace 'testuser' and 'testpassword' with valid credentials for your application.

# Here is a Python pytest test function using the requests library:
# 
# ```python
import pytest
import requests
# 
def test_login_invalid_credentials(access_token):
    # Construct the full endpoint URL
    endpoint_url = get_endpoint_url('/login')

    # Define the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the invalid credentials
    invalid_credentials = {
        'username': 'invalid_username',
        'password': 'invalid_password'
    }
# 
    # Send a POST request
    response = requests.post(endpoint_url, headers=headers, json=invalid_credentials)
# 
    # Assert that the status code is 401 Unauthorized
    assert response.status_code == 401, f'Expected status code 401, but got {response.status_code}'
# ```
# 
# This test function sends a POST request to the '/login' endpoint with invalid credentials and checks if the API returns a 401 Unauthorized response. The 'access_token' fixture is used in the Authorization header. The full endpoint URL is constructed using the 'get_endpoint_url' helper function.

# Here is a Python pytest test function using the requests library:
# 
# ```python
import pytest
import requests
# 
def test_empty_email_or_password_field(access_token):
    # Construct the full endpoint URL
    endpoint_url = get_endpoint_url('/login')

    # Define the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the payloads
    payloads = [
        {"username": "", "password": "valid_password"},
        {"username": "valid_username", "password": ""}
    ]
# 
    # Iterate over payloads and send requests
    for payload in payloads:
        response = requests.post(endpoint_url, headers=headers, json=payload)
# 
        # Assert that the status code is 401 (Unauthorized)
        assert response.status_code == 401, f"For payload {payload}, expected status code 401 but got {response.status_code}"
# ```
# 
# This test function constructs the full endpoint URL using the helper function `get_endpoint_url(path)`. It then defines the headers and the payloads for the requests. The payloads are designed to test the scenario where either the email or the password field is empty. The function then sends a POST request to the '/login' endpoint for each payload and asserts that the status code of the response is 401 (Unauthorized).

# Here is a Python pytest test function that uses the requests library to test if the API handles special characters in the email and password fields:
# 
# ```python
import pytest
import requests
import json
# 
def test_special_characters_in_login(access_token):
    # Construct the endpoint URL
    url = get_endpoint_url('/login')

    # Define the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the payload with special characters in username and password
    payload = {
        'username': 'test!@#$%^&*()',
        'password': 'pass!@#$%^&*()'
    }
# 
    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
# 
    # Assert that the response status code is 200 (Login successful)
    assert response.status_code == 200, f'Expected status code 200, but got {response.status_code}'
# ```
# 
# This test function sends a POST request to the '/login' endpoint with a payload that contains special characters in the 'username' and 'password' fields. It then asserts that the response status code is 200, indicating that the login was successful. If the status code is not 200, the test will fail and print a message indicating the actual status code received.

# Here is a Python pytest test function using the requests library:
# 
# ```python
import pytest
import requests
import json
# 
def test_excessively_long_inputs(access_token):
    # Construct the endpoint URL
    endpoint_url = get_endpoint_url('/login')

    # Define excessively long email and password
    excessively_long_email = 'a' * 1024
    excessively_long_password = 'b' * 1024
# 
    # Define the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the payload
    payload = {
        'username': excessively_long_email,
        'password': excessively_long_password
    }
# 
    # Send the POST request
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(payload))
# 
    # Assert that the response status code is as expected (401 Unauthorized)
    assert response.status_code == 401, f'Expected status code 401, but got {response.status_code}'
# ```
# 
# This test function sends a POST request to the '/login' endpoint with excessively long email and password inputs. It expects the API to return a 401 Unauthorized status code, indicating that the API correctly handles excessively long inputs by rejecting them.

# Here is a Python pytest test function that tests if the API handles SQL injection attacks in the email and password fields:
# 
# ```python
import pytest
import requests
import json
# 
def test_sql_injection(access_token):
    # Define SQL injection attack strings
    sql_injection_strings = [
        "admin' --",
        "admin' #",
        "admin'/*",
        "' or 1=1--",
        "' or 1=1#",
        "' or 1=1/*",
        "') or '1'='1--",
        "') or ('1'='1--",
    ]

    # Iterate over each SQL injection string
    for s in sql_injection_strings:
        # Construct the payload with the SQL injection string
        payload = {
            "username": s,
            "password": s
        }
# 
        # Get the endpoint URL
        url = get_endpoint_url('/login')
# 
        # Define the headers
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
# 
        # Make the POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload))
# 
        # Assert that the response status code is 401 (Unauthorized)
        assert response.status_code == 401, f"SQL Injection attack succeeded with string: {s}"
# ```
# 
# This test function iterates over a list of common SQL injection attack strings, and for each string, it constructs a payload where both the username and password are the SQL injection string. It then makes a POST request to the '/login' endpoint with this payload, and asserts that the response status code is 401 (Unauthorized). If the response status code is not 401, it means that the SQL injection attack succeeded, and the test fails.

# Here is a Python pytest test function that uses the requests library to test if the API handles multiple login attempts with the same credentials:
# 
# ```python
import pytest
import requests
# 
def test_multiple_login_attempts_with_same_credentials(access_token):
    url = get_endpoint_url('/login')
    headers = {'Authorization': f'Bearer {access_token}'}
    credentials = {'username': 'testuser', 'password': 'testpassword'}

    # First login attempt
    response1 = requests.post(url, headers=headers, json=credentials)
    assert response1.status_code == 200, "First login attempt failed"
# 
    # Second login attempt
    response2 = requests.post(url, headers=headers, json=credentials)
    assert response2.status_code == 200, "Second login attempt failed"
# ```
# 
# This test function first constructs the full endpoint URL using the helper function `get_endpoint_url()`. It then sets up the Authorization header using the provided `access_token`. The test user's credentials are defined in the `credentials` dictionary.
# 
# The test function then makes two POST requests to the /login endpoint using the same credentials. It asserts that the status code of both responses is 200, indicating that both login attempts were successful. If the API does not handle multiple login attempts with the same credentials correctly, one or both of these assertions will fail, causing the test to fail.

# Here is a Python pytest test function using the requests library:
# 
# ```python
import pytest
import requests
# 
def test_multiple_login_attempts(access_token):
    # Define the endpoint URL
    url = get_endpoint_url('/login')

    # Define the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the list of credentials for multiple login attempts
    credentials = [
        {'username': 'user1', 'password': 'pass1'},
        {'username': 'user2', 'password': 'pass2'},
        {'username': 'user3', 'password': 'pass3'},
    ]
# 
    # Iterate over the credentials and make a POST request for each
    for creds in credentials:
        response = requests.post(url, headers=headers, json=creds)
# 
        # Assert that the response status code is 200 (Login successful)
        assert response.status_code == 200, f"Failed to login with credentials: {creds}"
# ```
# 
# This test function will attempt to login with three different sets of credentials. For each attempt, it will send a POST request to the '/login' endpoint with the given credentials in the request body. It will then assert that the response status code is 200, indicating that the login was successful. If the status code is not 200, the test will fail and print a message indicating which set of credentials caused the failure.

# Here is a Python pytest test function using the requests library for the given scenario:
# 
# ```python
import pytest
import requests
from concurrent.futures import ThreadPoolExecutor
# 
def test_simultaneous_login(access_token):
    # Define the login details
    login_details = {
        "username": "test_user",
        "password": "test_password"
    }

    # Define the headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
# 
    # Define the endpoint URL
    endpoint_url = get_endpoint_url('/login')
# 
    # Define a function to perform a login attempt
def login_attempt(access_token):
        response = requests.post(endpoint_url, headers=headers, json=login_details)
        assert response.status_code == 200, "Login failed"

    # Perform simultaneous login attempts from different devices
    with ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(10):
            executor.submit(login_attempt)
# ```
# 
# This test function simulates 10 simultaneous login attempts from different devices by using a ThreadPoolExecutor to run the login_attempt function in parallel. The login_attempt function sends a POST request to the '/login' endpoint with the provided login details and checks that the response status code is 200, indicating a successful login. If the status code is not 200, the test fails with the message "Login failed".
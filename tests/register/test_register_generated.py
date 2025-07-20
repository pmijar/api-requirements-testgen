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
def test_user_registration(access_token):
    # Construct the endpoint URL
    endpoint_url = get_endpoint_url('/register')

    # Define the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the payload
    payload = {
        'email': 'testuser@example.com',
        'password': 'testpassword'
    }
# 
    # Send the POST request
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(payload))
# 
    # Assert that the status code is 201 (Registration successful)
    assert response.status_code == 201, f'Expected status code 201, but got {response.status_code}'
# 
    # Assert that the response body contains the expected values
    response_body = response.json()
    assert 'email' in response_body, 'Response body does not contain email'
    assert response_body['email'] == payload['email'], f"Expected email '{payload['email']}', but got '{response_body['email']}'"
# ```
# 
# This test function sends a POST request to the '/register' endpoint with the required email and password in the request body. It then checks that the response status code is 201 (indicating successful registration) and that the response body contains the expected email.
# 
# Please note that the test scenario mentioned testing with full name, email address, and password, but the OpenAPI spec only includes fields for email and password. Therefore, the test function only includes these two fields in the request body. If the API actually requires a full name for registration, you would need to update the OpenAPI spec and the test function accordingly.

# Here is a Python pytest test function using the requests library:
# 
# ```python
import pytest
import requests
import json
# 
def test_duplicate_registration(access_token):
    # Construct the endpoint URL
    endpoint_url = get_endpoint_url('/register')

    # Define the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the payload
    payload = {
        'email': 'test@example.com',
        'password': 'testpassword'
    }
# 
    # Send the first POST request
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(payload))
    assert response.status_code == 201, 'First registration should be successful'
# 
    # Send the second POST request with the same email
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(payload))
    assert response.status_code == 400, 'Duplicate registration should be rejected'
# ```
# 
# This test function first sends a POST request to the '/register' endpoint to register a user with a specific email and password. It then sends a second POST request with the same email and password. The test asserts that the first registration should be successful (HTTP status code 201) and the second registration should be rejected (HTTP status code 400).

# Here is a Python pytest test function using the requests library:
# 
# ```python
import pytest
import requests
# 
def test_password_length(access_token):
    url = get_endpoint_url('/register')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'email': 'test@example.com',
        'password': 'short'
    }
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 400, "Expected status code 400, but got {}".format(response.status_code)
```

# This test function sends a POST request to the '/register' endpoint with a password that is less than 8 characters long. It then checks if the response status code is 400, which indicates that the input is invalid. The 'access_token' is used in the Authorization header. The 'get_endpoint_url' function is used to construct the full endpoint URL.

# Here is a Python pytest test function using the requests library:
# 
# ```python
import pytest
import requests
import json
# 
def test_registration_missing_field(access_token):
    # Construct the endpoint URL
    endpoint_url = get_endpoint_url('/register')

    # Define the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the payload with missing field
    payload = {
        'email': 'test@example.com',
    }
# 
    # Send the POST request
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(payload))
# 
    # Assert that the response status code is 400
    assert response.status_code == 400, f'Expected status code 400, but got {response.status_code}'
# ```
# 
# In this test function, we are sending a POST request to the '/register' endpoint with a payload that is missing the 'password' field. According to the OpenAPI spec, this should result in a 400 Bad Request response. The test function asserts that the response status code is indeed 400. If it's not, the test will fail and print a message indicating the actual status code received.

# Here is a Python pytest test function using the requests library:
# 
# ```python
import pytest
import requests
import json
# 
def test_user_registration(access_token):
    # Define the endpoint path
    path = '/register'

    # Construct the full endpoint URL
    url = get_endpoint_url(path)
# 
    # Define the request headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the request body
    body = {
        'email': 'test@example.com',
        'password': 'testpassword'
    }
# 
    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(body))
# 
    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201
# 
    # Assert that the response body contains a user ID
    response_body = response.json()
    assert 'id' in response_body
# ```
# 
# This test function sends a POST request to the '/register' endpoint with a JSON body containing an email and password. It then checks that the response status code is 201 (Created) and that the response body contains a user ID. The 'access_token' pytest fixture is used to provide a valid token for the 'Authorization' header.

# Here is a Python pytest test function using the requests library:
# 
# ```python
import pytest
import requests
# 
def test_password_not_in_response(access_token):
    # Construct the endpoint URL
    endpoint_url = get_endpoint_url('/register')

    # Define the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the payload
    payload = {
        'email': 'test@example.com',
        'password': 'test_password'
    }
# 
    # Send the POST request
    response = requests.post(endpoint_url, headers=headers, json=payload)
# 
    # Assert that the response status code is 201 (Registration successful)
    assert response.status_code == 201
# 
    # Assert that 'password' is not in the response
    assert 'password' not in response.json()
# ```
# 
# This test function sends a POST request to the '/register' endpoint with a JSON payload containing 'email' and 'password'. It then checks that the response status code is 201 (indicating successful registration) and that 'password' is not included in the response.

# Here is a Python pytest test function using the requests library:
# 
# ```python
import pytest
import requests
import json
# 
def test_register_existing_email(access_token):
    # Construct the endpoint URL
    endpoint_url = get_endpoint_url('/register')

    # Define the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the request body
    body = {
        'email': 'existingemail@example.com',
        'password': 'password123'
    }
# 
    # Send the POST request
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(body))
# 
    # Assert that the response status code is 409 (Conflict)
    assert response.status_code == 409, f'Expected status code 409, but got {response.status_code}'
# ```
# 
# This test function sends a POST request to the '/register' endpoint with an existing email and checks if the response status code is 409 (Conflict). The 'access_token' fixture is used in the Authorization header. The 'get_endpoint_url' helper function is used to construct the full endpoint URL.

# Here is a Python pytest test function using the requests library:
# 
# ```python
import pytest
import requests
import json
# 
def test_registration_email_format(access_token):
    # Construct the endpoint URL
    url = get_endpoint_url('/register')

    # Define the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
# 
    # Define the payload with invalid email format
    payload = {
        'email': 'invalidemail',
        'password': 'password123'
    }
# 
    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
# 
    # Assert that the response status code is 400 (Bad Request)
    assert response.status_code == 400
# 
    # Define the payload with valid email format
    payload = {
        'email': 'validemail@example.com',
        'password': 'password123'
    }
# 
    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
# 
    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201
# ```
# 
# This test function first sends a POST request to the '/register' endpoint with an invalid email format and asserts that the response status code is 400 (Bad Request). Then, it sends another POST request with a valid email format and asserts that the response status code is 201 (Created). This way, it verifies that the system only accepts registrations where the email field follows a valid email format.
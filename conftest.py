import pytest
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(scope="session")
def access_token():
    """
    Returns an access token for API authentication.
    Reads CLIENT_ID, CLIENT_SECRET, and TOKEN_URL from environment variables (.env file).
    """
    client_id = os.environ.get("API_CLIENT_ID")
    client_secret = os.environ.get("API_CLIENT_SECRET")
    token_url = os.environ.get("TOKEN_URL")
    if not all([client_id, client_secret, token_url]):
        raise RuntimeError("API_CLIENT_ID, API_CLIENT_SECRET, and TOKEN_URL must be set in your .env file.")
    data = {"client_id": client_id, "client_secret": client_secret}
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    return response.json().get("access_token", "dummy_token")

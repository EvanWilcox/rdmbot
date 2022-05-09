"""
Auth for Twitter API

sudo docker run -it --rm -e CONSUMER_KEY=<CONSUMER_KEY> -e CONSUMER_SECRET=<CONSUMER_SECRET> rdmbot auth.py
"""

import os
import sys
from requests_oauthlib import OAuth1Session


CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")


# Get request token
REQUEST_TOKEN_URL = (
    "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
)
oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET)

try:
    fetch_response = oauth.fetch_request_token(REQUEST_TOKEN_URL)
except ValueError:
    print("There may have been an issue with the consumer_key or consumer_secret you entered.")
    sys.exit(1)

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")

# Get authorization
BASE_AUTHORIZATION_URL = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(BASE_AUTHORIZATION_URL)
print(f"Please go here and authorize: {authorization_url}")
verifier = input("Paste the PIN here: ")

# Get the access token
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    CONSUMER_KEY,
    client_secret=CONSUMER_SECRET,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)

oauth_tokens = oauth.fetch_access_token(ACCESS_TOKEN_URL)

ACCESS_TOKEN = oauth_tokens["oauth_token"]
ACCESS_TOKEN_SECRET = oauth_tokens["oauth_token_secret"]

print(f"access token: {ACCESS_TOKEN}")
print(f"access token secret: {ACCESS_TOKEN_SECRET}")

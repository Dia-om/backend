import logging
from fastapi import FastAPI, Request, Depends, APIRouter, status
from fastapi.responses import RedirectResponse
from requests_oauthlib import OAuth1Session
from typing import Optional

router = APIRouter(prefix="/user", tags=["User"])

TWITTER_API_KEY = "ti4w37vOVNRHE370vQHBwvk9Z"
TWITTER_API_SECRET = "GKdNRpmeOJ6qpNt09tm0c4NkdiCrmtNCqTG0GdMn4hawDHw5q2"
TWITTER_CALLBACK_URL = "http://localhost:800/api/v1/user/auth/twitter"
TWITTER_REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
TWITTER_AUTHORIZATION_URL = "https://api.twitter.com/oauth/authorize"
TWITTER_ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
TWITTER_USER_INFO_URL = "https://api.twitter.com/1.1/users/show.json"


@router.get("/login/twitter")
async def twitter_login(request: Request):
    # Create an OAuth1Session object
    twitter_oauth = OAuth1Session(
        TWITTER_API_KEY,
        client_secret=TWITTER_API_SECRET
        )

    # Get the request token
    response = twitter_oauth.fetch_request_token(TWITTER_REQUEST_TOKEN_URL)
    request.session["twitter_oauth_token"] = response.get("oauth_token")
    request.session["twitter_oauth_token_secret"] = response.get("oauth_token_secret")

    # Get the authorization URL
    authorization_url = twitter_oauth.authorization_url(TWITTER_AUTHORIZATION_URL)

    return RedirectResponse(url=authorization_url)

@router.get("/auth/twitter")
async def twitter_callback(request: Request, oauth_token: str = None, oauth_verifier: str = None):
    # Retrieve the stored token and token secret
    oauth_token = request.session.get("twitter_oauth_token")
    oauth_token_secret = request.session.get("twitter_oauth_token_secret")

    # Create a new OAuth1Session object
    twitter_oauth = OAuth1Session(
        TWITTER_API_KEY,
        client_secret=TWITTER_API_SECRET,
        resource_owner_key=oauth_token,
        resource_owner_secret=oauth_token_secret,
        verifier=oauth_verifier
    )

    # Fetch the access token
    try:
        response = twitter_oauth.fetch_access_token(TWITTER_ACCESS_TOKEN_URL)
        access_token = response.get("oauth_token")
        access_token_secret = response.get("oauth_token_secret")
    except Exception as e:
        logging.error("Error fetching access token: %s", e)
        return {"error": "Failed to fetch access token"}

    # Use the access token to fetch the user's profile information
    twitter_oauth = OAuth1Session(
        TWITTER_API_KEY,
        client_secret=TWITTER_API_SECRET,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )

    try:
        user_info = twitter_oauth.get(TWITTER_USER_INFO_URL).json()
        print(user_info)
    except Exception as e:
        logging.error("Error fetching user information: %s", e)
        return {"error": "Failed to fetch user information"}

    # Check the user information
    logging.info("User information: %s", user_info)
    

    return {
        "name": user_info.get("name"),
        "screen_name": user_info.get("screen_name"),
        "profile_image_url": user_info.get("profile_image_url")
    }
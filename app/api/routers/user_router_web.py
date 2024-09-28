"""This module defines the FastAPI API endpoints for user."""


from typing import Any

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.requests import Request

#from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError


from app.api.schemas.user_schemas import AccountSchema
from app.database.connection import get_db
from app.services.user_services import(
    sign_up,
)

router = APIRouter(prefix="/user", tags=["User"])

config = Config('.env')  # read config from .env file
oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id= config("GOOGLE_CLIENT_ID",None),
    client_secret=config("GOOGLE_CLIENT_SECRET",None),
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': 'http://localhost:8000/api/v1/user/auth/google'
    }
)

oauth.register(
    name='twitter',
    api_base_url='https://api.twitter.com/1.1/',
    client_id= config("TWITTER_CLIENT_ID",None),
    client_secret=config("TWITTER_CLIENT_SECRET",None),
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
)

@router.get('/signup/google')
async def google_signup(request: Request):
    redirect_uri = request.url_for('auth_google')
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/login/google')
async def google_login(request: Request):
    redirect_uri = request.url_for('auth_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/login/twitter')
async def twitter_login(request: Request):
    # absolute url for callback
    # we will define it below
    redirect_uri = request.url_for('auth_twitter')
    return await oauth.twitter.authorize_redirect(request, redirect_uri)

@router.get('/auth/google')
async def auth_google(request: Request, db:Session = Depends(get_db),):
    try:
        token = await oauth.google.authorize_access_token(request)
    # user = await oauth.google.parse_id_token(request, token)
    except OAuthError as e:
        raise e
    user = token.get('userinfo')
    user = dict(user)

    exist,resp = sign_up(user,db)

    request.session["email"] = user["email"]
    request.session["name"] = user["name"]

    if exist:
        return { "status": status.HTTP_200_OK,
                "message": "Login Success",
                "data":{}
                }
    return resp    

@router.get('/auth/twitter')
async def auth_twitter(request: Request):
    token = await oauth.twitter.authorize_access_token(request)
    url = 'account/verify_credentials.json'
    resp = await oauth.twitter.get(
        url, params={'skip_status': True}, token=token)
    user = resp.json()
    return user



@router.get('/session')
def current_session(request: Request):

    return {
        "status":status.HTTP_200_OK,
        "message":"success",
        "data": {
            "email": request.session.get("email"),
            "name": request.session.get("name")
        }
    }

@router.get('/logout')
def logout(request: Request):
    request.session.pop("email")
    request.session.pop("name")
    request.session.clear()

    return {
        "status": status.HTTP_200_OK,
        "message": "Logout Success",
        "data": {}
    }
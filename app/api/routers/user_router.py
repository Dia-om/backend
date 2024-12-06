"""This module defines the FastAPI API endpoints for user."""


from typing import Any

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.requests import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse


from app.api.schemas.user_schemas import AccountSchema, UpdateUserSchema
from app.database.connection import get_db
from app.services.user_services import(
    sign_up,
    sign_in,
    update_user_details,
)

router = APIRouter(prefix="/user", tags=["User"])

config = Config('.env')  # read config from .env file

@router.post('/signup/google')
async def google_signup(user: AccountSchema, request: Request, db:Session = Depends(get_db), ):

    exist,resp = sign_up(user,db)

    if exist:
        redirect_uri = request.url_for('google_login', **{"email" : user.email})

        return RedirectResponse(redirect_uri, status_code= status.HTTP_302_FOUND)
    jsonableData = jsonable_encoder(resp)

    return JSONResponse(content=jsonableData)


@router.get('/login/google/{email}')
def google_login(email: str, db:Session = Depends(get_db),):
    resp = sign_in(email,db)

    jsonableData = jsonable_encoder(resp)

    return JSONResponse( status_code= jsonableData['status'], content=jsonableData)

@router.put('/update_profile')
async def update_profile(email:str,user_details:UpdateUserSchema, db:Session = Depends(get_db),):
    resp = update_user_details(email,user_details,db)

    return JSONResponse(status_code=resp['status'], content= jsonable_encoder(resp))
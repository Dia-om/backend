"""This module provides functions for handling user related
operations."""

from datetime import datetime
from typing import Any
from uuid import uuid4
import string
import random

from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
#from sqlalchemy.exc import InternalError
from sqlalchemy.orm import Session

from app.api.models.user_models import User
from app.api.schemas.user_schemas import AccountSchema, UserSchema

def code_generator(size=8):
    code = "".join(random.choice(string.ascii_letters+string.digits) for i in range(size))
    return code

def sign_up(user:AccountSchema, db:Session) -> tuple[bool,Any]:
    # user = user.model_dump(exclude_unset = True)
    user_exist = False

    # check if user already signed up
    user_instance = db.query(User).filter(User.email == user.email).first()


    if user_instance == None:
        # Basic signup entry to database
        email=user.email
        business = user.name
        code = code_generator()
        new_user = User(email=email,business_name=business, user_code=code, id=uuid4().hex)

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            response = {
                "status" : status.HTTP_201_CREATED,
                "message": "User created success",
                "data": jsonable_encoder(new_user)
            }

            return user_exist, response
        except Exception as e:
            db.rollback()
            # raise HTTPException(
            #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #     detail="Failed to add user"
            # )
            raise e
        
    else:
        user_exist = True
        return user_exist,None



def sign_in(email:str, db:Session) -> Any:
    # check if user already exist and return data or error
    user_instance = db.query(User).filter(User.email == email).first()
    if user_instance == None:
        return  {
                "status" : status.HTTP_404_NOT_FOUND,
                "message": "User not found",
                "data": {}
            }
    return {
                "status" : status.HTTP_200_OK,
                "message": "login success",
                "data": jsonable_encoder(user_instance)
            }
    

def update_user_details():
    pass
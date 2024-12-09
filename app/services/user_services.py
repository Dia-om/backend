"""This module provides functions for handling user related
operations."""

from datetime import datetime
from typing import Any
from uuid import uuid4
import string
import random
from starlette.config import Config
from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
#from sqlalchemy.exc import InternalError
from sqlalchemy.orm import Session

from app.api.models.user_models import User
from app.api.schemas.user_schemas import AccountSchema, UpdateUserSchema

# retrieve environment variables from .env
config = Config(".env")
default_album_hash = config("DEFAULT_ALBUM_HASH",None)
# album_delete_hash = config("ALBUM_DELETE_HASH",None)
# client_secret = config("IMGUR_CLIENT_SECRET",None)

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
        # email=user.email
        # business = user.business_name
        # image_url = user
        code = code_generator()
        new_user = User(**user.dict(exclude_unset=True), user_code=code,password=default_album_hash, id=uuid4().hex)

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            response = {
                "status" : status.HTTP_201_CREATED,
                "message": "User created success",
                "data": jsonable_encoder(new_user)
            }

            return False, response
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
    

def update_user_details(email:str, details: UpdateUserSchema, db:Session) -> Any:
    # check if user already exist and return data or error
    user_instance = db.query(User).filter(User.email == email).first()

    if user_instance == None:
        return  {
                "status" : status.HTTP_404_NOT_FOUND,
                "message": "User not found",
                "data": {}
            }
    user_details = details.dict(exclude_unset = True)
    user_details['date_updated'] = datetime.now()

    print(user_details)
    
    try:
        for key,value in user_details.items():
            setattr(user_instance,key,value)

        db.commit()
        db.refresh(user_instance)

        return {
            "status" : status.HTTP_201_CREATED,
            "message": "User details updated successfully",
            "data": jsonable_encoder(user_instance)
        }
        
    except Exception as e:
        db.rollback()
        raise e


# def delete_user(user_id:str,db:Session):
#     # check if user already exist and return data or error
#     user_instance = db.query(User).filter(User.id == user_id).first()

#     if user_instance == None:
#         return  {
#                 "status" : status.HTTP_404_NOT_FOUND,
#                 "message": "User not found",
#                 "data": {}
#             }
#     try:
#         db.delete(user_instance)
#         db.commit()

#         return {
#             "status": status.HTTP_200_OK,
#             "message": f"User {user_id} deleted successfully",
#             "data": {}
#         }
#     except Exception as e:
#         db.rollback()
#         raise e

# def get_users(db:Session):
#     try:
#         users = db.query(User).all()
#         return users
#     except Exception as e:
#         raise e
"""This module provides functions for handling customer related
operations."""

from datetime import datetime
from typing import Any
from uuid import uuid4
import string
import random
from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api.models.customer_models import Customer
from app.api.models.user_models import User
from app.api.schemas.customer_schemas import CustomerSchema


def add_customer(user_id:str,customer:CustomerSchema,db:Session):
    # check user id is valid
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user ID")
    

    new_customer = Customer(**customer.dict(exclude_unset=True),user_id = user_id, id=uuid4().hex)

    # add entry into database
    try:
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)

        return {
            "status": status.HTTP_201_CREATED,
            "message": "Customer created successs",
            "data": jsonable_encoder(new_customer)
        }

    except Exception as e:
        db.rollback()
        raise e



def update_customer():
    pass



def fetch_customers(user_id:str, db:Session):
    # check user id is valid
    user = db.query(User).filter(User.id == user_id).first()

    if user is not None:
        try:
            customers = db.query(Customer).filter(Customer.user_id == user_id).all()
            return customers
        except Exception as e:
            raise e
        
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid User ID")
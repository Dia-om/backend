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
from app.api.models.record_models import Record
from app.api.models.user_models import User
from app.api.schemas.customer_schemas import CustomerSchema
from app.api.schemas.record_schemas import RecordCreate


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
    

def fetch_customer(customer_id:str,db:Session):
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()

        if customer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid customer id")
        
        return customer
    except Exception as e:
        raise e

def add_record(customer_id:str,record:RecordCreate,db:Session):
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()

        if customer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid customer id")
        
        new_record = Record(**record.dict(),customer_id = customer_id, id=uuid4().hex)

        # add entry into database
        try:
            db.add(new_record)
            db.commit()
            db.refresh(new_record)

            return {
                "status": status.HTTP_201_CREATED,
                "message": "Record added successs",
                "data": jsonable_encoder(new_record)
            }

        except Exception as e:
            db.rollback()
            raise e
        

    except Exception as e:
        raise e

def remove_record(customer_id:str,record_id:str, db:Session):
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()

        if customer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid customer id")
        
        record = db.query(Record).filter(Record.id == record_id).first()

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid record id")
        
        try:
            db.delete(record)
            db.commit()

            return {
                "status": status.HTTP_200_OK,
                "message": f"Record {record_id} deleted successfully",
                "data": {}
            }
        except Exception as e:
            db.rollback()
            raise e
    except Exception as e:
        raise e

def update_record():
    pass
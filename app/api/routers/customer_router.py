"""This module defines the FastAPI API endpoints for Customer."""


from typing import Any

from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


from app.api.schemas.customer_schemas import CustomerSchema
from app.api.schemas.record_schemas import RecordCreate
from app.database.connection import get_db
from app.services.customer_services import(
    add_customer,
    add_record,
    fetch_customer,
    fetch_customers,
    remove_record,
)

router = APIRouter(prefix="/customer", tags=["Customer"])

@router.post("/add")
async def customer_add(user_id:str,details:CustomerSchema, db:Session = Depends(get_db)) -> Any:
    """Add a new customer, customer details submitted as body"""
    resp = add_customer(user_id,details,db)
    return JSONResponse(content=jsonable_encoder(resp))


@router.get("/customers")
def get_customers(user_id:str, db:Session = Depends(get_db)) -> Any:
    resp = fetch_customers(user_id,db)
    return JSONResponse(content=jsonable_encoder(resp))

@router.get("")
def get_customer(customer_id:str, db:Session = Depends(get_db)) -> Any:
    resp = fetch_customer(customer_id,db)
    return JSONResponse(content=jsonable_encoder(resp))

@router.post("/add_record")
async def record_create(customer_id:str, record:RecordCreate,db:Session = Depends(get_db)) -> Any:
    """Add a new record for a customer, record details submitted as body"""
    resp= add_record(customer_id,record,db)
    return JSONResponse(content=jsonable_encoder(resp))

@router.delete("/remove_record")
async def  record_delete(customer_id:str,record_id:str,db:Session=Depends(get_db)) -> Any:
    resp = remove_record(customer_id,record_id,db)
    return JSONResponse(content=jsonable_encoder(resp))




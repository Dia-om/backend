"""This module defines the FastAPI API endpoints for file uploads."""


from typing import Any

from fastapi import APIRouter, Depends, File, UploadFile

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# from app.api.models.user_models import User
from sqlalchemy.orm import Session
from app.api.schemas.upload_schemas import ImgurSchema
from app.database.connection import get_db
from app.services.imgur_services import(
    get_album_images,
    delete_image,
    return_token,
    upload_image,
    get_account_images,
    create_album,
    add_to_album,
)

router = APIRouter(prefix="/files", tags=["File Management"])

@router.get("/album/images/")
async def album_images(payload: ImgurSchema = Depends()) -> Any:
    """Retrieve images from imgur album"""
    resp = get_album_images(payload.album_hash)
    return JSONResponse(content=resp)

@router.get("/account/images/")
async def account_images() -> Any:
    """Retrieve all images from imgur Account"""
    resp = get_account_images()
    return JSONResponse(content=resp)

@router.delete("/{delete_hash}")
async def image_delete(delete_hash:str) -> Any:
    resp = delete_image(delete_hash)
    return JSONResponse(content= {"message":"image deleted successfully!", "response":resp})

@router.post("/upload/")
async def image_upload(payload:ImgurSchema = Depends(),file:UploadFile = File(...), db:Session=Depends(get_db)) -> Any:
    """Upload an image to an album if album_hash is provided; or upload to account. To be implemented later for 
    web app"""

    if not payload:
        return JSONResponse(status_code= 204,content={"message": "No file sent"})
    
    # read file data from payload
    email  = payload.email
    album_hash = payload.album_hash

    content = await file.read()

    # upload the image
    resp = upload_image(email,content,db,album_hash)
    
    return JSONResponse(content= jsonable_encoder(resp))
@router.post("/album/create/")
async def new_album(imgur_id:str, title:str) -> Any:
    """Create a new Album"""
    resp = create_album(imgur_id,title)    
    # return JSONResponse(content={"album_id": album_id})
    return JSONResponse(content= jsonable_encoder(resp))


@router.post("/album/add")
async def add_image(payload:ImgurSchema = Depends(), db:Session = Depends(get_db)) -> Any:
    """ Add already uploaded image to an Album"""
    resp = add_to_album(payload.email,payload.image_hash,payload.album_hash,db)
    return JSONResponse(content=jsonable_encoder(resp))

@router.get("/token/")
def get_token() -> Any:
    token = return_token()

    return JSONResponse(content={"token":token})
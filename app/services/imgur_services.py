from fastapi import HTTPException, status
import requests
import base64
from starlette.config import Config

from sqlalchemy.orm import Session

from app.api.models.user_models import User

# retrieve environment variables from .env
config = Config(".env")
client_id = config("IMGUR_CLIENT_ID", None) 
account_id = config("IMGUR_ACCOUNT_ID", None) 
access_token = config("IMGUR_ACCESS_TOKEN",None)
# default_album_hash = config("DEFAULT_ALBUM_HASH",None)
# album_delete_hash = config("ALBUM_DELETE_HASH",None)
# client_secret = config("IMGUR_CLIENT_SECRET",None)
# refresh_token =  config("IMGUR_REFRESH_TOKEN", None)

# base url for api calls
base_url = "https://api.imgur.com/3"

def return_token():
    return access_token

def create_album(user_id: str, title:str):
    """Create an Imgur album for the user."""

    if user_id != account_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message":"You dont't have the right access to this service"})
    url = f"{base_url}/album"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        }
    data = {"title": title, "description": f"{title} Album for user {user_id}"}
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    # print(response.json()["data"]["id"])
    return  response.json()["data"]


def get_album_images(album_hash: str):
    """Retrieve images from an album."""
    url = f"{base_url}/album/{album_hash}/images"
    # headers = {"Authorization": f"Client-ID {client_id}"}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

def get_account_images():
    url = f"{base_url}/account/me/images"

    # headers = {"Authorization": f"Client-ID {client_id}"}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        images = response.json()["data"]
        # Filter images where album field is None
        # no_album_images = [img for img in images if img["album"] is None]
        no_album_images = [img for img in images ]

        return no_album_images
    else:
        raise Exception(f"Failed to fetch images: {response.json()}")


def delete_image(deletehash:str):
    """Delete an image by deletehash."""
    url = f"{base_url}/image/{deletehash}"
    # headers = {"Authorization": f"Client-ID {client_id}"}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

def upload_image(email:str,file:bytes, db:Session, album_hash:str = None,):

    # check if user is valid
    user_instance = db.query(User).filter(User.email == email)

    if user_instance == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Invalid user")
    
    # headers = {"Authorization": f"Client-ID {client_id}"}
    headers = {
        "Authorization": f"Bearer {access_token}",
        }
    
    image_data = base64.b64encode(file).decode()

    try:
       
        url = f"{base_url}/image"
        data = {"image": image_data}
        response = requests.post(url,headers=headers, data=data)
        # image_hash = response.json()["data"]["deletehash"]
        image_id = response.json()["data"]["id"]

        if not image_id:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Failed to return image hash")
    except Exception as e:
        raise e

    if album_hash != None:
        url = f"{base_url}/album/{album_hash}/add"    
        data = {"ids": image_id}
        
        try:
            add_to_album = requests.post(url,headers=headers, json=data)
            print(add_to_album.json()["data"])
            add_to_album.raise_for_status()
        except Exception as e:
            raise e
        
    # return {
    #     "id": response.json()["data"]["id"],
    #     "deletehash": response.json()["data"]["deletehash"],
    #     "album_id": album_id
    # }
    return response.json()["data"]

def add_to_album(email:str, image_hash:str,album_hash:str,db:Session):
    # check if user is valid
    user_instance = db.query(User).filter(User.email == email)

    if user_instance == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Invalid user")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        }
    url = f"{base_url}/album/{album_hash}/add"    
    data = {"ids": image_hash}
    
    try:
        response = requests.post(url,headers=headers, json=data)
        response.raise_for_status()
    except Exception as e:
        raise e
    
    return response.json()["data"]
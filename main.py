import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from starlette.middleware.sessions import SessionMiddleware

from app.api.routers.user_router import router as user_routers

v1_router = APIRouter(prefix="/api/v1")


v1_router.include_router(
    user_routers,
)

app = FastAPI(
    title="Diamobile API",
    description="Manage you clients one api call at a time",
    version="0.1.0",
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="!secret")

@app.get("/health")
def health():
    """Health check endpoint."""
    # add exception handling here
    return {
        "status": 200,
        "message": "Healthy"
    }


app.include_router(v1_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app",host="localhost", port=8000, reload=True)
        
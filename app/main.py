from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)  # use sqlalchemy to generate tables

app = FastAPI()

origins = ["*"]                                 # modify this origin to our specific webapp

# Allow different domains to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Display root page
@app.get("/")									# <fast api decorator><instance name>.<http method>.("<path>")
async def root():								# parallel function
    return {"message": "welcome to my api!"}	# data sent back to user, converted to json






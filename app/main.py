from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, like

# instance of FastAPI
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)

# binding models to main file 
# no need after alembic (it creates tables auto)
# models.Base.metadata.create_all(bind=engine)

origins = ['*']

# CORS setting
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# func for welcome msg (root)
@app.get("/")
def welcome_message():
    return {"message": "Welcome to my API"}
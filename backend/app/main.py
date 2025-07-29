from fastapi import FastAPI
from .routes import router

app = FastAPI()
app.include_router(router)


# This is a FastAPI application that includes a router from the routes module.
# The router contains various endpoints that handle different functionalities of the application.
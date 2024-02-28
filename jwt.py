import requests
from typing import Annotated
from fastapi import FastAPI, Form, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
import json

app = FastAPI(title="Testing FastApi",
    summary="by haynafi",
    version="0.0.1",)

class User(BaseModel):
    username: str
    password: str

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@app.post('/getToken')
def getToken(user: User, Authorize: AuthJWT = Depends()):
    if user.username != "1111" or user.password != "1111":
        raise HTTPException(status_code=401,detail="Bad username or password")

    # Use create_access_token() and create_refresh_token() to create our
    # access and refresh tokens
    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    return {"access_token": access_token, "refresh_token": refresh_token}


@app.post("/sample")
def sso(username: Annotated[str, Form()], password: Annotated[str, Form()], Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    data = 'username='+username+'&password='+password+'&userAuth='+current_user
    return json.loads(data)

        


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="10.62.164.188", port=8000)
from typing_extensions import Annotated, Doc
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from auth.jwt_handler import Auth

class User_JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(User_JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials = await super(User_JwtBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid and Expired Token "
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid and expired token "
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid or expired token !")

    def verify_jwt(self, jwttoken: str):
        decode_token = Auth.decode_access_token(jwttoken)

        return decode_token is not None

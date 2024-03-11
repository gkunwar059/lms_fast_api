from typing_extensions import Annotated, Doc
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from auth.jwt_handler import Auth

class Librarian_JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):    #auto_error: bool = True->  #automatically raise a exception while true 
        super(Librarian_JwtBearer, self).__init__(auto_error=auto_error)  #if no value will given,it will default to true  #super()-used to acess the methods and properties from the parent class of a derieved class 

    async def __call__(self, request: Request) :
        credentials= await super(Librarian_JwtBearer, self).__call__(request)
        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code= 403,
                    detail= "Invalid or expired Token!"
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403,
                    detail="Invalid or expired token"
                )
            return credentials.credentials
        
        else:
            raise HTTPException(
                status_code= 403,
                detail= "Invalid or expired Token!"
            )
    
    def verify_jwt(self, jwttoken:str):
        # Decode the JWT token
        decode_token=Auth.decode_librarian_token(jwttoken)
        
        #Check if the decoded token is not None(indicating a valid token)
        return decode_token is not None
    

class Member_JwtBearer(HTTPBearer):
    def __init__(self,auto_error:bool=True):
        super(Member_JwtBearer,self).__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials= await super(Member_JwtBearer,self).__call__(request)
        
        if credentials:
            if not credentials.scheme =='Bearer':
                raise HTTPException(
                    status_code=403,
                    detail="Invalid and Expired Token "
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403,
                    detail="Invalid and expired token "
                    
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403,
                detail="Invalid or expired token !"
            )
        
    def verify_jwt(self,jwttoken:str):
        decode_token=Auth.decode_member_token(jwttoken)
        
        return decode_token is not None

        
        
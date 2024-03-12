
from fastapi import HTTPException,status
import jwt
from datetime import datetime,timedelta
from decouple import config


LIBRARIAN_JWT_SECRET=config('librarian_secret_key')
LIBRARIAN_JWT_ALGORITHM=config('algorithm')

MEMBER_JWT_SECRET=config('member_secret_key')
MEMBER_JWT_ALGORITHM=config('algorithm')


class Auth:
    
    @staticmethod
    def generate_librarian_token(email):
        # Generate both acess and refresh token
        access_payload={
            'email':email,
            'exp':datetime.utcnow() +timedelta(minutes=15)
        }
        
        refresh_payload={
            'email':email,
            'exp':datetime.utcnow() +timedelta(minutes=35)
        }
        
        access_token=jwt.encode(access_payload,LIBRARIAN_JWT_SECRET,algorithm=LIBRARIAN_JWT_ALGORITHM)
        refresh_token=jwt.encode(refresh_payload,LIBRARIAN_JWT_SECRET,algorithm=LIBRARIAN_JWT_ALGORITHM)

        return {"acess_token":access_token,
                "refresh_token":refresh_token}
    

    @staticmethod
    def decode_librarian_token(token):
        # decode and verify token
        try:
            decoded_data = jwt.decode(token,LIBRARIAN_JWT_SECRET, algorithms=[LIBRARIAN_JWT_ALGORITHM])
            return decoded_data
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Signature expired. Please log in again")
            
        
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token. Please log in again")


    @staticmethod
    def generate_member_token(email):
        # generate both acess and refresh token
        
        access_payload={
            'email':email,
            'exp':datetime.utcnow()+timedelta(minutes=15)
        }
        
        refresh_payload={
            'email':email,
            'exp':datetime.utcnow()+timedelta(minutes=35)
        }

        access_token=jwt.encode(access_payload,MEMBER_JWT_SECRET,algorithm=MEMBER_JWT_ALGORITHM)
        refresh_token=jwt.encode(refresh_payload,MEMBER_JWT_SECRET,algorithm=MEMBER_JWT_ALGORITHM)
        
        return{
            "access_token":access_token,
            "refresh_token":refresh_token
        }

    def decode_member_token(token):
        try:  
            decode_data=jwt.decode(token,MEMBER_JWT_SECRET,algorithms=[MEMBER_JWT_ALGORITHM])
            return decode_data
        
        except jwt.ExpiredSignatureError:
            raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Signature expired. Please log in again!")  
        
               
        except jwt.InvalidTokenError:
            raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token. Please log in again")



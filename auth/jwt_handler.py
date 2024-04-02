from fastapi import HTTPException, status
import jwt
from datetime import datetime, timedelta
from decouple import config

USER_ACCESS_JWT_SECRET = config("access_secret_key")
USER_REFRESH_JWT_SECRET=("refresh_secret_key")

USER_JWT_ALGORITHM = config("algorithm")


class Auth:

    @staticmethod
    def generate_user_token(email):

        access_payload = {
            "email": email,
            "exp": datetime.utcnow() + timedelta(minutes=15),
        }

        refresh_payload = {
            "email": email,
            "exp": datetime.utcnow() + timedelta(minutes=35),
        }

        access_token = jwt.encode(
            access_payload, USER_ACCESS_JWT_SECRET, algorithm=USER_JWT_ALGORITHM
        )
        refresh_token = jwt.encode(
            refresh_payload, USER_REFRESH_JWT_SECRET, algorithm=USER_JWT_ALGORITHM
        )

        return {"access_token": access_token, "refresh_token": refresh_token}

    def decode_access_token(token):
        try:
            decode_data = jwt.decode(
                token, USER_ACCESS_JWT_SECRET, algorithms=[USER_JWT_ALGORITHM]
            )
            return decode_data
            
        

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Signature expired. Please log in again!",
            )

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token. Please log in again",
            )
            
    def decode_refresh_token(token):
        print(token)
        try:
            decode_data = jwt.decode(
                token,USER_REFRESH_JWT_SECRET, algorithms=[USER_JWT_ALGORITHM]
            )
            print(decode_data)
            return decode_data
            
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Signature refresh expired. Please log in again!",
            )

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token. Please log in again",
            )

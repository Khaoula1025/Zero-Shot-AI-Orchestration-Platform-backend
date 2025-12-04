from fastapi import Depends
from jose import jwt 
import time
from db.database import sessionmaker,get_db
from models.user import User
import os 
from dotenv import load_dotenv

load_dotenv()

jwtSecret=os.getenv('secret')

def signJwt(user_id):
    payload={
        'user_id':user_id,
              "expires": time.time() +800
    }
    token = jwt.encode(payload,jwtSecret,algorithm='HS256')
    return {
        'access_token':token,
        'token_type':'Bearer'
    }

def check_user(user,db:sessionmaker=Depends(get_db)):
    found =db.query(User).filter(User.username==user.username,User.password==user.password).first()
    if found:
        return 'user found'
    else:
        return 'user not found'




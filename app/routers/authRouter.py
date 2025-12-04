from fastapi import APIRouter,Depends,HTTPException,Response
from schemas.user import userCreate
from models.user import User
from db.database import get_db
from db.database import sessionmaker
from dependencies import signJwt

authRouter= APIRouter(prefix="/auth")

@authRouter.post("/signUp")
async def create_user(user:userCreate,db:sessionmaker=Depends(get_db)):
    found =db.query(User).filter(User.username==user.username,User.password==user.password).first()
    if found:
        raise HTTPException(status_code=409,detail='User Already found')
    else:
        new_user=User(username=user.username,password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return 'sign up sucessfull'


@authRouter.post('/login')
async def register(response:Response,user:userCreate,db:sessionmaker=Depends(get_db)):
    found =db.query(User).filter(User.username==user.username,User.password==user.password).first()
    if found :
        token =signJwt(user.username)
        response.set_cookie(
            key='access_token',
            value=token['access_token'],
            httponly=True,
            samesite='none'
        )
        return 'login successfull'

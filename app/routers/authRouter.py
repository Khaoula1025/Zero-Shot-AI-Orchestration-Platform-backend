from fastapi import APIRouter, Depends, HTTPException, Response , status
from schemas.user import userCreate
from models.user import User
from db.database import get_db
from db.database import sessionmaker
from services.auth_services import signJwt
from core.security import hash_password, verify_password
from services.auth_services import get_current_user
authRouter = APIRouter(prefix="/auth")

@authRouter.post("/signUp")
async def create_user(user: userCreate, db: sessionmaker = Depends(get_db)):
    found = db.query(User).filter(User.username == user.username).first()
    
    if found:
        raise HTTPException(status_code=409, detail='User Already exists')
    
    new_user = User(username=user.username, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Sign up successful"}

@authRouter.post('/login')
async def login(response: Response, user: userCreate, db: sessionmaker = Depends(get_db)):

    found = db.query(User).filter(User.username == user.username).first()

    if not found or not verify_password(user.password, found.password):
        raise HTTPException(status_code=401, detail='Invalid username or password')
    
    token = signJwt(found.id)
    response.set_cookie(
        key='access_token',
        value=token['access_token'],
        httponly=True,
        samesite='none',
        secure=True, 
    )
    
    return {"message": "Login successful"}


@authRouter.post('/logout')
async def logout(response:Response):
       response.delete_cookie(
        key="access_token",
        httponly=True,       
        samesite="none",      
        secure=True          
    )
       return {'message':'logout succesful','code':200}

@authRouter.get('/verifyToken')
def verifyToken(current_user:str=Depends(get_current_user)):
     if not current_user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
     elif current_user :
         return {'message':'sucess'}

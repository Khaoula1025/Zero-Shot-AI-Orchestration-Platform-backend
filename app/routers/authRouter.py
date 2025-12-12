from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.schemas.user import userCreate
from app.models.user import User
from app.db.database import get_db
from app.db.database import sessionmaker
from app.services.auth_services import signJwt, get_current_user
from app.core.security import hash_password, verify_password
from app.core.logger import logger   # ⬅️ ADD THIS

authRouter = APIRouter(prefix="/auth")


@authRouter.post("/signUp")
async def create_user(user: userCreate, db: sessionmaker = Depends(get_db)):
    logger.info(f"SignUp requested for user: {user.username}")  # LOG

    found = db.query(User).filter(User.username == user.username).first()
    if found:
        logger.warning(f"SignUp failed — user already exists: {user.username}")  # LOG
        raise HTTPException(status_code=409, detail='User Already exists')
    
    new_user = User(username=user.username, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"User created successfully: {user.username}")  # LOG
    return {"message": "Sign up successful"}


@authRouter.post('/login')
async def login(response: Response, user: userCreate, db: sessionmaker = Depends(get_db)):
    logger.info(f"Login attempt: {user.username}")  # LOG

    found = db.query(User).filter(User.username == user.username).first()
    if not found or not verify_password(user.password, found.password):
        logger.warning(f"Login failed: {user.username}")  # LOG
        raise HTTPException(status_code=401, detail='Invalid username or password')
    
    token = signJwt(found.id)
    response.set_cookie(
        key='access_token',
        value=token['access_token'],
        httponly=True,
        samesite='none',
        secure=True,
    )

    logger.info(f"Login successful: {user.username}")  # LOG
    return {"message": "Login successful"}


@authRouter.post('/logout')
async def logout(response: Response):
    logger.info("User logged out")  # LOG

    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="none",
        secure=True          
    )
    return {'message': 'logout succesful', 'code': 200}


@authRouter.get('/verifyToken')
def verifyToken(current_user: str = Depends(get_current_user)):
    logger.info("Token verification requested")  # LOG

    if not current_user:
        logger.warning("Token invalid")  # LOG
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    logger.info("Token valid")  # LOG
    return {'message': 'success'}

from fastapi import FastAPI,APIRouter
from app.db.database import Base,engine
from app.routers.authRouter import authRouter 
from app.routers.analyzeRouter import analyzeRouter 

app=FastAPI(
    description="Zero-Shot-Ai-Orchestration-Platform"
)
Base.metadata.create_all(bind=engine)

app.include_router(authRouter)
app.include_router(analyzeRouter)
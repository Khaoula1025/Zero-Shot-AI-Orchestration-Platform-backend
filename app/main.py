from fastapi import FastAPI,APIRouter
from db.database import Base,engine
from routers.authRouter import authRouter 
from routers.analyzeRouter import analyzeRouter 

app=FastAPI(
    description="Zero-Shot-Ai-Orchestration-Platform"
)
Base.metadata.create_all(bind=engine)

app.include_router(authRouter)
app.include_router(analyzeRouter)
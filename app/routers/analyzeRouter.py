from fastapi import APIRouter ,Depends
from services.gemini_api import gemini_analyse
from services.hugging_face_filter import articles_analyses
from services.auth_services import get_current_user
from schemas.articles import request_analyse

analyzeRouter=APIRouter()

@analyzeRouter.post('/analyse')
def text_analyze(request:request_analyse,current_user:str=Depends(get_current_user)):
    res_1=articles_analyses(request.article_text)
    response = gemini_analyse(request.article_text,res_1["label"],res_1["score"])
    return response

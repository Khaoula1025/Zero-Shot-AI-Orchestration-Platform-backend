from fastapi import APIRouter
from services.gemini_api import gemini_analyse
from services.hugging_face_filter import articles_analyses
from schemas.articles import request_analyse

analyzeRouter=APIRouter()

@analyzeRouter.post('/analyse')
def text_analyze(request:request_analyse):
    res_1=articles_analyses(request.article_text)
    response = gemini_analyse(res_1["label"],res_1["score"])
    return response
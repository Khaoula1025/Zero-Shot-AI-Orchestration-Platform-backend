from fastapi import APIRouter, Depends
from app.services.gemini_api import gemini_analyse
from app.services.hugging_face_filter import articles_analyses
from app.services.auth_services import get_current_user
from app.schemas.articles import request_analyse
from app.core.logger import logger   # ⬅️ ADD THIS

analyzeRouter = APIRouter()


@analyzeRouter.post('/analyse')
def text_analyze(request: request_analyse, current_user: str = Depends(get_current_user)):
    logger.info(f"/analyse called by {current_user}")  # LOG
    logger.info(f"Text length received: {len(request.article_text)} characters")  # LOG

    res_1 = articles_analyses(request.article_text)
    logger.info(f"HuggingFace result: {res_1}")  # LOG

    response = gemini_analyse(request.article_text, res_1["label"], res_1["score"])
    logger.info(f"Gemini response generated")  # LOG

    return response

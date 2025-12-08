from pydantic import BaseModel

class request_analyse(BaseModel):
    article_text: str

from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
load_dotenv()
HF_KEY=os.getenv('HUGGINGFACE_API_KEY')
client=InferenceClient(token=HF_KEY)

def articles_analyses(text,labels):
    response=client.zero_shot_classification(
        text=text,
        candidate_labels=labels,
        model='facebook/bart-large-mnli'
    )
    return response[0]


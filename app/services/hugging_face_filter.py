from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
load_dotenv()
HF_KEY=os.getenv('HUGGINGFACE_API_KEY')
client=InferenceClient(token=HF_KEY)
CATEGORIES = [
    "Finance",
    "Ressources Humaines",
    "Technologies de l'Information",
    "Opérations",
    "Marketing et Communication",
    "Juridique et Conformité",
    "Stratégie et Management",
    "Risques et Sécurité",
    "Innovation et R&D",
    "Relations Clients",
    "Supply Chain et Logistique",
    "Responsabilité Sociale et Environnementale"
]
def articles_analyses(text):
    response=client.zero_shot_classification(
        text=text,
        candidate_labels=CATEGORIES,
        model='facebook/bart-large-mnli'
    )
    best_result=max(response,key=lambda x:x['score'])
    return {"label": best_result.label, "score": best_result.score}

texte_test_1 = """
Tesla a dépassé les attentes du marché avec un bénéfice trimestriel en hausse de 20%. 
L'entreprise a livré un nombre record de véhicules électriques et prévoit d'ouvrir trois 
nouvelles usines en 2025. Les investisseurs ont salué ces résultats exceptionnels, 
faisant grimper l'action de 12% en séance.
"""

# print(articles_analyses(texte_test_1))


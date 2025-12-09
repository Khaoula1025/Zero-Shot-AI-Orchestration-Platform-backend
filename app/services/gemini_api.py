from google import generativeai as genai
import json 
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def create_prompt(text_org, categorie):
    prompt = f"""Vous êtes un analyste de presse professionnel. Analysez le texte suivant :

Texte : {text_org}
Catégorie détectée : {categorie}

Tâches :
1. Générez un résumé concis en 2-3 phrases maximum
2. Déterminez le ton général (positif, négatif ou neutre)
3. Répondez UNIQUEMENT au format JSON strict ci-dessous, sans texte avant ou après :

{{
    "resume": "votre résumé ici",
    "ton": "positif|negatif|neutre"
}}

Contraintes :
- Restez factuel et objectif
- Le ton doit être exactement : "positif", "negatif" ou "neutre"
- Pas de markdown, pas d'explication additionnelle 
"""
    return prompt

def gemini_analyse(text, categorie):
    try:
        # Configuration de l'API 
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Initialisation du modèle
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Génération du contenu
        response = model.generate_content(create_prompt(text, categorie))
        # Extraction et nettoyage
        texte_reponse = response.text
        texte_propre = texte_reponse.replace('```json', '').replace('```', '').strip()
        
        # Parsing JSON
        resultat = json.loads(texte_propre)
        
        return {'resume':resultat['resume'],'ton':resultat['ton'],'categorie':categorie}
        
    except json.JSONDecodeError as e:
        print(f"Erreur de parsing JSON: {e}")
        return {
            "error": "Invalid JSON response from Gemini",
            "details": str(e)
        }
    
    except Exception as e:
        print(f"Erreur Gemini API: {e}")
        return {
            "error": "Gemini analysis failed",
            "details": str(e)
        }
    

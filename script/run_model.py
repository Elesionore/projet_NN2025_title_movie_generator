"""
Programme qui est un exemple d'utilisation du modèle fine-tuné pour générer un titre de film à partir d'un résumé.
"""

import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Charger le modèle fine-tuné et le tokenizer :
model_save_path = '/home/onyxia/work/projet_NN2025_title_movie_generator/model'
tokenizer = T5Tokenizer.from_pretrained(model_save_path)
model = T5ForConditionalGeneration.from_pretrained(model_save_path)

# Résumé à donner au modèle :
summary = """In a dystopian future where emotions are suppressed by a totalitarian regime, 
    a young woman named Elara discovers an underground movement that seeks to restore feelings 
    to humanity. As she becomes more involved, she learns about the power of love, hope, and rebellion. 
    With the help of a charismatic leader and a group of misfits, Elara must confront her own fears 
    and fight against the oppressive system to reclaim the right to feel. The journey leads her to 
    unexpected alliances and dangerous confrontations, ultimately challenging the very fabric of society."""

# Tokenisation du résumé :
input_ids = tokenizer.encode(summary, return_tensors='pt')

# Création d'un ensemble pour stocker les titres générés et ne pas avoir de doublons
generated_titles = set()

# Générer plusieurs titres différents
while len(generated_titles) < 5:  # Générer jusqu'à 5 titres différents
    with torch.no_grad():
        generated_ids = model.generate(
            input_ids,          # Résumé du film
            max_length=10,      # Longueur maximale du titre
            min_length=3,       # Longueur minimale du titre
            num_beams=5,        # Utilisation de beam search pour une meilleure qualité
            temperature=1.0,    # Paramètre de température pour la génération de texte
            top_k=50,           # Paramètres pour la génération de texte
            top_p=0.9,          # Idem
            do_sample=True,     # Permet de générer des échantillons
            early_stopping=True # Arrêt de la génération lorsque la probabilité de fin est atteinte
        ) 
    
    title = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    
    # Ajouter le titre à l'ensemble s'il n'est pas déjà présent
    generated_titles.add(title)

# Afficher les titres générés
for title in generated_titles:
    print(f"Generated title: {title}")
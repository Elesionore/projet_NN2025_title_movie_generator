from transformers import T5Tokenizer, T5ForConditionalGeneration

model_save_path = '/home/onyxia/work/projet_NN2025_title_movie_generator/model'
tokenizer = T5Tokenizer.from_pretrained(model_save_path)
model = T5ForConditionalGeneration.from_pretrained(model_save_path)

# Résumé à donner au modèle
summary = """In a dystopian future where emotions are suppressed by a totalitarian regime, 
    a young woman named Elara discovers an underground movement that seeks to restore feelings 
    to humanity. As she becomes more involved, she learns about the power of love, hope, and rebellion. 
    With the help of a charismatic leader and a group of misfits, Elara must confront her own fears 
    and fight against the oppressive system to reclaim the right to feel. The journey leads her to 
    unexpected alliances and dangerous confrontations, ultimately challenging the very fabric of society."""

# Tokenisation
input_ids = tokenizer.encode(summary, return_tensors='pt')

# Génération du titre
with torch.no_grad():
    generated_ids = model.generate(
        input_ids,
        max_length=10,  # Longueur maximale du titre
        min_length=3,   # Longueur minimale du titre
        num_beams=5,    # Utilisation de beam search pour une meilleure qualité
        temperature=1.0,  # Valeur de température pour le sampling
        top_k=50,        # Limite le choix aux 50 mots les plus probables
        top_p=0.9,       # Choisit parmi les mots qui représentent 90% de la probabilité cumulée
        do_sample=True,  # Active le sampling
        early_stopping=True
    )

# Décodage du titre généré
title = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
print(f"Generated title : {title}")

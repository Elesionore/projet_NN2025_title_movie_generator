"""
Programme qui fine-tune le modèle T5-small afin de générer des titres de films à partir de résumés de films.
Le modèle est enregistré dans le dossier model/ et peut être ensuite utilisé pour générer des titres.
"""

import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration


###################### Importation du modèle #######################
model_name = "t5-small"  # Possible aussi avec "t5-base" ou "t5-large" mais trop lourd pour notre usage
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


###################### Préparation du dataset pour le modèle #######################

# Chargement les données que nous avons préparées dans prepared_data.py
df = pd.read_csv('/home/onyxia/work/result/movie_data.csv', sep="\t") 

# Préparation des entrées et des sorties
inputs = df['Plot Summary'].tolist()
outputs = df['Movie Title'].tolist()

# Tokenisation
input_encodings = tokenizer(inputs, padding=True, truncation=True, return_tensors="pt")
output_encodings = tokenizer(outputs, padding=True, truncation=True, return_tensors="pt")


####################### Partie Fine-tuning du modèle #######################

# Création d'un classe pour la gestion des données dans le modèle
class MovieDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    # On récupère les éléments d'encodage et les labels pour un index donné.
    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = self.labels[idx]
        return item

    # On retourne la taille du dataset
    def __len__(self):
        return len(self.labels)

# Création du dataset et du DataLoader pour gérer les lots de données pendant l'entraînement.
dataset = MovieDataset(input_encodings, output_encodings['input_ids'])
loader = DataLoader(dataset, batch_size=8, shuffle=True)

#### Entraînement du modèle : ####
model.train()
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

for epoch in range(3):
    for batch in loader:
        optimizer.zero_grad()                               # Initialisation du gradient
        input_ids = batch['input_ids']                      # Entrées pour l'entraînement
        labels = batch['labels']                            # Labels pour l'entraînement
        outputs = model(input_ids=input_ids, labels=labels) # Sorties du modèle
        loss = outputs.loss                                 # Calcul de la loss
        loss.backward()                                     # Rétropropagation
        optimizer.step()                                    # Mise à jour des poids
        print(f"Loss: {loss.item()}")                       # Affichage de la loss

# Enregistrement du modèle et du tokenizer
model_save_path = '/home/onyxia/work/projet_NN2025_title_movie_generator/model' 
model.save_pretrained(model_save_path)
tokenizer.save_pretrained(model_save_path)


####################### Génération de titres avec une longueur limitée #######################

# Exemple avec un titre généré à partir d'un résumé de film : 

model.eval()
summary = """In a near-future world where memories can be extracted and sold, a skilled memory thief named
    Alex discovers a hidden conspiracy while attempting to steal the memories of a powerful politician. 
    As Alex delves deeper, he uncovers a plot that threatens to erase the past and manipulate the future. 
    With the help of a rebellious hacker and a former detective haunted by his own memories, Alex must 
    navigate a web of deception and danger to expose the truth. As they race against time, they learn that 
    some memories are worth fighting for, and the echoes of the past can shape the destiny of tomorrow."""

# On tokenise le résumé :
input_ids = tokenizer.encode(summary, return_tensors='pt')

# Génération du titre à partir du résumé donné, 
# avec des paramètres de génération spécifiques pour améliorer la qualité du titre généré :
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

# Décodage et affichage du titre généré
title = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
print(f"Generated title : {title}")

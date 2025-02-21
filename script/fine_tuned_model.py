from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd
from torch.utils.data import DataLoader, Dataset
import torch


###################### Importation du modèle :
model_name = "t5-small"  # ou "t5-base", "t5-large" selon vos besoins
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


###################### Préparation du dataset pour le modèle :

# Charger les données
df = pd.read_csv('/home/onyxia/work/result/movie_data.csv', sep="\t")  # Remplacez par le chemin de votre fichier

# Préparer les entrées et les sorties
inputs = df['Plot Summary'].tolist()
outputs = df['Movie Title'].tolist()

# Tokenisation
input_encodings = tokenizer(inputs, padding=True, truncation=True, return_tensors="pt")
output_encodings = tokenizer(outputs, padding=True, truncation=True, return_tensors="pt")


####################### Partie Fine-tuning du modèle :

class MovieDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)

dataset = MovieDataset(input_encodings, output_encodings['input_ids'])
loader = DataLoader(dataset, batch_size=8, shuffle=True)

# Entraînement
model.train()
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

for epoch in range(3):  # Nombre d'époques
    for batch in loader:
        optimizer.zero_grad()
        input_ids = batch['input_ids']
        labels = batch['labels']
        outputs = model(input_ids=input_ids, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        print(f"Loss: {loss.item()}")


# Génération de titres avec une longueur limitée
model.eval()
summary = """In a near-future world where memories can be extracted and sold, a skilled memory thief named
    Alex discovers a hidden conspiracy while attempting to steal the memories of a powerful politician. As Alex delves deeper,
    he uncovers a plot that threatens to erase the past and manipulate the future. With the help of a
    rebellious hacker and a former detective haunted by his own memories, Alex must navigate a web of deception and danger to expose the truth.
    As they race against time, they learn that some memories are worth fighting for, and the echoes of the past can shape the destiny of tomorrow."""

input_ids = tokenizer.encode(summary, return_tensors='pt')

with torch.no_grad():
    generated_ids = model.generate(
        input_ids,
        max_length=10,  # Longueur maximale du titre
        min_length=3,   # Longueur minimale du titre
        num_beams=5,    # Utilisation de beam search pour une meilleure qualité
        early_stopping=True
    )

title = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
print(f"Generated title : {title}")

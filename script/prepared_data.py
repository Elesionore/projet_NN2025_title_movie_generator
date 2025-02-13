"""
Ce programme permet de fusionner les fichiers movie.metadata.tsv et plot_summaries.txt afin que nous puissions avoir un seul fichier contenant les informations sur les films et leurs résumés.

Utilisation :
- python prepared_data.py
"""
import pandas as pd
import os

# Nous allons lire nos deux fichiers de données et les fusionner en un seul fichier
movie_metadata = pd.read_csv("../data/movie.metadata.tsv", sep="\t", header=0)
plot_summaries = pd.read_csv("../data/plot_summaries.txt", sep="\t", header=None, names=["Wikipedia Movie ID", "Plot Summary"])

# Nous allons merger les deux fichiers sur Wikipedia Movie ID
merged_data = pd.merge(movie_metadata, plot_summaries, on="Wikipedia Movie ID")

# Ici nous sélectionnons les colonnes que nous voulons garder
merged_data = merged_data[["Wikipedia Movie ID", "Movie Title", "Plot Summary"]]

# Nous allons créer le dossier "result" s'il n'existe pas
if not os.path.exists("../result"):
    os.makedirs("../result")

# Nous allons enregistrer le fichier fusionné dans le dossier "result"
merged_data.to_csv("../result/movie_data.csv", index=False, sep="\t")

print("🥳 Le fichier est sauvegardé dans ../result/movie_data.csv 🥳")
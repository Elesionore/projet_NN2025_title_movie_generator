<img src="./assets/img/tiger.png" alt="Logo du projet" width="200"/>


Ce projet de groupe a été effectué dans le cadre du cours Réseau de neurones et Interfaces pour le web enseigné par M. Loïc Grobol au sein du master TAL (Université Paris Nanterre).

## Équipe

Ce projet a été réalisé par :
- **AUGUSTYN Patricia** : [GitHub](https://github.com/PatriciaAugustyn)
- **BRISSET Lise** : [GitHub](https://github.com/Lise-Brisset)
- **KOROL Solomia** : [Github](https://github.com/Elesionore)

## Objectifs

L'objectif de ce projet est de créer un générateur de titres de films basé sur les résumés de films.

## Utilisation

1. Créer un environnement virtuel : 
```
python3 -m venv venv
```

2. Activer son environnement virtuel :
```
source venv/bin/activate
```
3. Installer les librairies
``` 
pip install -r requirements.txt
```

1. Lancer notre application :
```
uvicorn main:app
```

Une fois le serveur lancé, vous pouvez accéder à l'application en cliquant sur le lien suivant dans votre navigateur : [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Important

Lorsque vous lancez l'application avec **uvicorn**, il est essentiel de s'assurer qu'aucune autre fenêtre de terminal n'est ouverte avec des processus actifs. Si d'autres applications ou serveurs sont en cours d'exécution dans le terminal, cela pourrait provoquer des erreurs au démarrage du serveur.

Pour éviter cela, suivez ces étapes :
1. Fermez toutes les autres instances de terminal ouvertes.
2. Lancez **uvicorn** dans une fenêtre de terminal propre, sans autres processus en cours.

Voici un exemple de commande pour démarrer le serveur :
```
uvicorn main:app --reload
```
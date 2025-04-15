# Prénomator 3000 EXTRA MAX V2.0

Le `Prénomator 3000 EXTRA MAX V2.0` est un programme très puissant se sérvant d'[open data](www.data.gouv.fr) pour vous offrir multes fonctionnalités et données statistiques en relation avec les prénoms en France.

## Fonctionnalités

- Intérface graphique utilisant CustomTkinter
- Permet de trouver un prénom et découvrir sa popularité au fil des années (en terme de naissances) dans l'onglet **Recherche**
- Permet de visualizer les tendances générales des naissances en France dans l'onglet **Statistiques**
- Permet d'analyser l'évolution d'un prénom spécifique (tendances croissantes, décroissantes) dans l'onglet 
- Vous fait découvrir les classements des prénoms les plus populaires par année (en fonction du nombre de naissances) dans l'onglet **Classement**
- Des modes d'affichage clairs et sombres, vos yeux méritent le méilleur!
- Les chemins des ressources sont gérés pour fonctionner dans un environnement compilé nous permettant d'ainsi vous fournir un ZIP contenant tout le nécessaire pour la bonne execution du programme (même si vous avez pas python ou manquez certaines dépendances), facilitant ainsi l'utilisation du `Prénomator 3000 EXTRA MAX V2.0`
- Télécharge lui-même les fichiers auxiliaires nécessaires à son éxécution (fichiers CSV, txt...) et s'initialize par lui-même permettant de ne prendre qu'un espace de stockage intial infime


## Prérequis

- Python 3.10 ou supérieur
- Bibliothèques Python :
    - fichier `requirements.txt`
## Installation & Utilisation

### Option 1: ZIP (Plus sûre pour Windows)

1. Télechargez l'archive zip de la derniere version sur github (à droite par rapport à la page du projet)

2. Extrayez le contenu

3. Trouvez prenoms.exe et executez le

### Option 2: Clonage (Moins sûre)

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/BzaleTheBlaze/python_csv_to_SQL.git
   cd python_csv_to_SQL
   ```

2. Installez les dépendances nécessaires :
   ```bash
   pip install -r requirements.txt
   ```

3. Executez et poursuivez avec la GUI
   ```bash
   python prenoms.py
   ```

## Configuration

Le fichier `config.ini` permet de définir les paramètres suivants :
- Chemins des fichiers de données.
- URLs des fichiers à télécharger.
- Répertoires de stockage temporaire.
> Attention: le modifier sans éxperience/à l'aveugle peut résulter dans la corruption du programme
---
Pour toute question ou assistance, veuillez contacter <contact@bzale.com>.

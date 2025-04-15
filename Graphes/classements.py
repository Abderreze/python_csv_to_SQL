import sqlite3
import matplotlib.pyplot as plt

def classements(annee: str, db_prenoms: str) -> dict:
    """Récupère le top 10 des prénoms par sexe pour une année donnée.

    Args:
        annee (str): L'année de recherche (format 'YYYY').
        db_prenoms (str): Chemin vers la base de données SQLite des prénoms.

    Returns:
        dict: Dictionnaire contenant deux clés :
            - 'masculin': Liste de tuples (prénom, nombre) pour le top 10 masculin
            - 'feminin': Liste de tuples (prénom, nombre) pour le top 10 féminin

    Exemple:
        >>> classements('2020', 'prenoms.db')
        {
            'masculin': [('Léo', 4500), ('Gabriel', 4200), ...],
            'feminin': [('Jade', 3800), ('Louise', 3700), ...]
        }

    Note:
        - Exclut automatiquement les prénoms rares (marqués '_PRENOMS_RARES')
        - Les sexes sont codés : 1 (masculin), 2 (féminin) dans la base
    """
    # Connexion à la base de données
    conn = sqlite3.connect(db_prenoms)
    cursor = conn.cursor()

    # Dictionnaire pour stocker les résultats
    tops_10 = {}

    # Recherche pour les deux sexes (1: masculin, 2: féminin)
    for i in range(1, 3):
        cursor.execute("""
            SELECT preusuel, nombre 
            FROM prenoms
            WHERE annais = ? AND sexe = ? AND preusuel != '_PRENOMS_RARES'
            ORDER BY nombre DESC
            LIMIT 10;
        """, (annee, i))
        
        # Conversion des résultats en liste de tuples (prénom, nombre)
        top_pour_un_sexe = [(prenom, nombre) for prenom, nombre in cursor.fetchall()]
        
        # Catégorisation des résultats
        categorie = "masculin" if i == 1 else "feminin"
        tops_10[categorie] = top_pour_un_sexe

    # Fermeture propre de la connexion
    conn.close()
    
    return tops_10

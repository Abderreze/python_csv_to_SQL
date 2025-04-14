import sqlite3
import matplotlib.pyplot as plt

def classements(annee: str, db_prenoms: str):
    conn = sqlite3.connect(db_prenoms)
    cursor = conn.cursor()

    tops_10 = {}

    for i in range(1, 3):
        cursor.execute("""
            SELECT preusuel, nombre 
            FROM prenoms
            WHERE annais = ? AND sexe = ? AND preusuel != '_PRENOMS_RARES'
            ORDER BY nombre DESC
            LIMIT 10;
        """, (annee, i, ))
        top_pour_un_sexe = [(prenom, nombre) for prenom, nombre in cursor.fetchall()]
        categorie = "masculin" if i == 1 else "feminin"
        tops_10[categorie] = top_pour_un_sexe
    conn.close()
    return tops_10

import csv
import sqlite3 

liaison = sqlite3.connect("prenoms.db")
curseur = liaison.cursor()

with open("nat2022.csv", 'r', encoding='UTF-8') as f:
    csv_read = csv.reader(f, delimiter=';')

    curseur.execute("""
        CREATE TABLE IF NOT EXISTS prenoms (
            sexe INTEGER,
            preusuel TEXT,
            annais TEXT,
            nombre INTEGER
        )
    """)

    next(csv_read)

    for ligne in csv_read:
        curseur.execute("""
            INSERT INTO prenoms (sexe, preusuel, annais, nombre)
            VALUES (?, ?, ?, ?)    
        """, (int(ligne[0]), ligne[1], ligne[2], int(ligne[3])))

    liaison.commit() # on valide

liaison.close()

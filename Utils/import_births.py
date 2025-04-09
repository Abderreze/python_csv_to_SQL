import csv
import sqlite3
import sys
import requests
import os
from Utils.path import resource_path
from Utils.unzip import unzip_file

def create_births_table(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prenoms (
            sexe INTEGER,
            preusuel TEXT,
            annais TEXT,
            nombre INTEGER
        )
    """)
    connection.commit()
    connection.close()

def import_csv_sql_births(db_path, csv_file_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    with open(csv_file_path, 'r', encoding='UTF-8') as f:
        csv_read = csv.reader(f, delimiter=';')

        next(csv_read)

        for ligne in csv_read:
            cursor.execute("""
                INSERT INTO prenoms (sexe, preusuel, annais, nombre)
                VALUES (?, ?, ?, ?)    
            """, (int(ligne[0]), ligne[1], ligne[2], int(ligne[3])))

    connection.commit()
    connection.close()



def import_births_to_sql(db_path, data_dir, file_url):
    if file_url:
        try:
            response = requests.get(file_url)
            response.raise_for_status()
            births_zip_path = os.path.join(data_dir, resource_path("naissances2022.zip"))
            birth_csv_path = os.path.join(data_dir, resource_path("nat2022.csv"))
            with open(births_zip_path, "wb") as f:
                f.write(response.content)
            
            if unzip_file(births_zip_path, data_dir):
                if os.path.exists(birth_csv_path):
                    create_births_table(db_path)
                    import_csv_sql_births(db_path, birth_csv_path)
                    os.remove(births_zip_path)
                    os.remove(birth_csv_path)
                else:
                    sys.stderr.write(f"Err: Le fichier nat2022.csv n'a pas été trouvé")
                    return False
            else:
                sys.stderr.write(f"Err: La décompression de l'archive des naissances à échoué")
                return False
        except requests.exceptions.RequestException as e:
            sys.stderr.write(f"Err. lors du téléchargement du fichier ZIP des naissances: {e}")
            return False
    else:
        sys.stderr.write("URL pour le fichier ZIP des naissances non configurée dans config.ini")
        return False

import csv
import sqlite3
import sys
import requests
import os
from Utils.unzip import unzip_file

def create_births_table(db_path):
    """
    Crée une table 'prenoms' dans la base de données SQLite si elle n'existe pas.

    ARGUMENTS
        db_path: (str), chemin vers la base de données SQLite.
    """
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prenoms (
                sexe INTEGER,
                preusuel TEXT,
                annais TEXT,
                nombre INTEGER
            )
        """)
    except Exception as e:
        print(e)
    finally:
        connection.commit()
        connection.close()

def import_csv_sql_births(db_path, csv_file_path):
    """
    Importe les données d'un fichier CSV dans la table 'prenoms' de la base de données.

    ARGUMENTS
        db_path: (str), chemin vers la base de données SQLite.
        csv_file_path: (str), chemin vers le fichier CSV contenant les données.
    """
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        with open(csv_file_path, 'r', encoding='UTF-8') as f:
            csv_read = csv.reader(f, delimiter=';')
            next(csv_read)  # Ignore la première ligne (en-têtes)
            for ligne in csv_read:
                cursor.execute("""
                    INSERT INTO prenoms (sexe, preusuel, annais, nombre)
                    VALUES (?, ?, ?, ?)    
                """, (int(ligne[0]), ligne[1], ligne[2], int(ligne[3])))
    except Exception as e:
        print(e)
    finally:
        connection.commit()
        connection.close()

def import_births_to_sql(db_path, data_dir, file_url):
    """
    Télécharge un fichier ZIP contenant les données de naissances, le décompresse,
    puis importe les données dans la base de données SQLite.

    ARGUMENTS
        db_path: (str), chemin vers la base de données SQLite.
        data_dir: (str), répertoire où les fichiers seront temporairement stockés.
        file_url: (str), URL du fichier ZIP à télécharger.

    RETOURNE
        (bool): False en cas d'erreur, sinon rien.
    """
    if file_url:
        try:
            response = requests.get(file_url)
            response.raise_for_status()
            births_zip_path = os.path.join(data_dir, "naissances2022.zip")
            birth_csv_path = os.path.join(data_dir, "nat2022.csv")
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
                sys.stderr.write(f"Err: La décompression de l'archive des naissances a échoué")
                return False
        except requests.exceptions.RequestException as e:
            sys.stderr.write(f"Err. lors du téléchargement du fichier ZIP des naissances: {e}")
            return False
    else:
        sys.stderr.write("URL pour le fichier ZIP des naissances non configurée dans config.ini")
        return False

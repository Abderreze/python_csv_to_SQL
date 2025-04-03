import re
import sqlite3
import csv

# A NE TOUCHER EN AUCUN CAS CE PATTERN REGEX, IL MARCHE, C'EST TOUT CE QUI COMPTE (M'A PRIS DES HEURES)


pattern = r"^([^*]*)(?:\*)([^\/]*)(?:\/)\s*(\d{1})(\d{8})([\dA-Z]{0,5})\s*([A-Z\- '0-9,.°\(\)\/]{1,30})\s*(\D+\s*)?(\d{8})([\dA-Z]{5}|\s*)(.*)\s*$"

def create_table():
    connection = sqlite3.connect("prenoms.db")
    cursor = connection.cursor()

    # Si doutes concernant le type des données, n'en ayez aucun, tout est fait pour marcher dans tous
    # les cas qu'on risque de rencontrer
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deces (
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        sexe CHAR(1) CHECK (sexe IN ('H', 'F')),
        date_naissance TEXT NOT NULL,
        code_lieu_naissance TEXT NOT NULL,
        commune_naissance TEXT NOT NULL,
        pays_naissance TEXT NOT NULL,
        date_deces TEXT NOT NULL,
        code_lieu_deces TEXT NOT NULL,
        numero_acte TEXT NOT NULL,
        annee_deces TEXT NOT NULL
    )
    """)
    connection.commit()
    connection.close()


def gen_deces_csv(year):

    connection = sqlite3.connect("prenoms.db")
    cursor = connection.cursor()

    with open(f"deces-{year}.csv", "w", newline='' ,encoding="UTF-8") as csvfile:

        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["nom", "prenom", "sexe", "date_naissance", "code_lieu_naissance", "commune_naissance", "pays_naissance", "date_deces", "code_lieu_deces", "numero_acte", "annee_deces"])


        with open(f"deces-{year}.txt", "r", encoding="UTF-8") as f:

            for line in f:

                match = re.match(pattern, line)

                # test théorique, en vérité le regex matche tous les cas
                if match:

                    last = match.group(1)
                    first = match.group(2)
                    sex = "F" if int(match.group(3)) == 2 else "H"
                    birth_date = match.group(4)
                    birth_place_code = match.group(5)
                    birth_place_name = match.group(6).strip()
                    birth_country = match.group(7).strip() if match.group(7) else ""
                    death_date = match.group(8)
                    death_place_code = match.group(9)
                    death_certificate_num = match.group(10).strip()
                    death_year = death_date[0:4] if death_date[0:4] != "0000" else "2024"

                    csv_writer.writerow([last, first, sex, birth_date, birth_place_code, birth_place_name, birth_country, death_date, death_place_code, death_certificate_num, death_year])

create_table()
for i in range(2019, 2025):
    gen_deces_csv(i)

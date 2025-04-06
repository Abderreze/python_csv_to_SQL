#!/usr/bin/env python3
import argparse
import os
import zipfile

parser = argparse.ArgumentParser(description="Projet CSV vers SQL")

parser.add_argument("-i", "--init", action="store_true", help="Initialize le programme, en créant les .csv et .db nécessaires à l'éxecution correcte du programme")
parser.add_argument("--gen-csv", action="store_true", help="Genère uniquement les fichiers CSV")
parser.add_argument("--gen-db", action="store_true", help="Genère uniquement la base de données .db à partir des .csv existants")
parser.add_argument("--rebuild-db", action="store_true", help="Supprime la base de données .db existante et la regenère")
parser.add_argument("--db-path", type=str, help="Spécifie le chemin d'accès pour le fichier de base de données .db")
# coté dev/ pour partager
parser.add_argument("-z, --gen-zip", action="store_true", help="Compresse et rassemble les fichiers sources nécessaires à la création de la base de données")
# potentiellement
# parser.add_argument("-v", "--verbose")

args = parser.parse_args()

# verifier pour des combinaisons incompatibles
if args.init:
    if args.gen_csv or args.gen_db or args.rebuild_db or args.gen_zip:
        parser.error("--init ne peut pas être utilisé avec --gen-csv, --gen-db, --rebuild-db, ou --gen-zip.")

elif args.gen_csv:
    if args.init or args.gen_db or args.rebuild_db or args.gen_zip or args.db_path:
        parser.error("--gen-csv ne peut pas être utilisé avec --init, --gen-db, --rebuild-db, --db-path, ou --gen-zip.")

elif args.gen_db:
    if args.init or args.gen_csv or args.rebuild_db or args.gen-zip:
        parser.error("--gen-db ne peut pas être utilisé avec --init, --gen-csv, --rebuild-db, ou --gen-zip.")

elif args.rebuild_db:
    if args.init or args.gen_csv or args.gen_db or args.gen-zip:
        parser.error("--rebuild-db ne peut pas être utilisé avec --init, --gen-csv, --gen-db, ou --gen-zip.")

elif args.gen_zip:
    if args.init or args.gen_csv or args.gen_db or args.rebuild_db:
        parser.error("--gen-zip ne peut pas être utilisé avec --init, --gen-csv, --gen-db, ou --rebuild-db.")

# Si aucune de ces options exclusives n'est choisie, on peut supposer qu'on lance l'interface graphique
else:
    print("Lancement de l'interface graphique...")
    # Code pour lancer l'interface graphique


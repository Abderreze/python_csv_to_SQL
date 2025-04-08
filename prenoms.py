#!/usr/bin/env python3
# import argparse
import configparser
import os
import customtkinter as ctk

from Utils.config import set_setting
from Utils.import_births import import_births_to_sql
from Utils.import_deaths import import_deaths_to_sql
from Utils.import_trivia import import_trivia_to_sql



# parser = argparse.ArgumentParser(description="Projet CSV vers SQL")
#
# parser.add_argument("-i", "--init", action="store_true", help="Initialize le programme, en créant les .csv et .db nécessaires à l'éxecution correcte du programme")
# parser.add_argument("--gen-csv", action="store_true", help="Genère uniquement les fichiers CSV")
# parser.add_argument("--gen-db", action="store_true", help="Genère uniquement la base de données .db à partir des .csv existants")
# parser.add_argument("--rebuild-db", action="store_true", help="Supprime la base de données .db existante et la regenère")
# parser.add_argument("--db-path", type=str, help="Spécifie le chemin d'accès pour le fichier de base de données .db")
# # coté dev/ pour partager
# parser.add_argument("-z, --gen-zip", action="store_true", help="Compresse et rassemble les fichiers sources nécessaires à la création de la base de données")
# parser.add_argument("-c", "--config", nargs='+', help="Gérer la configuration (get <clé> ou set <sélection> <clé> <valeur>)")
#
# args = parser.parse_args()
# verifier pour des combinaisons incompatibles
# if args.init:
#     if args.gen_csv or args.gen_db or args.rebuild_db or args.gen_zip:
#         parser.error("--init ne peut pas être utilisé avec --gen-csv, --gen-db, --rebuild-db, ou --gen-zip.")
#
# elif args.gen_csv:
#     if args.init or args.gen_db or args.rebuild_db or args.gen_zip or args.db_path:
#         parser.error("--gen-csv ne peut pas être utilisé avec --init, --gen-db, --rebuild-db, --db-path, ou --gen-zip.")
#
# elif args.gen_db:
#     if args.init or args.gen_csv or args.rebuild_db or args.gen-zip:
#         parser.error("--gen-db ne peut pas être utilisé avec --init, --gen-csv, --rebuild-db, ou --gen-zip.")
#
# elif args.rebuild_db:
#     if args.init or args.gen_csv or args.gen_db or args.gen-zip:
#         parser.error("--rebuild-db ne peut pas être utilisé avec --init, --gen-csv, --gen-db, ou --gen-zip.")
#
# elif args.gen_zip:
#     if args.init or args.gen_csv or args.gen_db or args.rebuild_db:
#         parser.error("--gen-zip ne peut pas être utilisé avec --init, --gen-csv, --gen-db, ou --rebuild-db.")

# Si aucune de ces options exclusives n'est choisie, on peut supposer qu'on lance l'interface graphique
# else:
#     print("Lancement de l'interface graphique...")
#     # Code pour lancer l'interface graphique
#

# on charge le fichier de configuration
config = configparser.ConfigParser()
config.read('config.ini')
#
# database_path = config.get("paths", "database_path", fallback="Tables/prenoms.db")
# data_directory = config.get("paths", "data_directory", fallback="./Tables")
# deaths_urls_str = config.get("remote", "deaths_urls", fallback="")
# deaths_urls = [url.strip() for url in deaths_urls_str.split(',')] if deaths_urls_str else []
# births_url = config.get("remote", "births_url", fallback="")
# first_deaths_year = config.get("remote", "first_deaths_year", fallback=2019)
# last_deaths_year = config.get("remote", "last_deaths_year", fallback=2024)

def download_and_process_data():
    db_path = config.get("paths", "database_path")
    data_dir = config.get("paths", "data_directory")
    trivia_url = config.get("remote", "trivia_url")
    births_url = config.get("remote", "births_url")
    deaths_urls_str = config.get("remote", "deaths_urls")
    deaths_urls = [url.strip() for url in deaths_urls_str.split(',')]
    first_deaths_year = config.get("remote", "first_deaths_year")
    os.makedirs(data_dir, exist_ok=True)
    import_births_to_sql(db_path, data_dir, births_url)
    import_deaths_to_sql(db_path, data_dir, deaths_urls, first_deaths_year)
    import_trivia_to_sql(db_path, data_dir, trivia_url) 
    return True

def ask_for_existing_path():
    path_window = ctk.CTkToplevel()
    path_window.title("Chemin BDD")
    path_label = ctk.CTkLabel(path_window, text="Veuillez spécifier le chemin du fichier de base de données existant:")
    path_label.pack(padx=20, pady=10)
    path_entry = ctk.CTkEntry(path_window)
    path_entry.pack(padx=20, pady=5)

    def save_path():
        new_path = path_entry.get()
        if os.path.exists(new_path) and new_path.endswith(".db"):
            set_setting("config.ini", "paths", "database_path", new_path)
            path_window.destroy()
        else:
            error_label = ctk.CTkLabel(path_window, text="Chemin invalide ou fichier non '.db'.")
            error_label.pack(padx=20, pady=5)

    save_button = ctk.CTkButton(path_window, text="Sauvegarder le chemin", command=save_path)
    save_button.pack(padx=20, pady=10)
    path_window.wait_window()

def check_gen_db(database_path):
    if not os.path.exists(database_path):
        def display_notification(title, value):
            success_window = ctk.CTkToplevel()
            success_window.title(title)
            success_label = ctk.CTkLabel(success_window, text=value)
            success_label.pack(padx=20, pady=10)
            return success_window

        def handle_choice(choice):
            choice_window.destroy()
            if choice == "Spécifier un chemin existant":
                ask_for_existing_path()
                if download_and_process_data():
                    hSuccess = display_success()

            elif choice == "Générer au chemin par défaut":
                if download_and_process_data():
                    hSuccess = display_notification("Succès", "La base de données a été téléchargée et créée avec succès!")
                else:
                    hError = display_notification("Erreur", "La création de la base de données a échoué. Veuillez vérifier votre connexion internet et la configuration")

            # elif choice == "Spécifier un nouveau chemin pour la générer":
            #     ask_for_new_path()


        choice_window = ctk.CTk()
        choice_window.title("Base de données manquante!!!")
        label = ctk.CTkLabel(choice_window, text="La base de données est introuvable dans le chemin par défaut")
        label.pack(padx=20, pady=10)
        label_question = ctk.CTkLabel(choice_window, text="Sohuaitez-vous spécifier un autre chemin la génerer ?")
        label_question.pack(padx=20, pady=5)
        options = ["Spécifier un chemin existant", "Générer au chemin par défaut", "Spécifier un nouveau chemin pour la générer"]
        option_menu = ctk.CTkOptionMenu(choice_window, values=options, command=handle_choice)
        option_menu.pack(padx=20, pady=10)
        
        choice_window.wait_window()
    return os.path.exists(database_path)



if __name__ == "__main__":

    database_path = config.get("paths", "database_path")

    if check_gen_db(database_path):
        print("yay")

#!/usr/bin/env python3
# import argparse
import configparser
import os
import customtkinter as ctk

from Utils.config import set_setting
from Utils.import_births import import_births_to_sql
from Utils.import_deaths import import_deaths_to_sql
from Utils.import_trivia import import_trivia_to_sql
from affichage_graphique import gui

# on charge le fichier de configuration
config = configparser.ConfigParser()
config.read('config.ini')

def download_and_process_data():
    # to make sure latest config is fetched
    db_path = config.get("paths", "database_path")
    data_dir = config.get("paths", "data_directory")
    trivia_url = config.get("remote", "trivia_url")
    births_url = config.get("remote", "births_url")
    deaths_urls_str = config.get("remote", "deaths_urls")
    deaths_urls = [url.strip() for url in deaths_urls_str.split(',')]
    first_deaths_year = config.get("remote", "first_deaths_year")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
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

def ask_for_new_path(db_path):


    path_window = ctk.CTkToplevel()
    path_window.title("Chemin de la nouvelle base de données")
    path_label = ctk.CTkLabel(path_window, text="Veuillez spécifier le chemin où créer la nouvelle base de données:")
    path_label.pack(padx=20, pady=10)
    path_entry = ctk.CTkEntry(path_window)
    path_entry.insert(0, db_path)
    path_entry.pack(padx=20, pady=5)

    def generate_at_path():
        new_path = path_entry.get()
        set_setting("config.ini", "paths", "database_path", new_path)
        path_window.destroy()
        if download_and_process_data():
            success_window = display_notification("Succès", "La base de données a été téléchargée et créée avec succès!")
        else:
            erreur_window = display_notification("Erreur", "La création de la base de données a échoué. Veuillez vérifier votre connexion internet et la configuration")

        
    generate_button = ctk.CTkButton(path_window, text="Générer la base de données ici", command=generate_at_path)
    generate_button.pack(padx=20, pady=10)
    path_window.wait_window()
    

def display_notification(title, value):
    success_window = ctk.CTkToplevel()
    success_window.title(title)
    success_label = ctk.CTkLabel(success_window, text=value)
    success_label.pack(padx=20, pady=10)
    return success_window


def check_gen_db(database_path, parent):
    if not os.path.exists(database_path):

        def handle_choice(choice):
            choice_window.destroy()
            if choice == "Spécifier un chemin existant":
                # a modifier
                ask_for_existing_path()

            elif choice == "Générer au chemin par défaut":
                if download_and_process_data():
                    hSuccess = display_notification("Succès", "La base de données a été téléchargée et créée avec succès!")
                else:
                    hError = display_notification("Erreur", "La création de la base de données a échoué. Veuillez vérifier votre connexion internet et la configuration")

            elif choice == "Spécifier un nouveau chemin pour la générer":
                db_path = config.get("paths", "database_path")
                ask_for_new_path(db_path)


        choice_window = ctk.CTkToplevel(parent) # a modifier
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

    db_path = config.get("paths", "database_path")
    app = ctk.CTk()

    if os.path.exists(db_path):
        hGui = gui(db_path, app)
    else:
        check_gen_db(db_path, app)
    app.mainloop()


    # if check_gen_db(db_path):
    #     print("yay")

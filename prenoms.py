#!/usr/bin/env python3
import configparser
import os
import customtkinter as ctk
import time
import threading

from Utils.config import set_setting
from Utils.import_births import import_births_to_sql
from Utils.import_deaths import import_deaths_to_sql
from Utils.import_trivia import import_trivia_to_sql
from Utils.path import resource_path
from affichage_graphique import gui

# on charge le fichier de configuration
config = configparser.ConfigParser()
config.read(resource_path('config.ini'))

def spinner(label, stop_event):
    chars = ['⣾','⣽','⣻','⢿','⡿','⣟', '⣯', '⣷']
    while not stop_event.is_set():
        for char in chars:
            if stop_event.is_set():
                break
            text = char + " Base de données en cours d'initialization"
            label.configure(text=text)
            label.update()  # Force the label to update immediately
            time.sleep(0.1)
    label.winfo_toplevel().destroy()
    return True



def initialize_db(parent):

    running_window = ctk.CTkToplevel(parent)
    running_window.title("Initialization base de données")
    running_label = ctk.CTkLabel(running_window, text="")
    running_label.pack(padx=20, pady=10)

    stop_event = threading.Event()


    download_thread = threading.Thread(target=download_and_process_data, args=(stop_event,), daemon=True)
    download_thread.start()

    return spinner(running_label, stop_event)

def download_and_process_data(stop_event):
    # to make sure latest config is fetched
    db_path = config.get("paths", "database_path")
    data_dir = config.get("paths", "data_directory")
    trivia_url = config.get("remote", "trivia_url")
    births_url = config.get("remote", "births_url")
    deaths_urls_str = config.get("remote", "deaths_urls")
    deaths_urls = [url.strip() for url in deaths_urls_str.split(',')]
    first_deaths_year = config.get("remote", "first_deaths_year")
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    import_births_to_sql(db_path, data_dir, births_url)
    import_deaths_to_sql(db_path, data_dir, deaths_urls, first_deaths_year)
    import_trivia_to_sql(db_path, data_dir, trivia_url) 
    stop_event.set()

def ask_for_existing_path(parent):
    path_window = ctk.CTkToplevel(parent)
    path_window.title("Chemin BDD")
    path_label = ctk.CTkLabel(path_window, text="Veuillez spécifier le chemin du fichier de base de données existant:")
    path_label.pack(padx=20, pady=10)
    path_entry = ctk.CTkEntry(path_window)
    path_entry.pack(padx=20, pady=5)

    def save_path():
        new_path = path_entry.get()
        if os.path.exists(new_path) and new_path.endswith(".db"):
            set_setting(resource_path("config.ini"), "paths", "database_path", new_path)
            config.read(resource_path("config.ini")) # pour mettre à jour les données
            path_window.destroy()
        else:
            error_label = ctk.CTkLabel(path_window, text="Chemin invalide ou fichier non '.db'.")
            error_label.pack(padx=20, pady=5)

    save_button = ctk.CTkButton(path_window, text="Sauvegarder le chemin", command=save_path)
    save_button.pack(padx=20, pady=10)
    path_window.wait_window()

def ask_for_new_path(parent, db_path):


    path_window = ctk.CTkToplevel(parent)
    path_window.title("Chemin de la nouvelle base de données")
    path_label = ctk.CTkLabel(path_window, text="Veuillez spécifier le chemin où créer la nouvelle base de données:")
    path_label.pack(padx=20, pady=10)
    path_entry = ctk.CTkEntry(path_window)
    path_entry.insert(0, db_path)
    path_entry.pack(padx=20, pady=5)

    def generate_at_path():
        new_path = path_entry.get()
        set_setting(resource_path("config.ini"), "paths", "database_path", new_path)
        config.read(resource_path("config.ini")) # mettre à jour
        path_window.destroy()
        if initialize_db(parent):
            success_window = display_notification(parent, "Succès", "La base de données a été téléchargée et créée avec succès!")
        else:
            erreur_window = display_notification(parent, "Erreur", "La création de la base de données a échoué. Veuillez vérifier votre connexion internet et la configuration")

        
    generate_button = ctk.CTkButton(path_window, text="Générer la base de données ici", command=generate_at_path)
    generate_button.pack(padx=20, pady=10)
    path_window.wait_window()
    

def display_notification(parent, title, value):
    success_window = ctk.CTkToplevel(parent)
    success_window.title(title)
    success_label = ctk.CTkLabel(success_window, text=value)
    success_label.pack(padx=20, pady=10)
    return success_window


def check_gen_db(parent, database_path):
    if not os.path.exists(database_path):

        choice_window = ctk.CTkToplevel(parent) # a modifier
        choice_window.title("Base de données manquante!!!")
        label = ctk.CTkLabel(choice_window, text="La base de données est introuvable dans le chemin par défaut")
        label.pack(padx=20, pady=10)
        label_question = ctk.CTkLabel(choice_window, text="Sohuaitez-vous spécifier un autre chemin la génerer ?")
        label_question.pack(padx=20, pady=5)
        options = ["Spécifier un chemin existant", "Générer au chemin par défaut", "Spécifier un nouveau chemin pour la générer"]
        selected_option = ctk.StringVar(value=options[1])
        option_menu = ctk.CTkOptionMenu(choice_window, values=options, variable=selected_option)
        option_menu.pack(padx=20, pady=10)

        def handle_choice():
            choice = selected_option.get()
            choice_window.destroy()
            if choice == "Spécifier un chemin existant":
                ask_for_existing_path(parent)
            elif choice == "Générer au chemin par défaut":
                if initialize_db(parent):
                    hSuccess = display_notification(parent, "Succès", "La base de données a été téléchargée et créée avec succès!")
                else:
                    hError = display_notification(parent, "Erreur", "La création de la base de données a échoué. Veuillez vérifier votre connexion internet et la configuration")

            elif choice == "Spécifier un nouveau chemin pour la générer":
                db_path = config.get("paths", "database_path")
                ask_for_new_path(parent, db_path)


        confirm_button = ctk.CTkButton(choice_window, text="Confirmer", command=handle_choice)
        confirm_button.pack(padx=20, pady=10)

        choice_window.wait_window()

        return os.path.exists(config.get("paths", "database_path"))
        
    return True


if __name__ == "__main__":

    db_path = config.get("paths", "database_path")
    app = ctk.CTk()
    if os.name == "posix":
        app.withdraw() # on cache la fenêtre principale au début

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    if check_gen_db(app, db_path):
        if os.name == "posix":
            app.deiconify()
        gui(app, config.get("paths", "database_path")) # potentiellement changé depuis
    else:
        hError = display_notification(app, "Erreur", "La base de données n'a pas pu être chargée ou créée. L'application va fermer.")
        app.after(3000, app.destroy)

    if app.winfo_exists():
        # selon système, le processus pour mettre l'application en plein-écran change
        if os.name == 'posix':
            app.after(0, lambda: app.attributes('-zoomed', True))
        elif os.name == 'nt':
            app.after(0, lambda: app.state('zoomed'))

        app.mainloop()

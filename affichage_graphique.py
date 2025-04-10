import os #permet la vérification de si c'est un windows ou autre
import customtkinter as ctk
import sqlite3
import matplotlib #librairie permettant la création de graphe
import csv
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import randint
from PIL import Image, ImageTk
from Graphes.graphe_de_ton_prenom import graphe_prenom
from Graphes.classement import classements
from collections import defaultdict
from Utils.path import resource_path

def gui(root, db_prenoms):
    matplotlib.use('Agg')

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root.title("Prénomator 3000 EXTRA MAX V2.0")

    main_container = ctk.CTkFrame(root, corner_radius=0)
    main_container.pack(side="right", expand=True, fill="both")

    home_frame = ctk.CTkFrame(main_container, corner_radius=0)
    search_frame = ctk.CTkFrame(main_container, corner_radius=0)
    stat_frame = ctk.CTkFrame(main_container, corner_radius=0)
    evolution_frame = ctk.CTkFrame(main_container, corner_radius=0)

    def show_home():
        search_frame.pack_forget()
        stat_frame.pack_forget()
        evolution_frame.pack_forget()
        home_frame.pack(fill="both", expand=True)

    def show_search():
        home_frame.pack_forget()
        stat_frame.pack_forget()
        evolution_frame.pack_forget()
        search_frame.pack(fill="both", expand=True)

    def show_stat():
        home_frame.pack_forget()
        search_frame.pack_forget()
        evolution_frame.pack_forget()
        stat_frame.pack(fill="both", expand=True)

    def show_evolution():
        home_frame.pack_forget()
        search_frame.pack_forget()
        stat_frame.pack_forget()
        evolution_frame.pack(fill="both", expand=True)

# Sidebar with icons
    home_icon = ctk.CTkImage(Image.open(resource_path("Icons/home.png")), size=(24, 24))
    search_icon = ctk.CTkImage(Image.open(resource_path("Icons/search.png")), size=(24, 24))
    stats_icon = ctk.CTkImage(Image.open(resource_path("Icons/stats.png")), size=(24, 24))
    evolution_icon = ctk.CTkImage(Image.open(resource_path("Icons/evolution.png")), size=(24, 24))

    sidebar = ctk.CTkFrame(root, width=80, fg_color="#1e1e1e", corner_radius=2)
    sidebar.pack(side="left", fill="y", padx=0, pady=0)
    sidebar.pack_propagate(False) #la taille de sidebar n'est pas définis par ces enfants (dans se cas les icons)

    ctk.CTkLabel(sidebar, text="", height=20).pack()

    home_button = ctk.CTkButton(
        sidebar,
        text="",
        image=home_icon,
        width=50,
        height=50,
        corner_radius=10,
        command=show_home,
        fg_color="#dddddd",
        hover_color="#ffffff"
    )
    home_button.pack(pady=10)

    search_button = ctk.CTkButton(
        sidebar,
        text="",
        image=search_icon,
        width=50,
        height=50,
        corner_radius=10,
        command=show_search,
        fg_color="#dddddd",
        hover_color="#ffffff"
    )
    search_button.pack(pady=10)

    stat_button = ctk.CTkButton(
        sidebar,
        text="",
        image=stats_icon,
        width=50,
        height=50,
        corner_radius=10,
        command=show_stat,
        fg_color="#dddddd",
        hover_color="#ffffff"
    )
    stat_button.pack(pady=10)

    evolution_button = ctk.CTkButton(
        sidebar,
        text="",
        image=evolution_icon,
        width=50,
        height=50,
        corner_radius=10,
        command=show_evolution,
        fg_color="#dddddd",
        hover_color="#ffffff"
    )
    evolution_button.pack(pady=10)

    switch_frame =ctk.CTkFrame(sidebar, fg_color="transparent")
    switch_frame.pack(side="right", padx=10)


    dark_mode_switch = ctk.CTkSwitch(switch_frame, text="", command=lambda: ctk.set_appearance_mode("dark" if dark_mode_switch.get() else "light"))
    dark_mode_switch.pack(pady=(0, 5))
    dark_mode_switch.select() # l'active de base

    # pour que le texte soit centré ET en dessous du switch
    switch_label = ctk.CTkLabel(
        switch_frame,
        text="Dark mode",
        text_color="white",
        anchor="center",
        justify="center"
    )
    switch_label.pack()

    show_home()

    # Frame principale de l'accueil
    main_frame = ctk.CTkFrame(search_frame, corner_radius=20)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

#===============================================================================================================
#                                           HOME
#
#===============================================================================================================
    contributors = ctk.CTkImage(Image.open(resource_path("Icons/contributors.png")), size=(240, 190))

    label_bonjour = ctk.CTkLabel(
        home_frame,
        text="Bonjour!",
        font=("TimesNewRoman", 35, "bold")
    )
    label_bonjour.pack()
    label_expliquation = ctk.CTkLabel(
        home_frame,
        text="Vous êtes actuellement sur le 'Prénomator 3000 EXTRA MAX V2.0' ou plus communément appelé le 'Prénomator'. \nVous avez été choisi.e afin de pouvoir" \
            " tester ce petit bijoux de technologie qu'est le Prénomator.\n\n"\
            " Voici les différents onglets disponible sur la sidebar du Prénomator :\n\n"\
            "•L'onglet 'Home' sur lequel vous êtes actuellement, vous pouver revenir si jamais vous avez besoin d'aide.\n"\
            "•L'onglet 'Search' vous permettra de chercher votre nom ou celui de vos amis afin de comparer qui est le plus populaire.\nN'oubliez pas de sélectionner le bon genre ainsi que de cliquer sur valider OU appuyer sur la touche 'enter'. \n"\
            "•L'onglet 'Statisitques' vous permettra de faire une comparaison avec les chutes ou les pics de naissance en France.\n"\
            "•L'onglet 'Évolution' vous permettra de voir si le nom est de plus en plus donné ou de moins en moins donné.\n \n"\
            "Si jamais vous n'aimez pas le noir (pour une raison que l'on ne jugera pas)\nvous pouvez désactiver le dark mode grâce au switch du même nom sur la sidebar.",
        font=("TimesNewRoman", 25)
    )
    label_expliquation.pack()

    contributors_label = ctk.CTkLabel(home_frame, image=contributors, text="")
    contributors_label.pack(pady=20)

#===============================================================================================================
#                                           SEARCH
#
#===============================================================================================================

# Frame gauche : Infos
    frame_info = ctk.CTkFrame(main_frame, corner_radius=15)
    frame_info.pack(side="left", padx=10, pady=10, fill="both", expand=True, anchor="w")

    label_info = ctk.CTkLabel(frame_info, text="Informations sur le prénom", font=("Arial", 16, "bold"))
    label_info.pack(pady=5)

    stats_label = ctk.CTkLabel(frame_info, text="", anchor="w", justify="left", font=("Arial", 14))
    stats_label.pack(pady=10, fill="both", expand=False)

# Frame droite : Graphiques
    frame_graphiques = ctk.CTkFrame(main_frame, corner_radius=15)
    frame_graphiques.pack(side="left", padx=10, pady=10, fill="both", expand=True)

    label_graphiques = ctk.CTkLabel(frame_graphiques, text="Graphique du prénom", font=("Arial", 16, "bold"))
    label_graphiques.pack(pady=5)

# Configuration du genre
    sexe_saisi = ctk.IntVar(value=1)

    sexe_frame = ctk.CTkFrame(frame_info)
    sexe_frame.pack(pady=5)

    radio_homme = ctk.CTkRadioButton(sexe_frame, text="Homme", variable=sexe_saisi, value=1)
    radio_homme.pack(side="left", padx=10)

    radio_femme = ctk.CTkRadioButton(sexe_frame, text="Femme", variable=sexe_saisi, value=2)
    radio_femme.pack(side="left", padx=10)

# Récupération des prénoms existants
    conn = sqlite3.connect(db_prenoms)
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT preusuel FROM prenoms;""")
    result = cursor.fetchall()
    prenoms_existants = [uplet[0] for uplet in result]
    cursor.execute("""SELECT DISTINCT preusuel, sexe FROM prenoms;""")
    result = cursor.fetchall()
    prenoms_sexe_existants = [uplet for uplet in result]
    conn.close()
    tmp = defaultdict(list)
    with open(resource_path('suggestions.csv'), mode='r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)

        for prefixe, prenom in reader:
            tmp[prefixe].append(prenom)
    prefixes_prenoms = dict(tmp)
    for liste in prefixes_prenoms.values():
        liste.sort()
    del tmp
# Données des prénoms sélectionnés
    prenoms_sexe_select = {}
    prenoms_select = []

# Fonction d'affichage du graphique
    def afficher_graphique(dico_prenoms_sexe):
        for widget in frame_graphiques.winfo_children():
            if widget not in [label_graphiques, zone_select_search]:
                widget.destroy()
        
        result, fig = graphe_prenom(db_prenoms, dico_prenoms_sexe)
        if result:
            canvas = FigureCanvasTkAgg(fig, master=frame_graphiques)
            canvas.draw()
            canvas.get_tk_widget().pack()

# Gestion de l'ajout de prénom
    def on_enter(event=None):
        prenom = search.get()
        sexe = sexe_saisi.get()
        sexe_str = "masculin" if sexe == 1 else "féminin"

        if (prenom, sexe_str) not in prenoms_select and (prenom.upper(), sexe) in prenoms_sexe_existants:
            prenoms_sexe_select[(prenom, sexe)] = f"#{randint(0x333333, 0xFFFFFF):06x}"
            prenoms_select.append((prenom, sexe_str))

        prenoms_deja_select.configure(values=[f"{p} {s}" for p, s in prenoms_select])
        afficher_graphique(prenoms_sexe_select)
        update_stats_display()

# Retrait d'un prénom
    def retire_prenom():
        prenom_a_retirer = prenoms_deja_select.get()
        if not prenom_a_retirer or ' ' not in prenom_a_retirer:
            return

        prenom, genre = prenom_a_retirer.split(' ')
        genre_code = 1 if genre == 'masculin' else 2
        tuple_dico = (prenom, genre_code)

        if (prenom, genre) in prenoms_select:
            prenoms_select.remove((prenom, genre))
        if tuple_dico in prenoms_sexe_select:
            del prenoms_sexe_select[tuple_dico]

        prenoms_deja_select.configure(values=[f"{p} {s}" for p, s in prenoms_select])
        afficher_graphique(prenoms_sexe_select)
        update_stats_display()

# Zone de sélection des prénoms
    zone_select_search = ctk.CTkFrame(frame_graphiques)
    zone_select_search.pack(pady=10)

    prenoms_deja_select = ctk.CTkComboBox(zone_select_search, values=[], width=200)
    prenoms_deja_select.set("")
    prenoms_deja_select.pack(side="left", padx=5)

    remove_button = ctk.CTkButton(
        zone_select_search,
        text="Retirer",
        command=retire_prenom,
        fg_color="#d9534f",
        hover_color="#c9302c",
        text_color="white"
    )
    remove_button.pack(side="left", padx=5)

# Affichage du graphique
    image_label = ctk.CTkLabel(frame_graphiques, text="")
    image_label.pack(pady=10)

# Récupération des statistiques
    def get_max_occurrence(prenom, genre_code):
        conn = sqlite3.connect(db_prenoms)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT annais, nombre
                FROM prenoms
                WHERE preusuel=? AND sexe=? AND annais != 'XXXX'
                ORDER BY nombre DESC
                LIMIT 1
            """, (prenom.upper(), genre_code))
            result = cursor.fetchone()

            if not result:
                return 0, "N/A"

            annee, nombre = result[0], result[1]

            if str(annee).strip().upper() == "XXXX":
                cursor.execute("""
                    SELECT annais, nombre
                    FROM prenoms
                    WHERE preusuel=? AND sexe=? AND annais != 'XXXX'
                    ORDER BY nombre DESC
                    LIMIT 1
                """, (prenom, genre_code))
                alt_result = cursor.fetchone()
                if alt_result:
                    return alt_result[1], alt_result[0]
                else:
                    return nombre, "Année inconnue"

            return nombre, annee
        except Exception as e:
            print(f"Erreur de requête: {e}")
            return 0, "Erreur"
        finally:
            conn.close()

# Mise à jour de l'affichage des stats
    def update_stats_display():
        lines = []
        for (prenom, genre_code) in prenoms_sexe_select:
            genre_str = "masculin" if genre_code == 1 else "féminin"
            occur, annee = get_max_occurrence(prenom, genre_code)
            display_annee = "Année inconnue" if annee == "XXXX" else annee
            lines.append(f"{prenom[0] + prenom[1:].lower()} | {genre_str} | Max: {occur} en {display_annee}")

        stats_label.configure(text="\n".join(lines))

# Frame du bas avec contrôles
    bottom_frame = ctk.CTkFrame(search_frame, corner_radius=15)
    bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

    nom_info = ctk.CTkLabel(bottom_frame, text="Nom sélectionné:", font=("Arial", 14))
    nom_info.pack(side="left", padx=10, pady=5)

    search = ctk.StringVar()
    entry_custom = ctk.CTkEntry(bottom_frame, placeholder_text="Tape ton prénom ici...",
                               textvariable=search, width=200)
    entry_custom.pack(side="left", padx=10)
    entry_custom.bind("<Return>", on_enter)

# Suggestions de prénoms
    suggestion_frame = ctk.CTkScrollableFrame(master=frame_info, fg_color="transparent")
    suggestion_frame.pack()

    def update_suggestion(event=None):
        typed = search.get()
        for widget in suggestion_frame.winfo_children():
            widget.destroy()
        if len(typed) <= 3:
            return
        suggestion_frame._scrollbar.set(0, 0)

        filtrage = [prenom for prenom in prefixes_prenoms.get(typed.upper(), prefixes_prenoms.get(typed[:4].upper(), [])) if prenom.upper().startswith(typed.upper())]

        for suggestion in filtrage:
            btn = ctk.CTkButton(
                master=suggestion_frame,
                text=suggestion,
                command=lambda s=suggestion: select_suggestion(s),
                fg_color="#2b2b2b",
                hover_color="#3b3b3b"
            )
            btn.pack(fill="x", padx=5, pady=2)

    def select_suggestion(value):
        entry_custom.delete(0, ctk.END)
        entry_custom.insert(0, value)
        update_suggestion()

    entry_custom.bind("<KeyRelease>", update_suggestion)

    add_button = ctk.CTkButton(bottom_frame, text="Ajouter", command=on_enter)
    add_button.pack(side="left", padx=10)


#===============================================================================================================
#                                           STATISTIQUES
#
#===============================================================================================================

# Titre de la vue
    stat_label = ctk.CTkLabel(stat_frame, text="Statistiques Générales sur les naissances en France", font=("Arial", 20))
    stat_label.pack(pady=20)

# Frame pour les graphiques
    stats_frame = ctk.CTkFrame(stat_frame, corner_radius=15)
    stats_frame.pack(expand=True, fill="both", padx=20, pady=10)

# Graphique des naissances par année (exemple)
    try:
        conn = sqlite3.connect(db_prenoms)
        cursor = conn.cursor()
        cursor.execute("""SELECT annais, SUM(nombre) FROM prenoms WHERE annais != 'XXXX' GROUP BY annais ORDER BY annais;""")
        annees = []
        naissances = []
        for row in cursor.fetchall():
            annees.append(int(row[0]))
            naissances.append(row[1])
        conn.close()

        fig = Figure(figsize=(8, 5), dpi=100)
        fig.patch.set_facecolor('#000000')  # Fond de la figure

        plot = fig.add_subplot(111)
        plot.set_facecolor('#000000')  # Fond de la zone de tracé

        plot.plot(annees, naissances, color='#ff0000')
        plot.set_title("Naissances par année", color='white')  # Titre en blanc
        plot.set_xlabel("Année", color='white')  # Label X
        plot.set_ylabel("Nombre de naissances", color='white')  # Label Y
        plot.tick_params(colors='white')  # Couleur des ticks
        plot.grid(True, linestyle='--', alpha=0.3, color='white')  # Grille blanche légère

        canvas = FigureCanvasTkAgg(fig, master=stats_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)

    except Exception as e:
        error_label = ctk.CTkLabel(stats_frame, text=f"Erreur de chargement des données: {str(e)}", text_color="red")
        error_label.pack(pady=50)



#===============================================================================================================
#                                           ÉVOLUTIONS
#
#===============================================================================================================

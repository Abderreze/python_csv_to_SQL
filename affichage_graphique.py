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
from Graphes.classements import classements
from collections import defaultdict
from Utils.path import resource_path

naiss_rangs_deja_faits = {} # permettra d'éviter de recalculer pour des prénoms déjà sélectionnés

def gui(root, db_prenoms):
    matplotlib.use('Agg')
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root.title("Prénomator 3000 EXTRA MAX V2.0")

    # Création de la fenêtre définie par défaut en fullscreen
    main_container = ctk.CTkFrame(root, corner_radius=0)
    main_container.pack(side="right", expand=True, fill="both")
    # Création des frames qui seront nécessaire
    home_frame = ctk.CTkFrame(main_container, corner_radius=0)
    search_frame = ctk.CTkFrame(main_container, corner_radius=0)
    stat_frame = ctk.CTkFrame(main_container, corner_radius=0)
    evolution_frame = ctk.CTkFrame(main_container, corner_radius=0)
    classement_frame = ctk.CTkFrame(main_container, corner_radius=0)

    # Fonctions permettant de changer de frame grâce aux icons de la Sidebar
    def show_home():
        search_frame.pack_forget()
        stat_frame.pack_forget()
        evolution_frame.pack_forget()
        classement_frame.pack_forget()
        home_frame.pack(fill="both", expand=True)
    def show_search():
        home_frame.pack_forget()
        stat_frame.pack_forget()
        evolution_frame.pack_forget()
        classement_frame.pack_forget()
        search_frame.pack(fill="both", expand=True)
    def show_stat():
        home_frame.pack_forget()
        search_frame.pack_forget()
        evolution_frame.pack_forget()
        classement_frame.pack_forget()
        stat_frame.pack(fill="both", expand=True)
    def show_evolution():
        home_frame.pack_forget()
        search_frame.pack_forget()
        stat_frame.pack_forget()
        classement_frame.pack_forget()
        evolution_frame.pack(fill="both", expand=True)
    def show_classement():
        home_frame.pack_forget()
        search_frame.pack_forget()
        stat_frame.pack_forget()
        evolution_frame.pack_forget()
        classement_frame.pack(fill="both", expand=True)

    # Imports des icons
    home_icon = ctk.CTkImage(Image.open(resource_path("Icons/home.png")), size=(24, 24))
    search_icon = ctk.CTkImage(Image.open(resource_path("Icons/search.png")), size=(24, 24))
    stats_icon = ctk.CTkImage(Image.open(resource_path("Icons/stats.png")), size=(24, 24))
    evolution_icon = ctk.CTkImage(Image.open(resource_path("Icons/evolution.png")), size=(24, 24))
    classement_icon = ctk.CTkImage(Image.open(resource_path("Icons/classement.png")), size=(24, 24))

    # Création de la frame servant de sidebar
    sidebar = ctk.CTkFrame(root, width=80, fg_color="#1e1e1e", corner_radius=2)
    sidebar.pack(side="left", fill="y", padx=0, pady=0)
    sidebar.pack_propagate(False) #la taille de sidebar n'est pas définis par ces enfants (dans se cas les icons)
    ctk.CTkLabel(sidebar, text="", height=20).pack()

    # Création des bouttons de la sidebars puis on affiche ces mêmes bouttons
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

    classement_button = ctk.CTkButton(
        sidebar,
        text="",
        image=classement_icon,
        width=50,
        height=50,
        corner_radius=10,
        command=show_classement,
        fg_color="#dddddd",
        hover_color="#ffffff"
    )
    classement_button.pack(pady=10)

    # Création de la "mini-frame" contenant le switch du dark-mode AINSI QUE le texte l'accompagnant car sinon la texte est "coupé" par la sidebar
    switch_frame =ctk.CTkFrame(sidebar, fg_color="transparent")
    switch_frame.pack(side="right", padx=10)

    # Création du switch
    dark_mode_switch = ctk.CTkSwitch(switch_frame, text="", command=lambda: ctk.set_appearance_mode("dark" if dark_mode_switch.get() else "light"))
    dark_mode_switch.pack(pady=(0, 5))
    dark_mode_switch.select() # l'active de base

    # Pour que le texte soit centré ET en dessous du switch
    switch_label = ctk.CTkLabel(
        switch_frame,
        text="Dark-mode",
        text_color="white",
        anchor="center",
        justify="center"
    )
    switch_label.pack()

    # Affichage de la fenêtre
    show_home()


#===============================================================================================================
#                                           HOME
#
#===============================================================================================================
    # Import de l'image contenant les contributeurs
    contributors = ctk.CTkImage(Image.open(resource_path("Icons/contributors.png")), size=(240, 240))

    # Création d'un frame principal pour le contenu home
    home_content = ctk.CTkFrame(home_frame, fg_color="transparent")
    home_content.pack(expand=True, fill="both", padx=20, pady=20)

    # Frame pour le titre avec animation
    title_frame = ctk.CTkFrame(home_content, fg_color="transparent")
    title_frame.pack(pady=(0, 20))

    # Texte d'accueil avec animation de couleur
    def update_title_color():
        colors = ["#4CC9F0", "#F72585", "#7209B7", "#3A0CA3", "#4361EE"]
        current_color = colors[randint(0, len(colors))-1]
        label_bonjour.configure(text_color=current_color)
        home_frame.after(2000, update_title_color)

    label_bonjour = ctk.CTkLabel(
        title_frame,
        text="Prénomator 3000 EXTRA MAX V2.0",
        font=("Arial", 35, "bold"),
        text_color="#4CC9F0"
    )
    label_bonjour.pack()
    update_title_color()

    scroll_frame = ctk.CTkScrollableFrame(home_content, fg_color="transparent")
    scroll_frame.pack(expand=True, fill="both", padx=5, pady=5)

    # Fonction de gestion du scroll
    def _bound_to_mousewheel(event):
        scroll_frame._parent_canvas.bind_all("<MouseWheel>", _on_mousewheel) # Windows et Linux
        scroll_frame._parent_canvas.bind_all("<Button-4>", _on_mousewheel)  # Linux up
        scroll_frame._parent_canvas.bind_all("<Button-5>", _on_mousewheel)  # Linux down

    def _unbound_to_mousewheel(event):
        scroll_frame._parent_canvas.unbind_all("<MouseWheel>")
        scroll_frame._parent_canvas.unbind_all("<Button-4>")
        scroll_frame._parent_canvas.unbind_all("<Button-5>")

    def _on_mousewheel(event):
        if event.num == 4:  # Linux scroll up
            scroll_frame._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            scroll_frame._parent_canvas.yview_scroll(1, "units")
        else:  # Windows & MacOS
            scroll_frame._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Activer le scroll quand la souris est sur la scrollframe
    scroll_frame.bind("<Enter>", _bound_to_mousewheel)
    scroll_frame.bind("<Leave>", _unbound_to_mousewheel)


    # Section d'explication avec des cartes modernes
    def create_info_card(title, content):
        card = ctk.CTkFrame(
            scroll_frame,
            corner_radius=15,
            border_width=2,
            border_color="#3A0CA3"
        )
        card.pack(fill="x", pady=10, padx=5)

        # Titre de la carte
        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 18, "bold"),
            text_color="#F72585"
        ).pack(pady=(10, 5), padx=10, anchor="w")

        # Contenu
        ctk.CTkLabel(
            card,
            text=content,
            font=("Arial", 14),
            justify="left",
            wraplength=700
        ).pack(pady=5, padx=10, anchor="w")

        return card

    # Cartes d'information
    create_info_card(
        "Bienvenue !",
        "Vous êtes actuellement sur le 'Prénomator 3000 EXTRA MAX V2.0' ou plus communément appelé le 'Prénomator'. " \
        "Vous avez été choisi.e afin de pouvoir tester ce petit bijou de technologie qu'est le Prénomator."
    )

    create_info_card(
        "Fonctionnalités",
        "Explorez les différentes fonctionnalités de l'application grâce aux onglets de navigation :"
    )

    # Liste des fonctionnalités avec icônes
    features_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    features_frame.pack(fill="x", pady=5)

    # Icônes pour chaque fonctionnalité
    search_icon_small = ctk.CTkImage(Image.open(resource_path("Icons/search.png")), size=(20, 20))
    stats_icon_small = ctk.CTkImage(Image.open(resource_path("Icons/stats.png")), size=(20, 20))
    evolution_icon_small = ctk.CTkImage(Image.open(resource_path("Icons/evolution.png")), size=(20, 20))
    classement_icon_small = ctk.CTkImage(Image.open(resource_path("Icons/classement.png")), size=(20, 20))

    features = [
        ("Recherche", "Trouvez votre prénom et découvrez sa popularité au fil des années", search_icon_small),
        ("Statistiques", "Visualisez les tendances générales des naissances en France", stats_icon_small),
        ("Évolution", "Analysez l'évolution d'un prénom spécifique", evolution_icon_small),
        ("Classement", "Découvrez les prénoms les plus populaires par année", classement_icon_small)
    ]

    for i, (title, desc, icon) in enumerate(features):
        feature_card = ctk.CTkFrame(features_frame, fg_color="#1a1a1a", corner_radius=10)
        feature_card.pack(fill="x", pady=5)

        # Icône
        ctk.CTkLabel(feature_card, image=icon, text="").pack(side="left", padx=10)

        # Texte
        text_frame = ctk.CTkFrame(feature_card, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            text_frame,
            text=title,
            font=("Arial", 16, "bold"),
            text_color="#4361EE"
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text=desc,
            font=("Arial", 12),
            wraplength=600,
            justify="left"
        ).pack(anchor="w")

    # Section contributeurs
    contributors_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    contributors_frame.pack(pady=20)

    ctk.CTkLabel(
        contributors_frame,
        text="Contributeurs du projet",
        font=("Arial", 18, "bold"),
        text_color="#7209B7"
    ).pack()

    contributors_label = ctk.CTkLabel(contributors_frame, image=contributors, text="")
    contributors_label.pack(pady=10)

    # Note sur le dark mode
    dark_mode_note = ctk.CTkFrame(scroll_frame, fg_color="#1a1a1a", corner_radius=10)
    dark_mode_note.pack(fill="x", pady=20)

    ctk.CTkLabel(
        dark_mode_note,
        text="💡 Astuce : Vous pouvez ajuster le mode sombre/clair avec le switch dans la barre latérale",
        font=("Arial", 14, "italic"),
        text_color="#4CC9F0"
    ).pack(pady=10, padx=10)
#===============================================================================================================
#                                           SEARCH
#
#===============================================================================================================
# Frame du haut avec contrôles - Réorganisée pour un alignement central
    upper_frame = ctk.CTkFrame(search_frame, corner_radius=15)
    upper_frame.pack(side="top", fill="x", padx=10, pady=10)
# Conteneur principal pour centrer les éléments
    controls_container = ctk.CTkFrame(upper_frame, fg_color="transparent")
    controls_container.pack(expand=True, pady=5)

    nom_info = ctk.CTkLabel(controls_container, text="Nom sélectionné:", font=("Arial", 14))
    nom_info.grid(row=0, column=0, padx=(0,10), pady=5, sticky="e")

    # Fonction déclenchée lors de la validation d’un prénom
    def on_enter(event=None):
        """
        Gère l’ajout d’un prénom à la sélection lorsque l’utilisateur appuie sur Entrée.
        Met à jour la liste des prénoms affichés et rafraîchit les graphiques et statistiques.
        """
        global naiss_rangs_deja_faits
        prenom = search.get().upper()
        sexe = sexe_saisi.get()
        sexe_str = "masculin" if sexe == 1 else "féminin"

        # Vérifier si la limite est atteinte (ex: 5 prénoms max)
        if len(prenoms_select) >= 5:
            limite_label = ctk.CTkLabel(
                frame_graphiques,
                text="⚠ Limite de 5 prénoms atteinte !",
                text_color="red",
                font=("Arial", 12)
            )
            limite_label.pack(pady=5)
            return

        # Vérifier que le prénom est valide et n'a pas déjà été ajouté
        if (prenom, sexe_str) not in prenoms_select and (prenom.upper(), sexe) in prenoms_sexe_existants:
            prenoms_sexe_select[(prenom, sexe)] = f"#{randint(0x333333, 0xFFFFFF):06x}"
            prenoms_select.append((prenom, sexe_str))

        # Mettre à jour l'affichage
        prenoms_deja_select.configure(values=[f"{p} {s}" for p, s in prenoms_select])
        naiss_rangs_deja_faits = afficher_graphique(prenoms_sexe_select, naiss_rangs_deja_faits)
        update_stats_display()
        search.set("")  # Vide le champ de saisie après ajout

    # Zone de saisie du prénom
    search = ctk.StringVar()
    entry_custom = ctk.CTkEntry(controls_container, placeholder_text="Tape ton prénom ici...", textvariable=search, width=200)
    entry_custom.grid(row=0, column=1, padx=10, pady=5)
    entry_custom.bind("<Return>", on_enter)

    # Configuration du genre
    sexe_frame = ctk.CTkFrame(controls_container, fg_color="transparent")
    sexe_frame.grid(row=0, column=3, padx=10, pady=5)
    sexe_saisi = ctk.IntVar(value=1)
    radio_homme = ctk.CTkRadioButton(sexe_frame, text="Homme", variable=sexe_saisi, value=1)
    radio_homme.pack(side="left", padx=5)
    radio_femme = ctk.CTkRadioButton(sexe_frame, text="Femme", variable=sexe_saisi, value=2)
    radio_femme.pack(side="left", padx=5)

# Configuration du grid pour un espacement uniforme
    for i in range(4):  # 4 colonnes
        controls_container.grid_columnconfigure(i, weight=1 if i == 3 else 0)


# Frame "intérmédiaire" permettant de contenire les 2 autres frames
    middle_container = ctk.CTkFrame(search_frame, corner_radius=0)
    middle_container.pack(expand=True, fill="both", padx=10, pady=(0,10))  # pady=(0,10) pour un peu d'espace en bas

# Frame gauche : Infos
    frame_info = ctk.CTkFrame(middle_container, corner_radius=15)
    frame_info.pack(side="left", padx=10, pady=10, fill="both", expand=True, anchor="w")
    label_info = ctk.CTkLabel(frame_info, text="Informations sur le prénom", font=("Arial", 16, "bold"))
    label_info.pack(pady=5)
    lignes_stats_frame = ctk.CTkFrame(frame_info, fg_color='transparent')
    lignes_stats_frame.pack(pady=2, padx=2, expand=False, anchor='n', side='top')
    #stats_label = ctk.CTkLabel(frame_info, text="", anchor="w", justify="left", font=("Arial", 24))
    #stats_label.pack(pady=10, fill="both", expand=False)

# Frame droite : Graphiques
    frame_graphiques = ctk.CTkFrame(middle_container, corner_radius=15)
    frame_graphiques.pack(side="left", padx=10, pady=10, fill="both", expand=True)
    label_graphiques = ctk.CTkLabel(frame_graphiques, text="Graphique du prénom", font=("Arial", 16, "bold"))
    label_graphiques.pack(pady=5)


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
    with open('suggestions.csv', mode='r', encoding='utf-8', newline='') as f:
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

    # Fonction d'affichage du graphique principal
    def afficher_graphique(dico_prenoms_sexe, prenoms_deja_etudies):
        """
        Affiche le graphique des prénoms sélectionnés à partir de la base de données.

        Args:
            dico_prenoms_sexe (dict): Dictionnaire des prénoms avec leur sexe associé comme clé, et leur couleur comme valeur.
            prenoms_deja_etudies (dict): Dictionnaire des prénoms déjà traités pour éviter les recalculs.

        Returns:
            dict: Dictionnaire mis à jour avec les données traitées (naissances, rangs).
        """
        # Nettoyage des anciens widgets sauf ceux à conserver
        for widget in frame_graphiques.winfo_children():
            if widget not in [label_graphiques, zone_select_search]:
                widget.destroy()

        # Si aucun prénom n’est sélectionné, on ne fait rien
        if not dico_prenoms_sexe:
            return

        # Récupération des données et du graphique
        result, fig, prenoms_deja_etudies = graphe_prenom(
            db_prenoms, dico_prenoms_sexe, prenoms_deja_etudies
        )

        if result:
            # Si au moins un prénom valide, on affiche le graphique
            canvas = FigureCanvasTkAgg(fig, master=frame_graphiques)
            canvas.draw()
            canvas.get_tk_widget().pack()
        else:
            # Affiche un message si aucun prénom n'a été trouvé
            message_label = ctk.CTkLabel(
                frame_graphiques,
                text="⚠ Aucun prénom valide trouvé dans la base.",
                text_color="red",
                font=("Arial", 14, "bold")
            )
            message_label.pack(pady=20)

        return prenoms_deja_etudies

    # Fonction de retrait d’un prénom sélectionné
    # Fonction de retrait d’un prénom sélectionné
    def retire_prenom():
        """
        Retire un prénom de la sélection et met à jour le graphique et les statistiques affichées.
        """
        prenom_a_retirer = prenoms_deja_select.get()
        if not prenom_a_retirer:
            return

        prenom, genre = prenom_a_retirer.split(' ')
        genre_code = 1 if genre == 'masculin' else 2
        tuple_dico = (prenom, genre_code)

        # Supprime le prénom de la liste de sélection
        if (prenom, genre) in prenoms_select:
            prenoms_select.remove((prenom, genre))
        if tuple_dico in prenoms_sexe_select:
            del prenoms_sexe_select[tuple_dico]

        # Réinitialise l'Entry et la liste déroulante
        prenoms_deja_select.set("")  # <-- Cette ligne nettoie la ComboBox
        search.set("")  # <-- Cette ligne nettoie l'Entry principal

        # Met à jour la liste déroulante
        prenoms_deja_select.configure(values=[f"{p} {s}" for p, s in prenoms_select])

        # Rafraîchit le graphique et les stats
        global naiss_rangs_deja_faits
        naiss_rangs_deja_faits = afficher_graphique(prenoms_sexe_select, naiss_rangs_deja_faits)
        update_stats_display()

    # Zone de sélection des prénoms avec bouton de suppression
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

    # Label d’affichage d’image (optionnel ou message)
    image_label = ctk.CTkLabel(frame_graphiques, text="")
    image_label.pack(pady=10)

    # Fonction récupérant l’occurrence maximale d’un prénom et l’année associée
    def get_max_occurrence(prenom, genre_code):
        """
        Récupère le nombre maximal de naissances pour un prénom donné et l’année correspondante.

        Args:
            prenom (str): Le prénom recherché.
            genre_code (int): Code du sexe (1 pour masculin, 2 pour féminin).

        Returns:
            tuple: (nombre, année) ou (0, "N/A") si aucun résultat.
        """
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

            # Vérifie si l'année est invalide malgré tout
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
        for widget in lignes_stats_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        for (prenom, genre_code) in prenoms_sexe_select:
            genre_str = "masculin" if genre_code == 1 else "féminin"
            occur, annee = get_max_occurrence(prenom, genre_code)
            display_annee = "Année inconnue" if annee == "XXXX" else annee
            lines.append(f"{prenom[0] + prenom[1:].lower()} | {genre_str} | Max: {occur} en {display_annee}")
            label = ctk.CTkLabel(lignes_stats_frame,
                                 text=f"{prenom[0].upper() + prenom[1:].lower()} | {genre_str} | Max: {occur} en {display_annee}",
                                 text_color=prenoms_sexe_select[(prenom, genre_code)], anchor="w", font=("Arial", 24))
            label.pack(anchor="w", padx=2)


        #stats_label.configure(text="\n".join(lines), text_color=prenoms_sexe_select[(prenom, genre_code)])

# Suggestions de prénoms
    suggestion_frame = ctk.CTkScrollableFrame(master=frame_info, fg_color="transparent")
    suggestion_frame.pack(anchor="n")
    def update_suggestion(event=None):
        typed = search.get().upper()
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
    add_button = ctk.CTkButton(controls_container, text="Ajouter", command=on_enter, width=80)
    add_button.grid(row=0, column=2, padx=(10,20), pady=5)

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
        plot.plot(annees, naissances, color='blue')
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

    # Zone Titre
    evolution_label = ctk.CTkLabel(evolution_frame, text="Évolution : Différence Décès - Naissances", font=("Arial", 20))
    evolution_label.pack(pady=20)

    # Zone du haut pour les contrôles
    evolution_controls = ctk.CTkFrame(evolution_frame, corner_radius=15)
    evolution_controls.pack(pady=10)
    evolution_prenom_var = ctk.StringVar()
    evolution_entry = ctk.CTkEntry(evolution_controls, textvariable=evolution_prenom_var, placeholder_text="Tape ton prénom ici...", width=200)
    evolution_entry.pack(side="left", padx=10)

    # Simule une Listbox avec un CTkFrame + CTkButtons
    autocomplete_frame = ctk.CTkFrame(evolution_controls, corner_radius=8)
    autocomplete_frame.pack_forget()

    def update_autocomplete(event=None):
        typed = evolution_prenom_var.get().upper()
        for widget in autocomplete_frame.winfo_children():
            widget.destroy()
        if not typed:
            autocomplete_frame.pack_forget()
            return
        conn = sqlite3.connect(db_prenoms)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT preusuel FROM prenoms WHERE UPPER(preusuel) LIKE ? ORDER BY preusuel ASC LIMIT 10", (typed + '%',))
        results = cursor.fetchall()
        conn.close()
        if results:
            for item in results:
                suggestion = item[0]
                btn = ctk.CTkButton(autocomplete_frame, text=suggestion, width=100, command=lambda s=suggestion: select_from_autocomplete(s))
                btn.pack(anchor="w", padx=5, pady=1)
            autocomplete_frame.pack(side="left", padx=5)
        else:
            autocomplete_frame.pack_forget()

    def select_from_autocomplete(value):
        evolution_prenom_var.set(value)
        autocomplete_frame.pack_forget()
    evolution_entry.bind("<KeyRelease>", update_autocomplete)

    evolution_sexe_var = ctk.IntVar(value=1)
    evolution_radio_h = ctk.CTkRadioButton(evolution_controls, text="Homme", variable=evolution_sexe_var, value=1)
    evolution_radio_h.pack(side="left", padx=5)
    evolution_radio_f = ctk.CTkRadioButton(evolution_controls, text="Femme", variable=evolution_sexe_var, value=2)
    evolution_radio_f.pack(side="left", padx=5)
    evolution_button = ctk.CTkButton(evolution_controls, text="Afficher", command=lambda: afficher_graphe_evolution(db_prenoms))
    evolution_button.pack(side="left", padx=10)
    evolution_graph_frame = ctk.CTkFrame(evolution_frame, corner_radius=15)
    evolution_graph_frame.pack(expand=True, fill="both", padx=20, pady=10)

    def afficher_graphe_evolution(db_path):
        """
        Affiche un graphique représentant l'évolution de la différence entre
        le nombre de naissances et de décès d'un prénom donné, ainsi que sa dérivée.

        Paramètre :
            db_path (str) : Le chemin vers la base de données SQLite contenant
                            les informations de naissances et de décès.
        """
        # Nettoyage de la zone graphique précédente (si un graphe est déjà affiché)
        for widget in evolution_graph_frame.winfo_children():
            widget.destroy()
        # Récupération du prénom saisi et du sexe sélectionné
        prenom = evolution_prenom_var.get().strip().upper()
        sexe = evolution_sexe_var.get()
        # Si aucun prénom n'est saisi, on quitte la fonction
        if not prenom:
            return
        # Masquer et nettoyer la zone d'autocomplétion
        autocomplete_frame.pack_forget()
        for widget in autocomplete_frame.winfo_children():
            widget.destroy()

        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Naissances
        cursor.execute("""
            SELECT annais, SUM(nombre)
            FROM prenoms
            WHERE preusuel = ? AND sexe = ? AND annais != 'XXXX'
            GROUP BY annais;
        """, (prenom, sexe))
        naissances_data = cursor.fetchall()
        naissances = {int(annee): int(nb) for annee, nb in naissances_data}

        # Décès
        cursor.execute("""
            SELECT SUBSTR(CAST(date_deces AS TEXT), 1, 4) AS annee, COUNT(*)
            FROM deces
            WHERE UPPER(prenom) LIKE ? AND sexe = ?
            AND LENGTH(date_deces) = 8
            AND CAST(SUBSTR(CAST(date_deces AS TEXT), 1, 4) AS INTEGER) BETWEEN 1900 AND 2025
            GROUP BY annee
            HAVING annee IS NOT NULL;
        """, (prenom + '%', "M" if sexe == 1 else "F"))
        deces_data = cursor.fetchall()
        deces = {int(annee): int(nb) for annee, nb in deces_data if annee and annee.isdigit()}

        conn.close()

        toutes_annees = sorted(set(naissances.keys()).union(deces.keys()))

        annees_valides = []
        valeurs_diff = []
        for annee in toutes_annees:
            n = naissances.get(annee, 0)
            d = deces.get(annee, 0)
            annees_valides.append(annee)
            valeurs_diff.append(n - d)

        if len(valeurs_diff) < 2:
            return

        derivee = []
        annees_derivee = []
        for i in range(1, len(valeurs_diff)):
            if valeurs_diff[i - 1] != 0:
                variation = ((valeurs_diff[i] - valeurs_diff[i - 1]) / abs(valeurs_diff[i - 1])) * 100
                derivee.append(variation)
                annees_derivee.append(annees_valides[i])

        # Plot
        fig = Figure(figsize=(8, 5), dpi=100)
        fig.patch.set_facecolor('#000000')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#000000')

        # Remplir la zone sous la courbe
        ax.fill_between(annees_derivee, derivee, color="skyblue", alpha=0.4)

        # Tracer la courbe
        for i in range(1, len(derivee)):
            x = [annees_derivee[i - 1], annees_derivee[i]]
            y = [derivee[i - 1], derivee[i]]
            couleur = 'lime' if y[1] >= 0 else 'red'
            ax.plot(x, y, color=couleur)

        ax.set_title(f"Dérivée (%) de (Naissances - Décès) ==> {prenom}", color='white')
        ax.set_xlabel("Année", color='white')
        ax.set_ylabel("Variation en %", color='white')
        ax.tick_params(colors='white')
        ax.grid(True, linestyle='--', alpha=0.3, color='white')

        canvas = FigureCanvasTkAgg(fig, master=evolution_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)

#===============================================================================================================
#                                           CLASSEMENT
#
#===============================================================================================================

# Création de la frame de sélection (pour les boutons et combobox)
    frame_selection = ctk.CTkFrame(classement_frame, corner_radius=15)
    frame_selection.pack(side="top", fill="x", padx=10, pady=10)

# Configuration des colonnes de la frame de sélection pour centrer les éléments
    frame_selection.grid_columnconfigure(0, weight=1)
    frame_selection.grid_columnconfigure(1, weight=1)

# Création d'une frame conteneur principale pour les tableaux
# Cette frame va nous permettre de bien centrer les deux tableaux
    frame_conteneur_tableaux = ctk.CTkFrame(classement_frame)
    frame_conteneur_tableaux.pack(expand=True, fill='both', pady=20)

# Création des frames pour chaque tableau (filles et garçons)
    frame_tableau_fille = ctk.CTkFrame(master=frame_conteneur_tableaux)
    frame_tableau_garcon = ctk.CTkFrame(master=frame_conteneur_tableaux)

# Placement des tableaux côte à côte avec grid()
# Note: expand=True et sticky='nsew' permettent un bon redimensionnement
    frame_tableau_fille.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
    frame_tableau_garcon.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

# Configuration des poids des colonnes de la frame conteneur
# Cela permet de centrer les tableaux et de gérer l'espacement
    frame_conteneur_tableaux.grid_columnconfigure(0, weight=1)
    frame_conteneur_tableaux.grid_columnconfigure(1, weight=1)
    frame_conteneur_tableaux.grid_rowconfigure(0, weight=1)

# Création des éléments d'interface dans la frame de sélection
# Combobox pour choisir l'année
    annees_possibles = [str(i) for i in range(1900, 2023)]
    selection_annee = ctk.CTkComboBox(master=frame_selection, values=annees_possibles)
    selection_annee.grid(row=0, column=0, padx=20)

# Bouton pour afficher les résultats
    classement_button = ctk.CTkButton(frame_selection, text="Afficher", command=lambda: affiche_tableau_classement())
    classement_button.grid(row=0, column=1, padx=20)

# Lier l'événement de sélection à la fonction d'affichage
    selection_annee.bind('<<ComboboxSelected>>', lambda e: affiche_tableau_classement())

    def affiche_tableau_classement(event=None):
        """
        Fonction principale pour afficher les tableaux de classement
        - Récupère l'année sélectionnée
        - Obtient les données depuis la base
        - Affiche les tableaux avec mise en forme
        """

        # 1. Récupération des données
        annee_selectionnee = selection_annee.get()
        try:
            annee_selectionnee_entier = int(annee_selectionnee)
            if annee_selectionnee_entier >= 1900 and annee_selectionnee_entier <= 2022:
                les_tops = classements(annee_selectionnee, db_prenoms)

                # Extraction des listes filles et garçons
                liste_garcon = les_tops['masculin']
                liste_fille = les_tops['feminin']

                # Ajout des en-têtes de colonnes
                titres = ("Prénom", "Nombre de naissances")
                liste_fille.insert(0, titres)
                liste_garcon.insert(0, titres)

                # Définition des couleurs spéciales pour les 3 premières places
                couleurs_classement = {
                    1: '#fcb434',  # Or
                    2: '#d7d7d7',  # Argent
                    3: '#a77044'   # Bronze
                }

                # 2. Nettoyage des anciens widgets
                for widget in frame_tableau_fille.winfo_children():
                    widget.destroy()
                for widget in frame_tableau_garcon.winfo_children():
                    widget.destroy()

                # 3. Création du tableau des filles
                for i, ligne in enumerate(liste_fille):
                    for j, case in enumerate(ligne):
                        label = ctk.CTkLabel(
                            frame_tableau_fille,
                            text=case,
                            width=100,
                            anchor='center',
                            font=("Arial", 24),
                            text_color=couleurs_classement.get(i, '#ffffff')  # Couleur spéciale pour les 3 premiers
                        )
                        label.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')

                # 4. Création du tableau des garçons
                for i, ligne in enumerate(liste_garcon):
                    for j, case in enumerate(ligne):
                        label = ctk.CTkLabel(
                            frame_tableau_garcon,
                            text=case,
                            width=100,
                            anchor='center',
                            font=("Arial", 24),
                            text_color=couleurs_classement.get(i, '#ffffff')
                        )
                        label.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')

                # 5. Configuration du redimensionnement des tableaux

                # Pour le tableau des filles
                for i in range(len(liste_fille)):
                    frame_tableau_fille.grid_rowconfigure(i, weight=1)
                for j in range(len(titres)):
                    frame_tableau_fille.grid_columnconfigure(j, weight=1)

                # Pour le tableau des garçons
                for i in range(len(liste_garcon)):
                    frame_tableau_garcon.grid_rowconfigure(i, weight=1)
                for j in range(len(titres)):
                    frame_tableau_garcon.grid_columnconfigure(j, weight=1)
                    label.grid(row=i, column=j, padx=5, pady=5)
            else:
                raise ValueError
        except ValueError:
            label = ctk.CTkLabel(frame_tableau_garcon)
            label.pack()
            label.configure(text="Cette année est impossible, elle doit être entre 1900 et 2022 et sous forme décimale",
                            font=('Arial', 24),
                            text_color='#ff0000')


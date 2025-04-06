import customtkinter as ctk
import sqlite3
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import randint
from PIL import Image, ImageTk

from Graphes.graphe_de_ton_prenom import graphe_prenom

matplotlib.use('Agg')

# Apparence
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Fenêtre principale
root = ctk.CTk()
root.attributes('-zoomed', True)
root.title("Prénomator 3000 EXTRA MAX V2.0")

main_frame = ctk.CTkFrame(root, corner_radius=20)
main_frame.pack(expand=True, fill="both", padx=10, pady=10)

# ▶️ Frame gauche : Infos
frame_info = ctk.CTkFrame(main_frame, corner_radius=15)
frame_info.pack(side="left", padx=10, pady=10, fill="both", expand=True, anchor="w")

label_info = ctk.CTkLabel(frame_info, text="Informations sur le prénom", font=("Arial", 16, "bold"))
label_info.pack(pady=5)

stats_label = ctk.CTkLabel(frame_info, text="", anchor="w", justify="left", font=("Arial", 14))
stats_label.pack(pady=10, fill="both", expand=False)

# ▶️ Frame droite : Gère les prénoms + graph + image
frame_graphiques = ctk.CTkFrame(main_frame, corner_radius=15)
frame_graphiques.pack(side="left", padx=10, pady=10, fill="both", expand=True)

label_graphiques = ctk.CTkLabel(frame_graphiques, text="Graphique du prénom", font=("Arial", 16, "bold"))
label_graphiques.pack(pady=5)

# 🔸 RadioButtons de genre
sexe_saisi = ctk.IntVar(value=1)

sexe_frame = ctk.CTkFrame(frame_info)
sexe_frame.pack(pady=5)

radio_homme = ctk.CTkRadioButton(sexe_frame, text="Homme", variable=sexe_saisi, value=1)
radio_homme.pack(side="left", padx=10)

radio_femme = ctk.CTkRadioButton(sexe_frame, text="Femme", variable=sexe_saisi, value=2)
radio_femme.pack(side="left", padx=10)

# 🔸 Données prénoms sélectionnés
prenoms_sexe_select = {}
prenoms_select = []

def afficher_graphique(dico_prenoms_sexe):
    result = graphe_prenom(dico_prenoms_sexe)
    if result is True:
        try:
            image = Image.open("graphique.png")
            image = image.resize((500, 400), Image.Resampling.LANCZOS)
            photo = ctk.CTkImage(light_image=image, dark_image=image, size=(500, 400))
            image_label.configure(image=photo)
            image_label.image = photo
        except Exception as e:
            print("Erreur chargement image :", e)


def on_enter(event=None):
    prenom = search.get()
    sexe = sexe_saisi.get()
    sexe_str = "masculin" if sexe == 1 else "féminin"

    if (prenom, sexe_str) not in prenoms_select:
        prenoms_sexe_select[(prenom, sexe)] = f"#{randint(0, 0xFFFFFF):06x}"
        prenoms_select.append((prenom, sexe_str))
    else:
        print("ich bin ein berliner")

    prenoms_deja_select.configure(values=[f"{p} {s}" for p, s in prenoms_select])
    afficher_graphique(prenoms_sexe_select)
    update_stats_display()


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


# 🔸 Zone sélection
zone_select = ctk.CTkFrame(frame_graphiques)
zone_select.pack(pady=10)

prenoms_deja_select = ctk.CTkComboBox(zone_select, values=[], width=200)
prenoms_deja_select.pack(side="left", padx=5)

remove_button = ctk.CTkButton(
    zone_select,
    text="Retirer",
    command=retire_prenom,
    fg_color="#d9534f",       # Rouge style Bootstrap danger
    hover_color="#c9302c",    # Rouge plus foncé au survol
    text_color="white"
)

remove_button.pack(side="left", padx=5)

# 🔸 Image
image_label = ctk.CTkLabel(frame_graphiques, text="")
image_label.pack(pady=10)

def get_max_occurrence(prenom, genre_code):
    conn = sqlite3.connect("prenoms.db")
    cursor = conn.cursor()
    try:
        # Requête principale
        cursor.execute("""
            SELECT annais, nombre
            FROM prenoms
            WHERE preusuel=? AND sexe=?
            ORDER BY nombre DESC
            LIMIT 1
        """, (prenom.upper(), genre_code))
        result = cursor.fetchone()

        if not result:
            return 0, "N/A"

        annee, nombre = result[0], result[1]

        # Gestion spéciale pour l'année XXXX
        if str(annee).strip().upper() == "XXXX":
            #Recherche de la dernière année non-XXXX disponible
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
                return nombre, "Année inconnue"  # Conservation du nombre mais avec un libellé spécial


        return nombre, annee
    except Exception as e:
        print(f"Erreur de requête: {e}")
        return 0, "Erreur"
    finally:
        conn.close()

def update_stats_display():
    lines = []
    for (prenom, genre_code) in prenoms_sexe_select:
        genre_str = "masculin" if genre_code == 1 else "féminin"
        occur, annee = get_max_occurrence(prenom, genre_code)

        # Formatage spécial pour l'affichage
        display_annee = "Année inconnue" if annee == "XXXX" else annee
        lines.append(f"{prenom} | {genre_str} | Max: {occur} en {display_annee}")

    stats_label.configure(text="\n".join(lines))


# 🔸 Boutons de la frame d'en bas
bottom_frame = ctk.CTkFrame(root, corner_radius=15)
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

nom_info = ctk.CTkLabel(bottom_frame, text="Nom sélectionné:", font=("Arial", 14))
nom_info.pack(side="left", padx=10, pady=5)

search = ctk.StringVar()
entry_custom = ctk.CTkEntry(bottom_frame, placeholder_text="Tape ton prénom ici...", textvariable=search, width=200)
entry_custom.pack(side="left", padx=10)
entry_custom.bind("<Return>", on_enter)

add_button = ctk.CTkButton(bottom_frame, text="Ajouter", command=on_enter)
add_button.pack(side="left", padx=10)

dark_mode_switch = ctk.CTkSwitch(bottom_frame, text="Dark mode", command=lambda: ctk.set_appearance_mode("dark" if dark_mode_switch.get() else "light"))
dark_mode_switch.pack(side="right", padx=10)
dark_mode_switch.select()

# Start
root.mainloop()

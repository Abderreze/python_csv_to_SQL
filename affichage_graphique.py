import customtkinter as ctk  # Assurez-vous de l'installer avec `pip install customtkinter`
import random

# Configuration de l'apparence
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Fenêtre principale
root = ctk.CTk()
root.attributes('-zoomed', True)
root.title("Prénomator 3000 EXTRA MAX V2.0")

# Zone principale
main_frame = ctk.CTkFrame(root, corner_radius=20)
main_frame.pack(expand=True, fill="both", padx=10, pady=10)

# Définition des limites de la zone des bulles
ZONE_X_MIN, ZONE_Y_MIN = 100, 300   # Ajuste ces valeurs en fonction de la taille de ta fenêtre
ZONE_X_MAX, ZONE_Y_MAX = 600, 500   # Zone basse de l'interface

# Label principal
label = ctk.CTkLabel(main_frame, text="Bienvenue sur le Prénomator 3000 !", fg_color=("gray20", "gray30"), corner_radius=10)
label.pack(pady=10, fill="x", padx=10)

# Champ de saisie
prenom_saisi = ctk.StringVar(value="Nom recherché")
entry = ctk.CTkEntry(main_frame, placeholder_text="En savoir plus sur mon prénom...", corner_radius=20)
entry.pack(pady=10, fill="x", padx=10)

# Fonction pour récupérer et stocker la valeur
def valider_saisie():
    prenom_saisi.set(entry.get())
    switch2.configure(text=prenom_saisi.get())

# Liste contenant toutes les bulles
bulles = []

# Fonction pour animer une bulle
def animer_bulle(bulle, y, direction=5):
    if ZONE_Y_MIN <= y <= ZONE_Y_MAX:  # Restriction aux limites Y
        y += direction  # Monter ou descendre légèrement
        bulle.place_configure(y=y)
        root.after(500, animer_bulle, bulle, y, direction * -1)

# Fonction pour créer une bulle dans la zone définie
def creer_bulle(texte):
    # Générer une position uniquement dans la zone définie
    x = random.randint(ZONE_X_MIN, ZONE_X_MAX)
    y = random.randint(ZONE_Y_MIN, ZONE_Y_MAX)

    # Créer la bulle
    bulle = ctk.CTkLabel(main_frame, text=texte, fg_color="gray30", corner_radius=20, padx=10, pady=5)
    bulle.place(x=x, y=y)

    bulles.append(bulle)  # Ajouter à la liste
    animer_bulle(bulle, y)

# Bouton pour créer une bulle
button = ctk.CTkButton(main_frame, text="Créer une bulle", command=lambda: creer_bulle(prenom_saisi.get()))
button.pack(pady=10)

# Bouton de validation
valider_button = ctk.CTkButton(main_frame, text="Valider", corner_radius=20, command=valider_saisie)
valider_button.pack(pady=10)

# Interrupteurs (Switch)
switch = ctk.CTkSwitch(main_frame, text="Activer une option", corner_radius=10)
switch.pack(pady=5)

switch2 = ctk.CTkSwitch(main_frame, text=prenom_saisi.get(), corner_radius=10)
switch2.pack(pady=5)

# Mode sombre et clair
dark_mode_switch = ctk.CTkSwitch(main_frame, text="Dark mode", corner_radius=10, command=lambda: ctk.set_appearance_mode("dark" if dark_mode_switch.get() else "light"))
dark_mode_switch.pack(pady=5)
dark_mode_switch.select()

# Lancer l'application
root.mainloop()


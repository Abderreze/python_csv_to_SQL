import customtkinter as ctk  # Assurez-vous de l'installer avec `pip install customtkinter`
import random
# Configuration de l'apparence de CustomTkinter
ctk.set_appearance_mode("dark")  # Modes disponibles : "light", "dark", ou "system"
ctk.set_default_color_theme("dark-blue")  # Thèmes disponibles : "blue", "green", "dark-blue"

# Création de la fenêtre principale
root = ctk.CTk()
root.attributes('-zoomed', True)  # Ouvre la fenêtre en mode plein écran
root.title("Prénomator 3000 EXTRA MAX V2.0")  # Titre de la fenêtre

# Barre latérale (désactivée pour l'instant)
"""
sidebar = ctk.CTkFrame(root, width=150, corner_radius=20)
sidebar.pack(side="left", fill="y", padx=10, pady=10)

ctk.CTkButton(sidebar, text="Bouton 1", corner_radius=20).pack(pady=10)
ctk.CTkButton(sidebar, text="Bouton 2", corner_radius=20).pack(pady=10)
ctk.CTkButton(sidebar, text="Bouton 3", corner_radius=20).pack(pady=10)
"""

# Zone principale de contenu
main_frame = ctk.CTkFrame(root, corner_radius=20)
main_frame.pack(expand=True, fill="both", padx=10, pady=10)


# Label principal
label = ctk.CTkLabel(main_frame, text="Bienvenue sur le Prénomator 3000 !", fg_color=("gray20", "gray30"), corner_radius=10)
label.pack(pady=10, fill="x", padx=10)

# Champ de saisie
prenom_saisi = ctk.StringVar(value="Nom recherché")
entry = ctk.CTkEntry(main_frame, placeholder_text="En savoir plus sur mon prénom...", corner_radius=20)
entry.pack(pady=10, fill="x", padx=10)

# Fonction pour récupérer et stocker la valeur
def valider_saisie():
    prenom_saisi.set(entry.get())  # Met à jour la variable
    switch2.configure(text=prenom_saisi.get())  # Met à jour le texte du switch

bulles = [] #liste contenant toutes les bulles afin de ne pas les remplacer par une nouvelle bulle
# Fonction pour animer une bulle
def animer_bulle(bulle, y, direction=1, n=5):
    if 50 <= y <= 300:  # Limites pour éviter de sortir de l'écran
        y += direction  # Monter ou descendre légèrement
        bulle.place_configure(y=y)
        root.after(500, animer_bulle, bulle, y, direction * -1)  # Inverser le mouvement après 500ms

# Fonction pour créer une bulle de texte
def creer_bulle(texte):
    # Créer un label avec un fond semi-transparent
    bulle = ctk.CTkLabel(main_frame, text=texte, fg_color="gray30", corner_radius=20, padx=10, pady=5)
    x = random.randint(50, 400)
    y = random.randint(50, 300)
    bulle.place(x=x, y=y)  # Position aléatoire

    bulles.append(bulle)  # Ajouter la bulle à la liste
    animer_bulle(bulle, y)  # Lancer l'animation

button = ctk.CTkButton(main_frame, text="Créer une bulle", command=lambda: creer_bulle(prenom_saisi.get()))
button.pack(pady=10)


# Boutons interactifs

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

dark_mode_switch.configure(state="standard")
dark_mode_switch.select()  # Active par défaut le mode sombre


# Lancer l'application
root.mainloop()

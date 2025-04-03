import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from graphe_de_ton_prenom import graphe_prenom
def afficher_graphique():
    prenom, sexe = search.get(), dropdown.get()
    result = graphe_prenom(prenom, sexe)
    if result == True:
        image = Image.open("graphique.png")  # Remplace par le nom de ton fichier
        image = image.resize((500, 400), Image.Resampling.LANCZOS)  # Ajuster la taille si besoin
        photo = ImageTk.PhotoImage(image)
    
        label.config(image=photo)
        label.image = photo  # Nécessaire pour éviter la suppression par le garbage collector
def on_enter(event):
    sexe = dropdown.get()
    if sexe:
        afficher_graphique()
    else:
        print("Sélectionnez un sexe")
def on_select(event):
    sexe = dropdown.get()
# Création de la fenêtre principale
root = tk.Tk()
root.title("Affichage du Graphique")
# Création du bouton
btn = ttk.Button(root, text="Afficher le Graphique", command=afficher_graphique)
btn.pack(pady=10)
search = tk.StringVar()
search_label = tk.Label(root, text="Entrez un prénom : ")
entry = ttk.Entry(root, width=40, textvariable=search)
entry.pack(pady=10)
root.bind('<Return>', on_enter)
options = [1, 2]
dropdown = ttk.Combobox(values=options)
dropdown.pack()
# Label pour afficher l'image
label = tk.Label(root)
label.pack()

# Lancement de l'interface
root.mainloop()


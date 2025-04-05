import tkinter as tk
from tkinter import ttk
from random import randint
from PIL import Image, ImageTk
from graphe_de_ton_prenom import graphe_prenom
def afficher_graphique(dico_prenoms_sexe):
    result = graphe_prenom(dico_prenoms_sexe)
    if result == True:
        image = Image.open("graphique.png")  # Remplace par le nom de ton fichier
        image = image.resize((500, 400), Image.Resampling.LANCZOS)  # Ajuster la taille si besoin
        photo = ImageTk.PhotoImage(image)
    
        label.config(image=photo)
        label.image = photo  # Nécessaire pour éviter la suppression par le garbage collector
def on_enter(event):
    prenom, sexe = search.get(), dropdown.get()
    if sexe == "1":
        sexe_affichage = "masculin"
    else:
        sexe_affichage = "féminin"
    if (prenom, sexe_affichage) not in prenoms_select:
        prenoms_sexe_select[(prenom, int(sexe))] = f"#{randint(0, 0xFFFFFF):06x}"
        prenoms_select.append((prenom, sexe_affichage))
    else:
        print("ich bin ein berliner")
    prenoms_deja_select["values"] = prenoms_select
    if sexe:
        afficher_graphique(prenoms_sexe_select)
    else:
        print("Sélectionnez un sexe")
def on_select(event):
    sexe = dropdown.get()
def retire_prenom():
    prenom_a_retirer = prenoms_deja_select.get()
    index_espace = prenom_a_retirer.index(' ')
    tuple_a_retirer = (prenom_a_retirer[:index_espace], prenom_a_retirer[index_espace+1:])
    index = prenoms_select.index(tuple_a_retirer)
    if tuple_a_retirer[1] == 'masculin':
        tuple_a_retirer_dico = (tuple_a_retirer[0], 1)
    else:
        tuple_a_retirer_dico = (tuple_a_retirer[0], 2)
    del prenoms_select[index]
    del prenoms_sexe_select[tuple_a_retirer_dico]
    prenoms_deja_select["values"] = prenoms_select
    afficher_graphique(prenoms_sexe_select)
# Création de la fenêtre principale
root = tk.Tk()
root.title("Affichage du Graphique")
# Création du bouton
btn_retirer = ttk.Button(root, text="-", command=retire_prenom)
btn_retirer.pack(pady=10)
search = tk.StringVar()
search_label = tk.Label(root, text="Entrez un prénom : ")
entry = ttk.Entry(root, width=40, textvariable=search)
entry.pack(pady=10)
root.bind('<Return>', on_enter)
options = [1, 2]
dropdown = ttk.Combobox(values=options)
dropdown.pack()
prenoms_sexe_select = {}
prenoms_select = []
prenoms_deja_select = ttk.Combobox(values=prenoms_select)
prenoms_deja_select.pack()
# Label pour afficher l'image
label = tk.Label(root)
label.pack()
btn_retirer.pack(pady=10)
# Lancement de l'interface
root.mainloop()


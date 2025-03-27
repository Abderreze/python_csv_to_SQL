import csv
import sqlite3 
import matplotlib.pyplot as plt

liaison = sqlite3.connect("prenoms.db")
curseur = liaison.cursor()


curseur.execute("SELECT DISTINCT preusuel FROM prenoms;")

result = curseur.fetchall()
prenoms = [p_uplet[0] for p_uplet in result]
prenom = input("Entrer un prénom : ")
sexe = int(input("Entrer le sexe (1 pour masculin, 2 pour féminin) : "))
if prenom.upper() in prenoms:
    couleurs = ('purple', 'gold')
    curseur.execute("SELECT annais, nombre FROM prenoms WHERE preusuel LIKE ? AND sexe = ? ORDER BY annais ;", (prenom, sexe))

    result = curseur.fetchall()

    x = [int(annee) for annee, nombre in result if annee != 'XXXX']
    y = [int(nombre) for annee, nombre in result if annee != 'XXXX']
    indice_max = y.index(max(y))
    x_max = x[indice_max]
    y_max = y[indice_max]
#plt.scatter(x, y, color='r', label="Points")
    plt.plot(x, y, marker='o', linestyle='-', color=couleurs[0], label=prenom)
    plt.scatter(x_max, max(y), color='r', label=f"Max en x={x_max}")
    plt.text(x_max, max(y), f"x={x_max}, y={y_max}", verticalalignment='bottom', fontsize=14, color=couleurs[1])
    plt.xlabel("Années")
    plt.ylabel("Naissances")
    plt.title("Graphique avec abscisse du maximum")
    plt.legend()
    plt.show()
else:
    print("Ce prénom n'est pas dans la bdd")
liaison.close()

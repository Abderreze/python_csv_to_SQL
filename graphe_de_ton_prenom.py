import csv
import sqlite3 
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
plt.style.use('dark_background')
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

liaison = sqlite3.connect("prenoms.db")
curseur = liaison.cursor()


curseur.execute("SELECT DISTINCT preusuel FROM prenoms;")

result = curseur.fetchall()
prenoms = set([p_uplet[0] for p_uplet in result])
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

    plt.ylim(0, max(y) * 1.1)  # Ajuste pour un peu d'espace en haut
#plt.scatter(x, y, color='r', label="Points")
    plt.plot(x, y, marker='o', linestyle='-', color=couleurs[0], label=prenom)
    plt.scatter(x_max, max(y), marker='x', color='r', label=f"Max en x={x_max}", zorder=3)
    plt.text(x_max, max(y), f"année ={x_max}, nb naissance ={y_max}", verticalalignment='bottom', fontsize=14, color=couleurs[1])
    plt.xlabel("Années")
    plt.ylabel("Naissances")
    plt.title("Graphique avec abscisse du maximum")
    plt.legend()
    plt.show()
    plt.savefig("graphique.png")
else:
    print("Ce prénom n'est pas dans la bdd")
liaison.close()

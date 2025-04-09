import sqlite3 
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
def graphe_prenom(db_prenoms, prenoms_sexes: dict):
    plt.style.use('dark_background')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    liaison = sqlite3.connect(db_prenoms)
    curseur = liaison.cursor()
    plt.clf()
    curseur.execute("SELECT DISTINCT preusuel FROM prenoms;")
    prenoms = set([p_uplet[0] for p_uplet in curseur.fetchall()])
    curseur.execute("SELECT DISTINCT preusuel, sexe FROM prenoms;")
    prenoms_sexe = set([(p_uplet[0], int(p_uplet[1])) for p_uplet in curseur.fetchall()])
    existe = set(prenoms_sexes.keys()) <= prenoms_sexe
    fig = Figure(figsize=(5, 4), dpi=100)
    plot = fig.add_subplot(111)
    existe = True
    for prenom_sexe, couleur in prenoms_sexes.items():
        prenom, sexe = prenom_sexe
        if prenom.upper() in prenoms:
            curseur.execute("SELECT annais, nombre FROM prenoms WHERE preusuel LIKE ? AND sexe = ? ORDER BY annais ;", (prenom.upper(), sexe))

            result = curseur.fetchall()

            x = [int(annee) for annee, nombre in result if annee != 'XXXX']
            y = [int(nombre) for annee, nombre in result if annee != 'XXXX']
            indice_max = y.index(max(y))
            x_max = x[indice_max]
            y_max = y[indice_max]
            plot.text(x_max, min(y), f"{int(x_max)}", color='red', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
            plot.text(x[0], y_max, f"{y_max}", color='red', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
            plot.plot(x, y, marker=None, linestyle='-', color=couleur, label=prenom)
            plot.scatter(x_max, max(y), marker='x', color='r', label=f"Max en x={x_max}", zorder=3)
            plot.set_xlabel("Années")
            plot.set_ylabel("Naissances")
            plot.set_title("Graphique avec abscisse du maximum")
            plot.legend()
            existe = (True and existe)
        else:
            print("Ce prénom n'est pas dans la bdd")
    #        curseur.execute("SELECT DISTINCT preusuel FROM prenoms WHERE ")
            existe = (False and existe)

    return existe, fig
if __name__ == '__main__':
    graphe_prenom("gabriel", 1)

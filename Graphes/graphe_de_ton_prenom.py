import sqlite3 
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
plt.style.use('dark_background')
def graphe_prenom(db_prenoms, prenoms_sexes: dict):

    liaison = sqlite3.connect(db_prenoms)
    curseur = liaison.cursor()
    plt.clf()
    curseur.execute("SELECT DISTINCT preusuel FROM prenoms;")
    prenoms = set([p_uplet[0] for p_uplet in curseur.fetchall()])
    curseur.execute("SELECT DISTINCT preusuel, sexe FROM prenoms;")
    prenoms_sexe = set([(p_uplet[0], int(p_uplet[1])) for p_uplet in curseur.fetchall()])
    existe = set(prenoms_sexes.keys()) <= prenoms_sexe
    fig = Figure(figsize=(5, 8), dpi=100)
    plot_naissances = fig.add_subplot(2, 1, 1)
    plot_rangs = fig.add_subplot(2, 1, 2)
    
    plot_naissances.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plot_naissances.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    
    plot_rangs.invert_yaxis()
    plot_rangs.set_yscale('log')
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
            plot_naissances.text(x_max, min(y), f"{int(x_max)}", color='red', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
            plot_naissances.text(x[0], y_max, f"{y_max}", color='red', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
            plot_naissances.plot(x, y, marker=None, linestyle='-', color=couleur, label=prenom)
            plot_naissances.scatter(x_max, max(y), marker='x', color='r', label=f"Max en x={x_max}", zorder=3)
            plot_naissances.set_xlabel("Années")
            plot_naissances.set_ylabel("Naissances")
            plot_naissances.set_title("Graphique avec abscisse du maximum")
            plot_naissances.legend()
            existe = (True and existe)

            annees = sorted([int(uplet[0]) for uplet in result if uplet[0] != 'XXXX'])
            rangs_par_annees = {}
            for annee in annees:
                curseur.execute("""
                    SELECT rang 
                    FROM (
                        SELECT *,
                        RANK() OVER (ORDER BY nombre DESC) as rang
                        FROM prenoms
                        WHERE annais = ? AND preusuel != '_PRENOMS_RARES' AND sexe = ?
                    )
                    WHERE preusuel = ?
                """, (annee, sexe, prenom.upper()))
                result =curseur.fetchall()
                if result:
                    rangs_par_annees[annee] = result[0][0]

            x, y = list(rangs_par_annees.keys()), list(rangs_par_annees.values())
            plot_rangs.plot(x, y, marker=None, linestyle='--', color=couleur)
        else:
            print("Ce prénom n'est pas dans la bdd")
    #        curseur.execute("SELECT DISTINCT preusuel FROM prenoms WHERE ")
            existe = (False and existe)

    return existe, fig
if __name__ == '__main__':
    graphe_prenom("gabriel", 1)

import sqlite3
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
plt.style.use('dark_background')
def graphe_prenom(db_prenoms: str, prenoms_sexes_couleur: dict, naiss_rangs_connus: dict):

    if naiss_rangs_connus is None:
        naiss_rangs_connus = dict()

    liaison = sqlite3.connect(db_prenoms)
    curseur = liaison.cursor()
    plt.clf()
    curseur.execute("SELECT DISTINCT preusuel FROM prenoms;")
    prenoms = set([p_uplet[0] for p_uplet in curseur.fetchall()])
    curseur.execute("SELECT DISTINCT preusuel, sexe FROM prenoms;")
    prenoms_sexe = set([(p_uplet[0], int(p_uplet[1])) for p_uplet in curseur.fetchall()])
    existe = set(prenoms_sexes_couleur.keys()) <= prenoms_sexe
    fig = Figure(figsize=(5, 8), dpi=100)
    plot_naissances = fig.add_subplot(2, 1, 1)
    plot_rangs = fig.add_subplot(2, 1, 2)

    plot_naissances.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plot_naissances.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    plot_rangs.xaxis.set_major_locator(ticker.MaxNLocator(nbins=(2022 - 1900)//10, integer=True))
    plot_rangs.invert_yaxis()
    plot_rangs.set_yscale('log')
    plot_rangs.yaxis.set_major_formatter(ScalarFormatter())

    existe = True
    curseur.execute("""SELECT DISTINCT annais FROM prenoms;""")
    result = curseur.fetchall()
    annees = sorted([int(uplet[0]) for uplet in result if uplet[0] != 'XXXX'])
    naiss_rangs_deja_calcules = naiss_rangs_connus.copy() # évite les effets de bord (pour les beaux yeux de RDB car elle a pas l'air de savoir ce que c'est)
    for prenom_sexe, couleur in prenoms_sexes_couleur.items():
        prenom, sexe = prenom_sexe
        if prenom.upper() in prenoms:
            if prenom_sexe not in naiss_rangs_deja_calcules:
                curseur.execute("SELECT annais, nombre FROM prenoms WHERE preusuel LIKE ? AND sexe = ? ORDER BY annais ;", (prenom.upper(), sexe))

                result = curseur.fetchall()
                dico_naissances = {annee : nombre for annee, nombre in result if annee != 'XXXX'}
                naiss_rangs_deja_calcules[prenom_sexe] = {}
                naiss_rangs_deja_calcules[prenom_sexe]['naissance'] = dico_naissances
                naiss_rangs_deja_calcules[prenom_sexe]['rangs'] = None
            else:

                dico_naissances = naiss_rangs_deja_calcules[prenom_sexe]['naissance']

            x = list(dico_naissances.keys())
            y = list(dico_naissances.values())
            plot_naissances.plot(x, y, linestyle='-', marker=None, color=couleur)
            plot_naissances.set_ylabel("Naissances")
            existe = (True and existe)

            if prenom_sexe not in naiss_rangs_deja_calcules or naiss_rangs_deja_calcules[prenom_sexe]['rangs'] == None:
                curseur.execute("""
                    SELECT annais, rang FROM (
                        SELECT annais, preusuel, nombre,
                               RANK() OVER (PARTITION BY annais ORDER BY nombre DESC) as rang
                        FROM prenoms
                        WHERE preusuel != '_PRENOMS_RARES' AND sexe = ?
                    )
                    WHERE preusuel = ?
                     """, (sexe, prenom.upper()))
                result = curseur.fetchall()
                if result:
                    for annee, rang in result:

                        rangs_par_annees = {annee : rang for annee, rang in result if annee != 'XXXX'}
                naiss_rangs_deja_calcules[prenom_sexe]['rangs'] = rangs_par_annees
            else:
                rangs_par_annees = naiss_rangs_deja_calcules[prenom_sexe]['rangs']
            x, y = list(rangs_par_annees.keys()), list(rangs_par_annees.values())
            plot_rangs.plot(x, y, marker=None, linestyle='-', color=couleur)
            plot_rangs.set_xlabel('Rangs')
            plot_rangs.set_ylabel('Années')

        else:
            print("Ce prénom n'est pas dans la bdd")
    #        curseur.execute("SELECT DISTINCT preusuel FROM prenoms WHERE ")
            existe = (False and existe)

    return existe, fig, naiss_rangs_deja_calcules

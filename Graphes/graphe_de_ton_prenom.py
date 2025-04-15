import sqlite3
import matplotlib

# Configuration de matplotlib pour un backend non interactif (utilisé souvent en production)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter

# Style de graphique avec fond sombre
plt.style.use('dark_background')

def graphe_prenom(db_prenoms: str, prenoms_sexes_couleur: dict, naiss_rangs_connus: dict) -> tuple:
    """Génère des graphiques d'évolution des naissances et des rangs pour des prénoms donnés.

    Args:
        db_prenoms (str): Chemin vers la base de données SQLite des prénoms.
        prenoms_sexes_couleur (dict): Dictionnaire de tuples (prénom, sexe) associés à des couleurs.
            Format: {(prénom, sexe): couleur_hex}
        naiss_rangs_connus (dict): Dictionnaire de données pré-calculées (optionnel).
            Format: {(prénom, sexe): {'naissance': {année: nb_naissances}, 'rangs': {année: rang}}}

    Returns:
        tuple: Contient:
            - existe (bool): True si tous les prénoms existent dans la base
            - fig (Figure): Objet Figure matplotlib contenant les graphiques
            - naiss_rangs_deja_calcules (dict): Données calculées (réutilisables)

    Note:
        - Crée deux subplots : naissances par année et évolution du rang
        - Le graphique des rangs utilise une échelle logarithmique inversée
    """
    if naiss_rangs_connus is None:
        naiss_rangs_connus = dict()

    # Connexion à la base de données
    liaison = sqlite3.connect(db_prenoms)
    curseur = liaison.cursor()
    plt.clf()  # Efface les figures précédentes

    # Récupération des prénoms uniques et des combinaisons prénom/sexe
    curseur.execute("SELECT DISTINCT preusuel FROM prenoms;")
    prenoms = set([p_uplet[0] for p_uplet in curseur.fetchall()])
    curseur.execute("SELECT DISTINCT preusuel, sexe FROM prenoms;")
    prenoms_sexe = set([(p_uplet[0], int(p_uplet[1])) for p_uplet in curseur.fetchall()])

    # Vérification que les prénoms demandés existent dans la base
    existe = set(prenoms_sexes_couleur.keys()) <= prenoms_sexe

    # Configuration de la figure matplotlib
    fig = Figure(figsize=(5, 8), dpi=100)
    plot_naissances = fig.add_subplot(2, 1, 1)  # Subplot pour les naissances
    plot_rangs = fig.add_subplot(2, 1, 2)       # Subplot pour les rangs

    # Configuration des axes pour le plot des naissances
    plot_naissances.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plot_naissances.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Configuration des axes pour le plot des rangs
    plot_rangs.xaxis.set_major_locator(ticker.MaxNLocator(nbins=(2022 - 1900)//10, integer=True))
    plot_rangs.invert_yaxis()  # Inversion pour avoir le rang 1 en haut
    plot_rangs.set_yscale('log')  # Échelle logarithmique pour mieux visualiser
    plot_rangs.yaxis.set_major_formatter(ScalarFormatter())  # Format numérique standard

    # Récupération des années disponibles
    curseur.execute("""SELECT DISTINCT annais FROM prenoms;""")
    result = curseur.fetchall()
    annees = sorted([int(uplet[0]) for uplet in result if uplet[0] != 'XXXX'])

    # Copie des données connues pour éviter les effets de bord
    naiss_rangs_deja_calcules = naiss_rangs_connus.copy()

    # Traitement pour chaque prénom
    for prenom_sexe, couleur in prenoms_sexes_couleur.items():
        prenom, sexe = prenom_sexe
        
        if prenom.upper() in prenoms:
            # Récupération des données de naissance si non déjà calculées
            if prenom_sexe not in naiss_rangs_deja_calcules:
                curseur.execute(
                    "SELECT annais, nombre FROM prenoms WHERE preusuel LIKE ? AND sexe = ? ORDER BY annais ;", 
                    (prenom.upper(), sexe))
                result = curseur.fetchall()
                dico_naissances = {annee: nombre for annee, nombre in result if annee != 'XXXX'}
                naiss_rangs_deja_calcules[prenom_sexe] = {
                    'naissance': dico_naissances,
                    'rangs': None
                }
            else:
                dico_naissances = naiss_rangs_deja_calcules[prenom_sexe]['naissance']

            # Tracé des naissances
            x = sorted([int(an) for an in dico_naissances.keys()])

            y = [dico_naissances[str(an)] for an in x]
            plot_naissances.plot(x, y, linestyle='-', marker=None, color=couleur)
            plot_naissances.set_ylabel("Naissances")

            # Récupération des rangs si non déjà calculés
            if prenom_sexe not in naiss_rangs_deja_calcules or naiss_rangs_deja_calcules[prenom_sexe]['rangs'] is None:
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
                    rangs_par_annees = {annee: rang for annee, rang in result if annee != 'XXXX'}
                    naiss_rangs_deja_calcules[prenom_sexe]['rangs'] = rangs_par_annees
            else:
                rangs_par_annees = naiss_rangs_deja_calcules[prenom_sexe]['rangs']

            # Tracé des rangs
            x, y = sorted([int(an) for an in rangs_par_annees.keys()]), [rangs_par_annees[str(an)] for an in x]
            plot_rangs.plot(x, y, marker=None, linestyle='-', color=couleur)
            plot_rangs.set_xlabel('Rangs')
            plot_rangs.set_ylabel('Années')
        else:
            print(f"Le prénom {prenom} n'est pas dans la base de données")

    return existe, fig, naiss_rangs_deja_calcules

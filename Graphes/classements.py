import sqlite3
import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict
def classements(prenom, sexe):
    conn = sqlite3.connect("prenoms.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT annais FROM prenoms;""")
    result = cursor.fetchall()

    annees = sorted([int(uplet[0]) for uplet in result if uplet[0] != 'XXXX'])
    rangs_par_annees = {}
    for annee in annees:
        cursor.execute("""
            SELECT rang 
            FROM (
                SELECT *,
                RANK() OVER (ORDER BY nombre DESC) as rang
                FROM prenoms
                WHERE annais = ? AND preusuel != '_PRENOMS_RARES' AND sexe = ?
            )
            WHERE preusuel = ?
        """, (annee, sexe, prenom.upper()))
        result = cursor.fetchall()
        if result:
            rangs_par_annees[annee] = result[0][0]
    
    conn.close()
    return rangs_par_annees
dico = classements('helenne', 2)

x_axis = list(dico.keys())
y_axis = list(dico.values())

plt.plot(x_axis, y_axis, marker=None, linestyle='-', color='blue')
plt.gca().invert_yaxis()
plt.show()

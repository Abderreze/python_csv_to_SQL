import sqlite3
import matplotlib.pyplot as plt

import matplotlib.ticker as ticker
plt.style.use('dark_background')
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

liaison = sqlite3.connect("prenoms.db")
curseur = liaison.cursor()
curseur.execute("""SELECT DISTINCT annais FROM prenoms WHERE annais != 'XXXX' ORDER BY annais;""")
result = curseur.fetchall()
annees = set(sorted([int(p_uplet[0]) for p_uplet in result]))
dico = {}
for annee in annees:
    if annee != 'XXXX':
        curseur.execute("""SELECT SUM(nombre) FROM prenoms WHERE annais = ?;""", (annee, ))
        result = curseur.fetchall()
        dico[int(annee)] = result[0][0]

x_axis = list(dico.keys())
y_axis = list(dico.values())


plt.plot(x_axis, y_axis, marker='o', linestyle='-', color='yellow', label='mais naan')
plt.show()

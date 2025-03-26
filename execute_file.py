import csv
import sqlite3 

liaison = sqlite3.connect("prenoms.db")
curseur = liaison.cursor()

curseur.execute("SELECT * FROM prenoms WHERE preusuel LIKE 'Cyprien%';")

# Fetch all rows from the query result
result = curseur.fetchall()
print(result)

liaison.close()

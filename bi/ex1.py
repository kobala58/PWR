from os import getenv
import pymssql
import csv

server = "172.17.0.2"
user = "sa"
password = "<TajneHaslo1234.>"

conn = pymssql.connect(server, user, password, "AdventureWorks2022")
cursor = conn.cursor()

cursor.execute("SELECT TerritoryID, Name, CountryRegionCode, SalesYTD, SalesLastYear FROM Sales.SalesTerritory")

with open("res.csv", "w") as file:
    writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(col[0] for col in cursor.description)
    for row in cursor.fetchall():
        writer.writerow(row)


conn.close()

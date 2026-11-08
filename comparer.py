# compare 2 inventaires
# python comparer.py ancien.csv nouveau.csv
# sans argument ca prend les 2 derniers du dossier exports

import csv
import glob
import sys


def lire(fichier):
    machines = {}
    with open(fichier, encoding="utf-8-sig") as f:
        for l in csv.DictReader(f, delimiter=";"):
            # je compare avec la mac parce que l'ip change avec le dhcp
            machines[l["mac"] or l["ip"]] = l
    return machines


if len(sys.argv) == 3:
    a, b = sys.argv[1], sys.argv[2]
else:
    fichiers = sorted(glob.glob("exports/inventaire_*.csv"))
    if len(fichiers) < 2:
        print("il faut au moins 2 fichiers dans exports/")
        sys.exit()
    a, b = fichiers[-2], fichiers[-1]

avant = lire(a)
apres = lire(b)
print(a, "->", b)
print()

for k in apres:
    if k not in avant:
        print("NOUVEAU    ", apres[k]["ip"], k, apres[k]["nom"])

for k in avant:
    if k not in apres:
        print("DISPARU    ", avant[k]["ip"], k, avant[k]["nom"])

for k in apres:
    if k in avant and avant[k]["ip"] != apres[k]["ip"]:
        print("IP CHANGEE ", avant[k]["ip"], "->", apres[k]["ip"], k)

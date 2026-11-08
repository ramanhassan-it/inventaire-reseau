# inventaire reseau
# ping tout le reseau, recupere les MAC dans la table arp et exporte en csv
# usage : python inventaire.py  (ou python inventaire.py 192.168.0.0/24)

import csv
import ipaddress
import os
import platform
import re
import socket
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

RESEAU = "192.168.1.0/24"
THREADS = 64

windows = platform.system() == "Windows"


def ping(ip):
    if windows:
        cmd = ["ping", "-n", "1", "-w", "800", ip]
    else:
        cmd = ["ping", "-c", "1", "-W", "1", ip]
    res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
    # sur windows le returncode est 0 meme si "hote injoignable" donc je check TTL
    return "ttl=" in res.stdout.lower()


def table_arp():
    macs = {}
    try:
        sortie = subprocess.run(["arp", "-a"], capture_output=True, text=True, errors="ignore").stdout
    except FileNotFoundError:
        print("pas de commande arp, les mac seront vides")
        return macs

    for ligne in sortie.splitlines():
        ip = re.search(r"\d+\.\d+\.\d+\.\d+", ligne)
        mac = re.search(r"([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}", ligne)
        if ip and mac:
            macs[ip.group()] = mac.group().replace("-", ":").upper()
    return macs


def nom(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return ""


if len(sys.argv) > 1:
    RESEAU = sys.argv[1]

debut = datetime.now()
ips = [str(i) for i in ipaddress.ip_network(RESEAU, strict=False).hosts()]
print("scan de", RESEAU, "...")

with ThreadPoolExecutor(THREADS) as ex:
    reponses = list(ex.map(ping, ips))
actives = [ip for ip, ok in zip(ips, reponses) if ok]

macs = table_arp()
# print(macs)

with ThreadPoolExecutor(THREADS) as ex:
    noms = list(ex.map(nom, actives))  # un peu lent des fois

os.makedirs("exports", exist_ok=True)
fichier = "exports/inventaire_" + debut.strftime("%Y-%m-%d_%H-%M") + ".csv"

# ; et utf-8-sig sinon excel ouvre tout dans une colonne
with open(fichier, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["ip", "mac", "nom", "date"])
    for ip, n in zip(actives, noms):
        w.writerow([ip, macs.get(ip, ""), n, debut.strftime("%Y-%m-%d %H:%M")])
        print(ip, macs.get(ip, "?"), n)

print(len(actives), "machines trouvees en", (datetime.now() - debut).seconds, "s")
print("->", fichier)

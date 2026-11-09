# inventaire-reseau

Script python qui fait l'inventaire de mon reseau tout seul.

Avant je le faisais a la main (page de la box + noter chaque appareil), ca me prenait environ 1h et j'oubliais toujours une machine. Maintenant ca prend 2 min.

Le script ping toutes les adresses du reseau, recupere les adresses MAC avec la table arp, essaye de trouver le nom des machines et met tout dans un csv avec la date.

Ensuite `comparer.py` compare deux csv pour voir ce qui a change (nouvel appareil, appareil disparu, ip changee).

## Utilisation

Rien a installer, que python.

```
python inventaire.py
python inventaire.py 192.168.0.0/24
python comparer.py
```

Les csv vont dans `exports/`. Y'a 2 fichiers dans `exemple/` pour tester comparer.py :

```
python comparer.py exemple/inventaire_2026-03-01_18-05.csv exemple/inventaire_2026-03-08_18-02.csv
```

```
NOUVEAU     192.168.1.88 7A:1F:30:C2:55:E8
DISPARU     192.168.1.77 5C:E9:1E:72:C4:10 tv-salon.home
IP CHANGEE  192.168.1.52 -> 192.168.1.63 F0:99:B6:3E:08:9C
```

## Problemes

- les machines qui bloquent le ping sont pas detectees
- mon pc a pas de mac dans le tableau (il est pas dans sa propre table arp)
- sous windows ping disait OK meme quand l'hote repondait pas, j'avais des machines fantomes. Corrige en regardant s'il y a "TTL" dans la reponse

## A faire

- afficher le fabricant avec la MAC
- lancer le scan tout seul chaque semaine
Mise à jour contributeurs

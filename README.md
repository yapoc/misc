# `extract_domains_from_leak.py`
Ce script recherche dans un grand nombre de fichiers la présence de chaines correspondant à certains domaines. Porduit un fichier `csv` en sortie avec les colonnes `domaine` & `login`.


```
usage: extract_domains_from_leak.py [-h] --dump DUMP_DIR --report REPORT
                                    --domain DOMAIN

Récupération des @mails correspondant à des domaines donnés

optional arguments:
  -h, --help       show this help message and exit
  --dump DUMP_DIR  Emplacement du dossier contenant le dump.
  --report REPORT  Emplacement du rapport.
  --domain DOMAIN  Domaine à rechercher
```

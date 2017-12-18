#!/usr/bin/env python
import argparse
import logging
import logging.handlers
import re
from os import walk
from os.path import join, isfile
logger = logging.getLogger (__name__)
handler = logging.handlers.RotatingFileHandler (filename = "extract_domains_from_leak.log", maxBytes = 1024 * 1024 * 10, backupCount = 1000)
handler.setFormatter ( logging.Formatter ("[%(asctime)s] - %(levelname)-8s - %(name)-15s - %(message)s") )
logger.addHandler (handler)
logger.setLevel (logging.INFO)

def get_files_in_folder (path):
  for triple in walk (path):
    for f in triple[2]:
      if isfile (join (triple[0], f)):
        if re.match ('^[a-z0-9]$', f):
          logger.debug ("Détection du fichier {}".format (join (triple[0], f)))
          yield join (triple[0], f)

def callback (line, domains):
  for d in domains:
    if d in line:
      yield (line, OK)
      break

def get_matching_in_dump (file, domains):
    logger.info ("Traitement du fichier {}".format (file))
    i = 0
    with open (file, 'rb') as leak_file:
      for l in leak_file.read ().decode ('utf-8', errors = 'ignore').split ('\n'):
        i += 1
        logger.debug ("{} - {} - 0".format (f, i))
        l = l.strip ()
        if not l:
          continue
        logger.debug (l)
        logger.debug ("{} - {} - 1".format (f, i))
        leaked = re.split ('[:@]', l)
        logger.debug ("{} - {} - 2".format (f, i))
        leaked[0] = leaked[0].lower ()
        logger.debug ("{} - {} - 3".format (f, i))
        leaked[1] = leaked[1].lower ()
        logger.debug ("{} - {} - 4".format (f, i))
        if len (leaked) > 3:
          logger.debug ("{} - {} - 5".format (f, i))
          logger.warn ("La ligne {} pourrait poser un problème au parsing.".format (l))
          callback (l, domains)
        else:
          logger.debug ("{} - {} - 6".format (f, i))
          if leaked[1] in domains:
            logger.debug ("{} - {} - 7".format (f, i))
            logger.info ("On a trouvé une entrée pour {}".format (leaked[1]))
            yield leaked[0], leaked[1]
          else:
            logger.debug ("{} - {} - 8".format (f, i))


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Récupération des @mails correspondant à des domaines donnés')
  parser.add_argument('--dump', type = str, help = 'Emplacement du dossier contenant le dump.',\
    dest = 'dump_dir', required = True)
  parser.add_argument ('--report', type = argparse.FileType ('w'), help = "Emplacement du rapport.", 
    dest = "report", required = True)
  parser.add_argument ('--domain', type = str, help = "Domaine à rechercher", dest = 'domain', required = True, action = 'append')
  args = parser.parse_args ()

  domains = [ d.lower () for d in args.domain ]

  for f in get_files_in_folder (args.dump_dir):
    for match in get_matching_in_dump (file = f, domains = domains):
      args.report.write ("{};{}\n".format (match[1], match[0]))

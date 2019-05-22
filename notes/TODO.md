# TODO

+ essayer et installer rshell: https://github.com/dhylands/rshell
  + on peut facilement utiliser rm, ls -l /pyboard & rsync pour deployer sur le device
  + et ensuite passer en repl: rshell -p /dev/ttyUSB0 repl
  + rshell -p /dev/ttyUSB0 -e nano "repl ~ import sensors"
+ mettre au point un workflow simple pour les cycles de développement/run/debug
  + utiliser le port unix de micropython pour tester au moins la syntaxe?

+ écrire une interface clean sympa pour chaque device
  + réviser les objets en python
  + voir comment gérer proprement les bytes/bytearray:
    + https://stackoverflow.com/questions/7380460/byte-array-in-python

+ faire un module pour gérer des breathing lights avec la LED
  + s'inspirer de https://www.dfrobot.com/blog-606.html
  + et prendre une fréquence de breathing comme paramètre
  + ex.: init: rapide, wifi ok: lent, tranquille

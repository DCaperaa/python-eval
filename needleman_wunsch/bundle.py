'''
Lance l'algorithme de Neddleman-Wunsch sur tous les couples de lignes du
fichier DATASET.txt et affiche la distance et les séquences alignées.
Si le nombre de ligne est impair, la dernière ligne est ignorée.
'''
from ruler import Ruler
import sys
DATASET = sys.argv[1]
# DATASET correspond au deuxième argument passé dans la ligne de commande.
with open(DATASET, 'r') as file:
    lines = file.readlines()
    i = 0
    while i+1 <= len(lines)-1:
        top = lines[i][:-1]
        bottom = lines[i+1][:-1]
        # on supprime le caractère de retour à la ligne avec le slicing
        ruler = Ruler(top, bottom)
        ruler.compute()
        aligned_top, aligned_bottom = ruler.report()
        print(f"====== example # {i//2 + 1} - distance = {ruler.distance}")
        print(aligned_top)
        print(aligned_bottom)
        i = i+2

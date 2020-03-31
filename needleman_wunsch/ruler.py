'''
Implémente une classe Ruler qui permet d'appliquer aux deux séquences top
et bottom l'algorithme de Needleman-Wunsch. Peut afficher la distance
entre les deux séquences ainsi que les séquences alignées.
'''
import numpy as np
from colorama import Fore, Style


def red_text(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


class Ruler:

    # Le code supporte une modification de la valeur de ces constantes.
    MATCH = 0  # Coût d'une correspondance entre les deux lettres comparées.
    MISMATCH = 1  # Coût d'un remplacement.
    GAP = 1  # Coût d'une insertion/effacement.

    def __init__(self, top, bottom):
        self.top = top
        self.bottom = bottom
        # Création de la matrice des substitutions utilisée dans l'algorithme.
        self.nblines = len(self.bottom) + 1
        self.nbcolumns = len(self.top) + 1
        self.matrix = np.zeros((self.nblines, self.nbcolumns))

    def compute(self):
        '''
        Calcule les coefficients de la matrice de l'algorithme, dont on peut
        déduire la distance et les séquences alignées.
        Modifie directement self.matrix.
        Doit être lancé explicitement par l'utilisateur.
        '''
        M = self.matrix
        M[0] = np.array([j * self.GAP for j in range(self.nbcolumns)])
        M[:, 0] = np.array([i * self.GAP for i in range(self.nblines)])
        for i in range(1, self.nblines):
            for j in range(1, self.nbcolumns):
                if self.top[j-1] == self.bottom[i-1]:
                    M[i, j] = min(M[i-1, j-1] + self.MATCH, M[i-1, j] +
                                  self.GAP, M[i, j-1] + self.GAP)
                else:
                    M[i, j] = min(M[i-1, j-1] + self.MISMATCH, M[i-1, j] +
                                  self.GAP, M[i, j-1] + self.GAP)

    def distance(self):
        '''
        Si la fonction compute a été exécutée, renvoie la distance entre les
        séquences top et bottom.
        '''
        if self.matrix[self.nblines-1, 0] == 0:
            # compute n'a pas été exéxutée
            return None
        return self.matrix[self.nblines-1, self.nbcolumns-1]

    distance = property(distance)

    def report(self):
        '''
        Construit les deux nouvelles séquences dites "alignées" à l'aide de
        l'étape de traceback de l'algorithme de Needleman-Wunsch.
        '''
        aligned_top = []
        aligned_bottom = []
        M = self.matrix
        # Le traceback est initié dans le coin en bas à droite, où se trouve
        # la distance entre les deux séquences.
        i, j = self.nblines-1, self.nbcolumns-1
        while i != 0 or j != 0:
            neighbooring_min = min(M[i-1, j-1], M[i-1, j], M[i, j-1])
            # Le fait qu'on parle en termes de distance et non d'alignement
            # comme dans l'algorithme originel impose de convertir les max en
            # min (c'est bien la distance minimale qu'on recherche).
            difference = M[i, j] - neighbooring_min
            if (i != 0 and j != 0 and difference == self.MATCH and M[i, j] ==
                    M[i-1, j-1] + self.MATCH):
                aligned_top.insert(0, self.top[j-1])
                aligned_bottom.insert(0, self.bottom[i-1])
                i, j = i-1, j-1
            elif (i != 0 and j != 0 and difference == self.MISMATCH
                  and M[i, j] == M[i-1, j-1] + self.MISMATCH):
                aligned_top.insert(0, f"{red_text(self.top[j-1])}")
                # le texte est stocké en rouge car il y a présence d'un MISMATCH.
                aligned_bottom.insert(0, f"{red_text(self.bottom[i-1])}")
                i, j = i-1, j-1
            elif (i != 0 and difference == self.GAP and M[i, j] ==
                  M[i-1, j] + self.GAP):
                # GAP dans la séquence self.top.
                aligned_top.insert(0, f"{red_text('=')}")
                aligned_bottom.insert(0, self.bottom[i-1])
                i = i-1
            elif (j != 0 and difference == self.GAP and M[i, j] ==
                  M[i, j-1] + self.GAP):
                # GAP dans la séquence self.bottom.
                aligned_top.insert(0, self.top[j-1])
                aligned_bottom.insert(0, f"{red_text('=')}")
                j = j-1
            else:
                raise ValueError("Le traceback n'a pas abouti.")
        return ''.join(aligned_top), ''.join(aligned_bottom)

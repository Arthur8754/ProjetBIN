"""
Dans cette classe, on implémente les distances dont on peut se servir dans les algorithmes/
"""

import numpy as np

class distances:

    def __init__(self):
        pass

    def dist_levenshtein(self, S1, S2):
        """
        Calcule la distance de Levenshtein entre les 2 séquences S1 et S2.
        """
        dico_cout = {True:0,False:1} #si les 2 caractères sont pareils -> True => coût de 0. Sinon, coût de 1
        sup_line = np.arange(start=0,stop=len(S2)+1,step=1,dtype=int) #ligne au-dessus de la ligne courant qu'on est en train de compléter
        current_line = np.copy(sup_line)
        for i in range(len(S1)):
            current_line[0] = i+1
            for j in range(1,len(sup_line)):
                match = S1[i] == S2[j-1]
                candidats = np.array([
                    sup_line[j-1] + dico_cout[match], #D[i-1,j-1] + cout
                    current_line[j-1]+1, #D[i,j-1]
                    sup_line[j]+1
                    ])
                current_line[j] = np.min(candidats)
            sup_line = np.copy(current_line)
        return sup_line[-1]

    def dist_hamming(self, S1, S2):
        """
        Calcule la distance de Hamming entre 2 séquences.
        Pour les parties communes entre S1 et S2, on regarde pour chaque caractère, et s'ils sont différents, on rajoute 1.
        Pour la partie restante (une seule des 2 séquences), on rajoute 1 à chaque caractère.
        """
        dist = 0
        min_seq = min(len(S1),len(S2)) #on recherche la séquence qui est la plus courte
        max_seq = max(len(S1),len(S2))
        rest = max_seq - min_seq
        for i in range(min_seq):
            if S1[i]!=S2[i]:
                dist+=1
        dist += rest
        return dist
        

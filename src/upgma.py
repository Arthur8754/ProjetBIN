"""
Ici, on implémente l'algorithme UPGMA vu en cours de BIN702

https://github.com/lex8erna/UPGMApy/blob/master/UPGMA.py

"""

import numpy as np
from Bio import Phylo
from io import StringIO
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

from src import distances


class upgma:

    def __init__(self,sequences,familles):
        self.sequences = sequences
        self.familles = familles
        self.tree = None
        self.D = [[] for k in range(len(sequences))]
        self.clusters = []
        self.famille_extract = 0 #pour l'extraction de clusters

    def init_D(self):
        """
        Initialise la matrice D en calculant la distance de Levenshtein entre sequences[i] et sequences[j] pour tout (i,j)
        Remarque : cette matrice est symétrique.
        """
        for i in range(len(self.sequences)):
            for j in range(len(self.sequences)):
                if j==i:
                    dist = 0
                elif i<j:
                    #dist = self.dist_levenshtein(self.sequences[i],self.sequences[j])
                    dist = distances.distances().dist_hamming(self.sequences[i], self.sequences[j])
                else:
                    dist = self.D[j][i]
                self.D[i].append(dist)

    def update_D(self,i_min,j_min):
        """
        Supprime les 2 séquences ajoutées dans l'arbre, et ajoute la "séquence réunie" dans D
        """
        # Ajout de la nouvelle colonne Si_minj_min
        for i in range(len(self.D)):
            if i!= i_min and i!= j_min: #on va supprimer la ligne i_min et j_min après.
                moy = self.moyenne_arithmetique(i_min,j_min,i)
                self.D[i].append(moy)

        # Suppression des 2 lignes correspondant à i_min et j_min
        self.D.pop(i_min)
        self.D.pop(j_min-1) #-1 car on a enlevé un élément avec i_min < j_min --> décalé de 1 vers le bas
        
        # Suppression des 2 colonnes correspondant à i_min et j_min
        for i in range(len(self.D)):
            self.D[i].pop(i_min)
            self.D[i].pop(j_min-1)

        # Ajout de la nouvelle ligne
        self.D.append([0 for i in range(len(self.D)+1)])
        i = len(self.D)-1
        for j in range(len(self.D)-1):
            self.D[i][j] = self.D[j][i] #symétrie

    def moyenne_arithmetique(self,i_min,j_min,indice):
        """
        Calcule la moyenne de D(i_min,indice) et de D(j_min,indice).
        i_min et j_min sont les indices des 2 séquences à joindre.
        indice est un indice d'une séquence quelconque.
        """
        moy = self.D[i_min][indice] + self.D[j_min][indice]
        return int(moy/2)

    def recherche_arg_min(self):
        """
        Recherche les indices indice_seq1 et indice_seq2 correspondant à la valeur minimale dans D
        """
        i_min,j_min = 0,1
        min = self.D[i_min][j_min]
        for i in range(len(self.D)):
            for j in range(i+1,len(self.D)): #la matrice étant symétrique, inutile de tout rechercher
                if self.D[i][j] < min:
                    i_min = i
                    j_min = j
                    min = self.D[i_min][j_min]
        return i_min,j_min


    def algo_upgma(self):
        """
        Applique l'algorithme UPGMA sur un ensemble de séquences [S1,...,Sm].
        Regroupe itérativement des séquences ensemble. Ex : 
        1. [S1,S2,S3,S4,S5] 
        2. [S1,(S2,S4),S3,S4,S5] puis [S1,(S2,S4),S3,S5] --> S2 et S4 les + proches, on les met ensemble
        3. [(S1,S3),(S2,S4),S5] --> S1 et S3 les plus proches
        4. [((S1,S3),(S2,S4)),S5] --> S13 et S24 les plus proches
        """
        self.init_D()
        jointures = 1*self.sequences #tableau des clusters.
        jointures_array = 1*self.sequences

        while len(self.D)>1:
            # Recherche de A et B tq dist(A,B) est minimale
            i_min,j_min = self.recherche_arg_min()

            # Jointure de A et B
            jointures[i_min] = "(" + jointures[i_min] + "," + jointures[j_min] + ")" #arbre au format newick
            jointures_array[i_min] = (jointures_array[i_min],jointures_array[j_min]) #format tuple (pas str)
            jointures.pop(j_min)
            jointures_array.pop(j_min)

            # Mise à jour de la matrice D
            self.update_D(i_min,j_min)

        return jointures[0], jointures_array[0]
            

    def dist_levenshtein(self,S1,S2):
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

    def generate_tree(self,jointures):
        self.tree = Phylo.read(StringIO(jointures),"newick")
        plt.figure(0)
        Phylo.draw(self.tree, lambda x : None, False)
        plt.title("Arbre phylogénétique obtenu grâce à l'algo UPGMA")
        plt.savefig("../figures/Tree_UPGMA.png")

    def extract_clusters(self,couple):
        """
        Crée récursivement des clusters à partir de couples
        """
        for i in range(2): #pour chaque valeur du couple
            if len(couple[i])!=2: #autrement dit, on n'a pas de tuple, c'est donc une str (une feuille)
                self.clusters.append(f'{self.famille_extract}')
            else: #on a toujours un tuple, on est à un noeud interne, il faut rappeler la fonction
                self.famille_extract += i
                self.extract_clusters(couple[i])
    
    def eval_perf(self, expected):
        """
        Évalue la qualité du clustering par rapport aux familles attendues.
        On construit une matrice de confusion, où chaque ligne est une famille "réelle", et chaque colonne est une famille prédite
        """
        conf_matrix = confusion_matrix(expected, self.clusters)
        print("Matrice de confusion :")
        print(conf_matrix)
        print("")
        accuracy = round(100*np.sum(np.diag(conf_matrix))/np.sum(conf_matrix),1) #somme des diagos / somme de tous les éléments
        print(f"Accuracy : {accuracy} %")

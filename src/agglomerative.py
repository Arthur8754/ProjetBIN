"""
Dans cette classe, on applique un algo de clustering hiérarchique (en ascendant) avec scikit learn
"""
#from src import readFastaGene
from confusion import confusion, confusion_print, perf_confusion
from proximiteEspece import proximite_global

"""
Dans cette classe, on va appliquer l'algorithme des KMeans sur nos gènes. Plus précisément, on va l'appliquer sur Levenshtein.
"""

import distances
from sklearn.cluster import AgglomerativeClustering
import readSimulateGene
import numpy as np
from sklearn.metrics import confusion_matrix

class agglomerative:

    def __init__(self, sequences, familles):
        self.sequences = sequences
        self.familles = familles
        self.prediction = None
        self.D = [[] for k in range(len(self.sequences))] #matrice de distance

    def clean_familles(self):
        """
        Fonction auxiliaire qui transforme ['1','1','2'...] en [1, 1, 2...]
        """
        for i in range(len(self.familles)):
            self.familles[i] = int(self.familles[i])
    
    def matrice_distance_levenshtein(self):
        """
        Crée la matrice de distances sur les séquences, en utilisant la distance de Levenshtein. Matrice de taille mxm, où m est le nb de séquences
        """
        for i in range(len(self.sequences)):
            for j in range(len(self.sequences)):
                if i==j:
                    dist=0
                elif i>j:
                    dist = self.D[j][i] #matrice symétrique
                else:
                    calculator = distances.distances()
                    dist = calculator.dist_levenshtein(self.sequences[i], self.sequences[j])
                    #dist = dist/max(len(self.sequences[i]),len(self.sequences[j])) #normalisation
                self.D[i].append(dist)

    def matrice_distance_hamming(self):
        """
        Crée la matrice de distances sur les séquences, en utilisant la distance de Hamming.
        """
        for i in range(len(self.sequences)):
            for j in range(len(self.sequences)):
                if i==j:
                    dist=0
                elif i>j:
                    dist = self.D[j][i] #matrice symétrique
                else:
                    calculator = distances.distances()
                    dist = calculator.dist_hamming(self.sequences[i], self.sequences[j])
                    #dist = dist/max(len(self.sequences[i]),len(self.sequences[j])) #normalisation
                self.D[i].append(dist)


    def algo_agglomerative_clustering(self, K):
        """
        Appel de la fonction AgglomerativeClustering de scikit learn. 
        """
        modele = AgglomerativeClustering(n_clusters=K)
        self.prediction = modele.fit_predict(self.D)
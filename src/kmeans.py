"""
Dans cette classe, on va appliquer l'algorithme des KMeans sur nos gènes. Plus précisément, on va l'appliquer sur Levenshtein.
"""

import distances
from sklearn.cluster import KMeans
import readSimulateGene
import numpy as np
from sklearn.metrics import confusion_matrix

class kmeans:

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


    def algo_kmeans(self, K):
        """
        Appel de la fonction KMeans de scikit learn. 
        """
        modele = KMeans(n_clusters=K)
        self.prediction = modele.fit_predict(self.D)
        
    def eval_perf(self):
        """
        Évalue la qualité du clustering par rapport aux familles attendues.
        On construit une matrice de confusion, où chaque ligne est une famille "réelle", et chaque colonne est une famille prédite
        """
        conf_matrix = confusion_matrix(self.familles, self.prediction)
        print("Matrice de confusion :")
        print(conf_matrix)
        print("")
        accuracy = round(100*np.sum(np.diag(conf_matrix))/np.sum(conf_matrix),1) #somme des diagos / somme de tous les éléments
        print(f"Accuracy : {accuracy} %")

def main():
    rsg = readSimulateGene.readSimulateGene()
    rsg.generate_sequences()
    sequences = rsg.sequences[0:10]
    familles = rsg.familles[0:10]
    km = kmeans(sequences, familles)
    km.clean_familles()
    #km.matrice_distance_levenshtein()
    km.matrice_distance_hamming()
    #print(km.D)
    km.algo_kmeans(len(np.unique(familles)))
    print("Familles prédites :")
    print(km.prediction)
    print("Familles attendues :")
    print(km.familles)
    km.eval_perf()

if __name__=="__main__":
    main()
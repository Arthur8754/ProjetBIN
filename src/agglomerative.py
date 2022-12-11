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
    sequences = rsg.sequences[0:20]
    familles = rsg.familles[0:20]
    agg = agglomerative(sequences, familles)
    agg.clean_familles()
    agg.matrice_distance_levenshtein()
    #agg.matrice_distance_hamming()
    print(agg.D)
    agg.algo_agglomerative_clustering(len(np.unique(familles)))
    print("Familles prédites :")
    print(agg.prediction)
    print("Familles attendues :")
    print(agg.familles)
    #agg.eval_perf()

    TP, TN, FP, FN = confusion(agg.prediction, agg.familles)
    confusion_print(TP, TN, FP, FN)
    accuracy, recall, precision, F1 = perf_confusion(TP, TN, FP, FN)

    print("accuracy :", accuracy)
    print("recall :", recall)
    print("precision :", precision)
    print("F1 : ", F1)


def main2():
    limit = 50
    N = 10  # Nb_familles_differentes
    rsg = readFastaGene.readFastaGene()
    rsg.get_sequence_Human_Pig_Mosquito(limit=limit)
    sequences = rsg.sequences
    familles = [k for k in range(N - 1)] + [0 for k in range(N-1,limit*3)]  # Pour avoir 10 familles différentes
    agg = agglomerative(sequences, familles)
    agg.clean_familles()
    #agg.matrice_distance_levenshtein()
    agg.matrice_distance_hamming()
    agg.algo_agglomerative_clustering(N)
    fam_human = agg.prediction[:limit]
    fam_pig = agg.prediction[limit:2 * limit]
    fam_mosquito = agg.prediction[2 * limit:]
    prox_Human_Pig = proximite_global(fam_human, fam_pig, N)
    print(f"proximité entre Humain et Cochon : {prox_Human_Pig * 100}%")
    prox_Human_Mosquito = proximite_global(fam_human, fam_mosquito, N)
    print(f"proximité entre Humain et Moustique : {prox_Human_Mosquito * 100}%")

if __name__=="__main__":
    main()
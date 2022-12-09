"""
Dans cette classe, on va appliquer l'algorithme des KMeans sur nos gènes. Plus précisément, on va l'appliquer sur Levenshtein.
"""
import pandas as pd

import distances
from sklearn.cluster import KMeans
import readFastaGene
import readSimulateGene
import numpy as np
from sklearn.metrics import confusion_matrix

from src.confusion import confusion_print, confusion, perf_confusion
from src.proximiteEspece import *

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

    TP, TN, FP, FN = confusion(km.prediction, km.familles)
    confusion_print(TP, TN, FP, FN)
    accuracy, recall, precision, F1 = perf_confusion(TP,TN,FP,FN)

    print("accuracy :", accuracy)
    print("recall :", recall)
    print("precision :", precision)

def main2():
    rsg = readFastaGene.readFastaGene()
    rsg.get_sequences(limit=30)
    sequences = rsg.sequences
    familles = rsg.familles
    print(familles,len(familles))

    km = kmeans(sequences, familles)
    km.clean_familles()
    # km.matrice_distance_levenshtein()
    km.matrice_distance_hamming()
    # print(km.D)
    km.algo_kmeans(len(np.unique(familles)))
    print("Familles prédites :")
    print(km.prediction)
    print("Familles attendues :")
    print(km.familles)

    TP, TN, FP, FN = confusion(km.prediction, km.familles)
    confusion_print(TP, TN, FP, FN)
    accuracy, recall, precision, F1 = perf_confusion(TP, TN, FP, FN)

    print("accuracy :", accuracy)
    print("recall :", recall)
    print("precision :", precision)

def main_prediction_Human_Pig():
    limit = 50
    rsg = readFastaGene.readFastaGene()
    rsg.get_sequences(limit=limit)
    sequences = rsg.sequences
    N = 10 #Nb_familles_differentes
    familles = [k for k in range(N-1)] + [0 for k in range(limit-(N-1))] #Pour avoir 10 familles différentes
    km = kmeans(sequences, familles)
    km.clean_familles()
    # km.matrice_distance_levenshtein()
    km.matrice_distance_hamming()
    # print(km.D)
    km.algo_kmeans(len(np.unique(familles)))
    fam_human = km.prediction[:limit]
    fam_pig = km.prediction[limit:]
    print("fam_human : ",fam_human)
    print("fam_pig   : ",fam_pig)

    prox = proximite_global(fam_human, fam_pig, N)
    print(f"proximité entre Humain et Cochon : {prox*100}%")
def main_prediction_Human_Mosquito():
    limit = 50
    rsg = readFastaGene.readFastaGene()
    rsg.get_sequences_mosquito(limit=limit)
    sequences = rsg.sequences
    N = 10 #Nb_familles_differentes
    familles = [k for k in range(N-1)] + [0 for k in range(limit-(N-1))] #Pour avoir 10 familles différentes
    km = kmeans(sequences, familles)
    km.clean_familles()
    # km.matrice_distance_levenshtein()
    km.matrice_distance_hamming()
    # print(km.D)
    km.algo_kmeans(len(np.unique(familles)))
    fam_human = km.prediction[:limit]
    fam_mosquito = km.prediction[limit:]
    print("fam_Human : ",fam_human)
    print("fam_Mosquito   : ",fam_mosquito)
    prox = proximite_global(fam_human, fam_mosquito, N)
    print(f"proximité entre Humain et Moustique : {prox*100}%")

def main_prediction_Human_Mosquito_Pig():
    limit = 50
    N = 10  # Nb_familles_differentes


    rsg = readFastaGene.readFastaGene()
    rsg.get_sequence_Human_Pig_Mosquito(limit=limit)
    sequences = rsg.sequences
    familles = [k for k in range(N - 1)] + [0 for k in range(N - 1, limit * 3)]  # Pour avoir 10 familles différentes
    km = kmeans(sequences, familles)
    km.clean_familles()
    #km.matrice_distance_levenshtein()
    km.matrice_distance_hamming()
    # print(km.D)
    km.algo_kmeans(len(np.unique(familles)))
    print(len(km.prediction))
    fam_human = km.prediction[:limit]
    fam_pig = km.prediction[limit:2*limit]
    fam_mosquito = km.prediction[2*limit:]
    prox_Human_Pig = proximite_global(fam_human, fam_pig, N)
    print(f"proximité entre Humain et Cochon : {prox_Human_Pig * 100}%")
    prox_Human_Mosquito = proximite_global(fam_human, fam_mosquito, N)
    print(f"proximité entre Humain et Moustique : {prox_Human_Mosquito * 100}%")

if __name__=="__main__":
    #main_prediction_Human_Pig()
    #main_prediction_Human_Mosquito()
    main_prediction_Human_Mosquito_Pig()
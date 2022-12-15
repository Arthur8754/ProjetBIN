import numpy as np

import simulateGene
import readSimulateGene
import readFastaGene
import kmeans
import agglomerative
import upgma
import sys

from confusion import confusion, confusion_print, perf_confusion
from proximiteEspece import proximite_global

def main():
    """
    methode : kmeans, agglomerative, upgma
    simulated : 1 si données simulées, 0 si gènes réels
    hamming = 1 si distance de Hamming, 0 si distance de Levenshtein
    """

    if len(sys.argv)<4:
        usage = "\n Usage: python main.py methode simulated hamming \
        \n\n\t methode : kmeans, agglomerative, upgma \
        \n\t simulated : 1 : gènes simulés ; 0 : gènes réels \
        \n\t hamming : 1 : distance de Hamming ; 0 : distance de Levenshtein \n"
        print(usage)
        return

    methode = sys.argv[1]
    simulated = int(sys.argv[2])
    hamming = int(sys.argv[3])

    if simulated == 1:
        sim = simulateGene.simulateGene("./genes",10,20)
        sim.generate_genes()

        readSim = readSimulateGene.readSimulateGene()
        readSim.generate_sequences()
        sequences = readSim.sequences[0:30]
        familles = readSim.familles[0:30]

        if methode == "kmeans":
            print("KMEANS : ")
            print("-----------------")
            km = kmeans.kmeans(sequences, familles)
            km.clean_familles()
            
            if hamming == 1:
                km.matrice_distance_hamming()
            else:
                km.matrice_distance_levenshtein()
            
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
            print("F1 : ",F1)
        
        elif methode == "agglomerative":
            print("AGGLOMERATIVE : ")
            print("-----------------")
            agg = agglomerative.agglomerative(sequences, familles)
            agg.clean_familles()
            
            if hamming == 1:
                agg.matrice_distance_hamming()
            else:
                agg.matrice_distance_levenshtein()
            
            agg.algo_agglomerative_clustering(len(np.unique(familles)))
            print("Familles prédites :")
            print(agg.prediction)
            print("Familles attendues :")
            print(agg.familles)

            TP, TN, FP, FN = confusion(agg.prediction, agg.familles)
            confusion_print(TP, TN, FP, FN)
            accuracy, recall, precision, F1 = perf_confusion(TP,TN,FP,FN)
            print("accuracy :", accuracy)
            print("recall :", recall)
            print("precision :", precision)
            print("F1 : ",F1)
        
        else:
            print("UPGMA")
            print("-----------------")
            up = upgma.upgma(sequences, familles)

            # Application de l'algorithme UPGMA :
            jointures, jointures_array = up.algo_upgma()

            # Extraction des clusters :
            up.extract_clusters(jointures_array)

            print("Familles attendues :")
            print(familles)
            print("Familles prédites :")
            print(up.clusters)

            TP, TN, FP, FN = confusion(familles, up.clusters)
            confusion_print(TP, TN, FP, FN)
            accuracy, recall, precision, F1 = perf_confusion(TP, TN, FP, FN)

            print("accuracy :", accuracy)
            print("recall :", recall)
            print("precision :", precision)
            print("F1 : ",F1)

    else:
        limit = 50
        rsg = readFastaGene.readFastaGene()
        rsg.get_sequence_Human_Pig_Mosquito(limit=limit)
        sequences = rsg.sequences
        N = 10 #Nb_familles_differentes
        familles = [k for k in range(N-1)] + [0 for k in range(limit-(N-1))] #Pour avoir 10 familles différentes

        if methode == "kmeans":
            print("KMEANS : ")
            print("-----------------")
            km = kmeans.kmeans(sequences, familles)
            km.clean_familles()
            
            if hamming == 1:
                km.matrice_distance_hamming()
            else:
                km.matrice_distance_levenshtein()
            
            km.algo_kmeans(len(np.unique(familles)))
            fam_human = km.prediction[:limit]
            fam_pig = km.prediction[limit:2*limit]
            fam_mosquito = km.prediction[2*limit:]
            prox_Human_Pig = proximite_global(fam_human, fam_pig, N)
            print(f"proximité entre Humain et Cochon : {prox_Human_Pig * 100}%")
            prox_Human_Mosquito = proximite_global(fam_human, fam_mosquito, N)
            print(f"proximité entre Humain et Moustique : {prox_Human_Mosquito * 100}%")
        
        elif methode == "agglomerative":
            print("AGGLOMERATIVE : ")
            print("-----------------")
            agg = agglomerative.agglomerative(sequences, familles)
            agg.clean_familles()
            
            if hamming == 1:
                agg.matrice_distance_hamming()
            else:
                agg.matrice_distance_levenshtein()
            
            agg.algo_agglomerative_clustering(len(np.unique(familles)))
            fam_human = agg.prediction[:limit]
            fam_pig = agg.prediction[limit:2*limit]
            fam_mosquito = agg.prediction[2*limit:]
            prox_Human_Pig = proximite_global(fam_human, fam_pig, N)
            print(f"proximité entre Humain et Cochon : {prox_Human_Pig * 100}%")
            prox_Human_Mosquito = proximite_global(fam_human, fam_mosquito, N)
            print(f"proximité entre Humain et Moustique : {prox_Human_Mosquito * 100}%")
        
        else:
            print("UPGMA")
            print("-----------------")
            print("Ce cas n'a pas été géré.")

if __name__=="__main__":
    main()
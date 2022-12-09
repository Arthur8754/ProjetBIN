import numpy as np

import simulateGene
import readSimulateGene
import upgma
import matplotlib.pyplot as plt

from src import readFastaGene
from src.confusion import confusion, confusion_print, perf_confusion
from src.proximiteEspece import proximite_global


def test_upgma(sequences, familles):
    up = upgma.upgma(sequences, familles)
    
    print("Séquences (extrait) :")
    print(up.sequences[0:5])
    print("")
    print("Familles (extrait) :")
    print(up.familles[0:5])
    # Application de l'algorithme UPGMA :
    jointures, jointures_array = up.algo_upgma()

    # Extraction des clusters :
    up.extract_clusters(jointures_array)

    print("Familles attendues :")
    print(familles)
    print("")
    print("Familles prédites :")
    print(up.clusters)
    print("")

    # Évaluation des performances de l'algo de clustering :
    #up.eval_perf(familles)

    TP, TN, FP, FN = confusion(familles, up.clusters)
    confusion_print(TP, TN, FP, FN)
    accuracy, recall, precision, F1 = perf_confusion(TP, TN, FP, FN)

    print("accuracy :", accuracy)
    print("recall :", recall)
    print("precision :", precision)
    # Génération de l'arbre : 
    up.generate_tree(jointures)


def main():
    sg = simulateGene.simulateGene("./genes",10,20)

    # Simulation des familles de gènes
    sg.generate_genes()

    # Génération du tableau de séquences et de gènes :
    rsg = readSimulateGene.readSimulateGene()
    rsg.generate_sequences()

    # Algorithme UPGMA :
    test_upgma(rsg.sequences[0:10], rsg.familles[0:10])

def main2():
    limit = 50
    rsg = readFastaGene.readFastaGene()
    rsg.get_sequence_Human_Pig_Mosquito(limit=limit)
    sequences = rsg.sequences
    print(len(sequences))
    N = 10  # Nb_familles_differentes
    familles = [k for k in range(N - 1)] + [0 for k in range(limit - (N - 1))]  # Pour avoir 10 familles différentes
    up = upgma.upgma(sequences, familles)
    # Application de l'algorithme UPGMA :
    jointures, jointures_array = up.algo_upgma()
    # Extraction des clusters :
    up.extract_clusters(jointures_array)
    #up.generate_tree(jointures)
    #print(up.clusters)
    prediction = up.clusters
    for k in range(len(prediction)):
        prediction[k] = int(prediction[k])
    fam_human = prediction[:limit]
    fam_pig = prediction[limit:2 * limit]
    fam_mosquito = prediction[2 * limit:]
    Nfam = len(np.unique(prediction))
    prox_Human_Pig = proximite_global(fam_human, fam_pig, Nfam)
    print(f"proximité entre Humain et Cochon : {prox_Human_Pig * 100}%")

    print(len(fam_mosquito),len(fam_human))
    prox_Human_Mosquito = proximite_global(fam_human, fam_mosquito, Nfam)
    print(f"proximité entre Humain et Moustique : {prox_Human_Mosquito * 100}%")

if __name__=="__main__":
    main2()
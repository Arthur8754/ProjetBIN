import simulateGene
import readSimulateGene
import upgma
import matplotlib.pyplot as plt

from src.confusion import confusion, confusion_print, perf_confusion


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


if __name__=="__main__":
    main()
"""
https://pub.uni-bielefeld.de/download/2301975/2301978/thesis.pdf
http://lifesciencessociety.org/CSB2007/toc/PDF/391.2007.pdf

Dans cette classe, on implémente l'algorithme de Transitive Clustering de l'article.
ALGO : idée : partir d'un graphe non transitif, et le rendre transitif (union disjointe de cliques)
1. On lie i et j si le score de similarité est supérieur (strictement) à un seuil T
2. On effectue une transformation de ce graphe pour obtenir un graphe transitif. Pour ce faire, on utilise le WTGPP, qu'on va approximer par une 
   heuristique (car pb NP-complet), on va faire ça à l'aide d'une programmation linéaire (section 3.4.4)
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class transClust:

    def __init__(self, sequences, M, T) -> None:
        self.graphe = nx.Graph()
        self.sequences = sequences
        self.M = M #matrice de similarité
        self.T = T #seuil pour l'initialisation du graphe

    def compute_M(self):
        """
        Calcule la matrice de similarité du graphe
        """
        M = [[] for k in range(len(self.sequences))]
        for i in range(len(self.sequences)):
            for j in range(len(self.sequences)):
                if j==i:
                    dist = 0
                elif i<j:
                    dist = self.dist_levenshtein(self.sequences[i],self.sequences[j])
                    dist = dist/max(len(self.sequences[i]), len(self.sequences[j]))
                else:
                    dist = self.M[j][i]
                M[i].append(1-dist) #1-pour avoir une similarité
        return M

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

    def init_graph(self):
        m = len(self.sequences) #nombre de séquences
        # Création des noeuds :
        for i in range(m):
            self.graphe.add_node((i,self.sequences[i]))
        
        # Création des arêtes initiales : si M(i,j) > T, on lie i et j
        for i in range(m):
            for j in range(i+1,m): #matrice symétrique
                if self.M[i][j] > self.T:
                    node1 = (i,self.sequences[i])
                    node2 = (j,self.sequences[j])
                    self.graphe.add_edge(node1, node2)
    
    def vizualize_graph(self):
        nx.draw_networkx(self.graphe, with_labels=True, node_color='red')
        plt.savefig("graph.png")

    def remove_cuplrit(self):
        """
        Supprime l'arête qui maximise le score de similarité
        """
        argmax = (0,self.sequences[0],1,self.sequences[1])
        max_delta = 0
        D = 0
        m = len(self.sequences)
        for u in range(m):
            for v in range(u+1,m):
                for w in range(v+1,m):
                    D += min(self.M[u][v], self.M[v][w], self.M[u][w])

        for u in range(m):
            for v in range(u+1,m):
                Dprime = 0
                try:
                    self.graphe.remove_edge((u,self.sequences[u]),(v,self.sequences[v]))
                    oldMuv = self.M[u][v]
                    self.M[u][v] = -1000 #-infini
                    for w in range(m):
                        Dprime += min(self.M[u][v], self.M[v][w], self.M[u][w])
                    self.M[u][v] = oldMuv
                    delta = D - Dprime - self.M[u][v]
                    if delta > max_delta:
                        argmax = (u,self.sequences[u],v,self.sequences[v])
                        max_delta = delta
                    self.graphe.add_edge((u,self.sequences[u]),(v,self.sequences[v]))
                except:
                    continue
        try:
            self.graphe.remove_edge((argmax[0],argmax[1]),(argmax[2],argmax[3]))    
            return argmax
        except:
            return argmax


    def transitive_closure_cost(self):
        """
        Retourne le coût pour ajouter toutes les arêtes nécessaires pour obtenir le graphe transitif.
        """
        cout = 0
        m = len(self.sequences)
        for i in range(m):
            for j in range(i+1,m):
                print(self.M[i][j])
                cout += max(-self.M[i][j],0) # coût(i,j) <=> - similarité(i,j)
        return cout

    def transitive_graph(self):
        """
        Méthode qui permet d'obtenir un graphe transitif, à l'aide d'une heuristique
        """
        print(self.graphe)
        # 1.
        cost = self.transitive_closure_cost()

        # 2.
        if cost == 0:
            return [],0
        
        else:
            #3.
            deletions, delcost = [],0
            
            #4.
            number_components = len(list(nx.connected_components(self.graphe))) #nombre de sous-graphes disjoints dans le graphe
            #number_components = nx.number_connected_components(self.graphe) #nombre de sous-graphes disjoints dans le graphe
            while number_components <= 2:
                u, sequ, v, seqv = self.remove_cuplrit()
                deletions.append((u,sequ, v, seqv))
                delcost += self.M[u][v]
                number_components = len(list(nx.connected_components(self.graphe))) #nombre de sous-graphes disjoints dans le graphe
                #print(number_components)
        
            #5.
            for u, sequ, v, seqv in deletions:
                try:
                    self.graphe.remove_edge((u,sequ),(v,seqv))
                    if number_components ==2:
                        self.graphe.add_edge((u,sequ),(v,seqv))
                        deletions.remove((u,sequ,v,seqv))
                        delcost -= self.M[u][v]
                except:
                    continue

            # 6. 
            if delcost >= cost:
                return [],cost
            components = list(nx.connected_components(self.graphe))
            print(components)
            tc1 = transClust(self.sequences, self.M, self.T) #faudrait mettre à jour sequences et M
            tc1.graphe = self.graphe.subgraph(components[0])
            deletions1, cost1 = tc1.transitive_graph()
            if delcost + cost1 >= cost:
                return [], cost
            tc2 = transClust(self.sequences, self.M, self.T)
            tc2.graphe = self.graphe.subgraph(components[1])
            deletions2, cost2 = tc2.transitive_graph()
            if delcost + cost1 + cost2 >= cost:
                return [], cost

            # 7.
            deletions.append(deletions1)
            deletions.append(deletions2)
            return deletions, delcost + cost1 + cost2





    def algo_transclust(self):
        """
        Applique l'algorithme de Transitive Clustering.
        """
        # INITIALISATION DU GRAPHE :
        self.init_graph()

        # GRAPHE TRANSITIF :
        deletions, cost = self.transitive_graph()

    def extract_clusters(self):
        #print(nx.find_cliques(self.graphe))
        print(nx.cliques_containing_node(self.graphe)) #À CHANGER

def main():
    sequences = ["A","B","C","D","E"]
    M = [
        [1,-1,1,2,-3],
        [-1,1,-1,1,2],
        [1,-1,1,0,4],
        [2,1,0,1,-2],
        [-3,2,4,-2,1]
    ]
    T = 0
    tc = transClust(sequences, M, T)
    tc.algo_transclust()
    tc.vizualize_graph()

if __name__=="__main__":
    main()
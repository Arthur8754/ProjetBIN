"""
Dans cette classe, on implémente la structure de graphe qui sera utile dans les algorithmes de l'article à résumer.
Pour construire cette classe, je me suis inspiré de "util_gro_tp2.py" qu'on avait fait dans le TP2 de GRO l'an dernier à TN.
"""

class Node:
    """
    Classe associée à un noeud du graphe
    """

    def __init__(self, numero, value):
        self.numero = numero #numéro du noeud (plus facile à identifier)
        self.value = value #contenu du noeud (une séquence en l'occurrence)
        self.voisins = {} #clé --> numero du noeud d'un voisin, valeur : le noeud

    def link_noeuds(self, noeud):
        """
        Lie le noeud couranta avec le noeud "noeud"
        """
        if noeud.numero not in self.voisins.keys():
            self.voisins[noeud.numero] = noeud #on ajoute noeud dans les voisins du noeud courant
            noeud.voisins[self.numero] = self #on ajoute le noeud courant dans les voisins de noeud
        else:
            print("WARNING : les deux noeuds sont déjà reliés.")
        return noeud #on retourne pour mettre à jour les 2 noeuds en même temps

    def dislink_noeuds(self, noeud):
        """
        Casse le lien qu'il y avait entre le noeud courant et le noeud "noeud"
        """
        if noeud.numero in self.voisins.keys():
            del self.voisins[noeud.numero] #on supprime noeud des voisins du noeud courant
            del noeud.voisins[self.numero] #on supprime le noeud courant des voisins de noeud
        else:
            print("WARNING : les deux ne sont pas reliés, rien à enlever.")
        return noeud
    

class GrapheNonOriente:
    """
    Classe associé à la création d'un graphe orienté :
    """

    def __init__(self, nom_graphe):
        """
        Le graphe de base est un graphe sans noeud.
        """
        self.nom = nom_graphe #nom du graphe
        self.noeuds = {} #clé : identifiant du noeud, valeur : noeud

    def add_noeud(self, noeud):
        """
        Ajoute un noeud dans le graphe. Suppose que le noeud ajouté possède un numéro et une valeur non vide.
        Si un noeud avec le même numéro est déjà présent dans le graphe, le noeud n'est pas ajouté.
        """
        if noeud.numero not in self.noeuds.keys():
            self.noeuds[noeud.numero] = noeud
        else:
            print("WARNING : le noeud à ajouter existe déjà.")

    def add_arete(self, noeud1, noeud2):
        """
        Ajoute une arête entre noeud1 et noeud2.
        Si l'un des 2 noeuds n'est pas dans le graphe, l'arête n'est pas ajoutée.
        """
        if noeud1.numero in self.noeuds.keys() and noeud2.numero in self.noeuds.keys():
            self.noeuds[noeud1.numero] = self.noeuds[noeud2.numero].link_noeuds(noeud1) #on lie noeud1 et noeud2.
        else:
            print("WARNING : l'un des noeuds n'est pas dans le graphe.")

    def enlever_arete(self, noeud1, noeud2):
        """
        Enlève l'arête qui liait noeud1 et noeud2
        Si l'un des 2 noeuds n'est pas dans le graphe, rien ne se passe.
        """
        if noeud1.numero in self.noeuds.keys() and noeud2.numero in self.noeuds.keys():
            self.noeuds[noeud1.numero] = self.noeuds[noeud2.numero].dislink_noeuds(noeud1) #on supprime le lien entre noeud1 et noeud2.
        else:
            print("WARNING : l'un des noeuds n'est pas dans le graphe.")

def main():
    """
    On construit le graphe suivant :
    0 ---- 1 ------- 2
           |         |
           3 ---------
    0 est relié à 1
    1, 2 et 3 sont tous reliés entre eux.
    """
    graphe = GrapheNonOriente("Graphe test")
    noeud0 = Node(0,"0")
    noeud1 = Node(1,"1")
    noeud2 = Node(2,"2")
    noeud3 = Node(3,"3")

    graphe.add_noeud(noeud0)
    graphe.add_noeud(noeud1)
    graphe.add_noeud(noeud2)
    graphe.add_noeud(noeud3)

    print("Noeuds du graphe construit :")
    print(graphe.noeuds)
    print("")

    graphe.add_arete(noeud0, noeud1)
    graphe.add_arete(noeud1, noeud2)
    graphe.add_arete(noeud1, noeud3)
    graphe.add_arete(noeud2, noeud3)

    print("Voisins pour chaque noeud :")
    print("Voisins de 0 : ",graphe.noeuds[0].voisins)
    print("Voisins de 1 : ",graphe.noeuds[1].voisins)
    print("Voisins de 2 : ",graphe.noeuds[2].voisins)
    print("Voisins de 3 : ",graphe.noeuds[3].voisins)
    print("")

    """
    On va enlever une des arêtes désormais. On va enlever l'arête entre 1 et 3.
    """

    print("Suppression de l'arête entre 1 et 3 :")
    graphe.enlever_arete(noeud1, noeud3)
    print("Nouveaux voisins de 1 : ",graphe.noeuds[1].voisins)
    print("Nouveaux voisins de 3 : ",graphe.noeuds[3].voisins)

if __name__ == "__main__":
    main()

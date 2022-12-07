"""
Au sein de ce fichier, on lit les fichiers fasta créés par le script "simulateGene", et on en extrait une structure de données exploitables par les algorithmes futurs.
Plus précisément, on va créer 2 listes : sequences et familles, où familles[i] = famille de sequences[i]
"""

import re
import os

class readSimulateGene:
    
    def __init__(self):
        self.sequences = [] #tableau des différentes séquences du fichier fasta
        self.familles = [] #tableau des familles associées

    def read_fasta_file(self,filepath):
        """
        Lit le fichier fasta self.filepath, et extrait un tableau de séquences contenues dans ce fichier, ainsi que les familles associées à chacune des séquences.
        """
        header_pattern = r">fam(?P<family_number>[0-9]+)gene(?P<gene_number>[0-9]+)spec(?P<species_number>[0-9]+)"
        with open(filepath) as file:
            family_number,seq = None,[] #famille courante, séquence courante
            for line in file:
                match = re.match(header_pattern,line)
                if match is not None:
                    if family_number is not None: #si on trouve un nouveau header
                        self.sequences.append(''.join(seq)) #on stocke "l'ancienne séquence" (du header précédent)
                        seq=[]
                    family_number = match["family_number"] #on stocke l'header courant
                    self.familles.append(family_number)
                else:
                    seq.append(line.replace("\n",""))
            #Dernière séquence
            if family_number is not None: #si on trouve un nouveau header
                self.sequences.append(''.join(seq)) #on stocke "l'ancienne séquence" (du header précédent)

    def generate_sequences(self):
        for root, dirs, files in os.walk("genes/fasta_files"):
            for file in files:
                self.read_fasta_file("genes/fasta_files/" + file)

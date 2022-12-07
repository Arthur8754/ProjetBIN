import re
import os


class readFastaGene:

    def __init__(self):
        self.sequences = []  # tableau des différentes séquences du fichier fasta
        self.familles = []

    def read_fasta_file(self, filepath, filename, limit):
        """
        Lit le fichier fasta self.filepath, et extrait un tableau de séquences contenues dans ce fichier, ainsi que les familles associées à chacune des séquences.
        """
        header_pattern = r">lcl*"
        countPig,countHuman = 0,0
        with open(filepath + filename) as file:
            seq = []  # séquence courante
            for line in file:
                match = re.match(header_pattern, line)
                if match is not None:
                    if filename == "genesHuman.fna" and countHuman<limit :
                        self.sequences.append(''.join(seq))  # on stocke "l'ancienne séquence" (du header précédent)
                        seq = []
                        self.familles.append("0")
                        countHuman+=1
                    elif filename == "genesPig.fna" and countPig<limit :
                        self.sequences.append(''.join(seq))  # on stocke "l'ancienne séquence" (du header précédent)
                        seq = []
                        self.familles.append("1")
                        countPig += 1
                    elif countPig>=limit and countHuman>=limit:
                        break
                else:
                    seq.append(line.replace("\n", ""))
            if countPig<limit and countHuman<limit: #utile que si on va jusqu'au bout du fichier
                self.sequences.append(''.join(seq))  # on stocke "l'ancienne séquence" (du header précédent)

    def get_sequences(self,limit):
        files = ["genesHuman.fna",'genesPig.fna']
        for file in files:
            self.read_fasta_file("data/",file, limit)

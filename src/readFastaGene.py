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

    def read_fasta_file_mosquito(self, filepath, filename, limit):
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
                    elif filename == "genesMosquito.fna" and countPig<limit :
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
            self.read_fasta_file("genes/fasta_files/",file, limit)

    def get_sequences_mosquito(self,limit):
        files = ["genesHuman.fna",'genesMosquito.fna']
        for file in files:
            self.read_fasta_file_mosquito("genes/fasta_files/", file, limit)

    def read_fast_file_all(self,filepath,filename,limit):
        header_pattern = r">lcl*"
        countMosquito, countPig, countHuman = 0, 0, 0
        with open(filepath + filename) as file:
            seq = []  # séquence courante
            for line in file:
                match = re.match(header_pattern, line)
                if match is not None:
                    if filename == "genesHuman.fna" and countHuman < limit:
                        self.sequences.append(''.join(seq))  # on stocke "l'ancienne séquence" (du header précédent)
                        seq = []
                        self.familles.append("0")
                        countHuman += 1

                    elif filename == "genesMosquito.fna" and countMosquito < limit:
                        self.sequences.append(''.join(seq))  # on stocke "l'ancienne séquence" (du header précédent)
                        seq = []
                        self.familles.append("2")
                        countMosquito += 1

                    elif filename == "genesPig.fna" and countPig < limit:
                        self.sequences.append(''.join(seq))  # on stocke "l'ancienne séquence" (du header précédent)
                        seq = []
                        self.familles.append("1")
                        countPig += 1

                    elif countPig >= limit and countHuman >= limit and countMosquito >= limit:
                        break

                else:
                    seq.append(line.replace("\n", ""))

            if countPig < limit and countHuman < limit and countMosquito < limit:  # utile que si on va jusqu'au bout du fichier
                self.sequences.append(''.join(seq))  # on stocke "l'ancienne séquence" (du header précédent)

    def get_sequence_Human_Pig_Mosquito(self,limit):
        files = ["genesHuman.fna", "genesPig.fna", 'genesMosquito.fna']
        for file in files:
            self.read_fast_file_all("genes/fasta_files/", file, limit)
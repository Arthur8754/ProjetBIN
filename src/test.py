import re
import os

filepath = "genes/fasta_files/genesHuman.fna"
header_pattern = r">lcl*"
sequences = []
with open(filepath) as file:
    seq = []  # séquence courante
    for line in file:
        match = re.match(header_pattern, line)
        if match is not None:
            sequences.aqppend(''.join(seq))  # on stocke "l'ancienne séquence" (du header précédent)
            seq = []
        else:
            seq.append(line.replace("\n", ""))
    sequences.append(''.join(seq))  # on stocke "l'ancienne séquence" (du header précédent)
print(sequences)
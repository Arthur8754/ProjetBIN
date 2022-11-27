"""
Source : https://github.com/david-schaller/AsymmeTree/wiki/Manual

Dans ce code, on commence par construire un arbre phylogénétique des espèces, qui simule une évolution des espèces. Chaque espèce dans l'arbre possède un certain nombre de gènes (supposons, 20 gènes par espèce).

Puis, pour chacune des espèces, on va chercher à construire son génome. Pour ce faire, on va supposer que chaque espèce possède un certain nombre de familles de gènes 
(une famille de gènes est un ensemble de gènes codant la même chose (ou presque la même chose)), et on va générer un arbre par famille, qui va retracer l'évolution de la famille au cours du temps.

Enfin, on va générer le génome de chacune des espèces, en générant des séquences.

À la fin, on a alors :
--> le génome de chacune des espèces (dans "genome/fasta_files")
--> les arbres des familles de gènes (dans "genome/true_gene_trees")
--> l'alignement des familles de gènes (dans "genome"/alignements")

À quoi ça va nous servir dans nos algos ?
Nous, on va prendre les fichiers fasta. Dans ces fichiers, on sait déjà à quelles familles sont associées chacune des séquences (on connaît les clusters). On
appliquera alors les algos sur les séquences des fichiers fasta, et on vérifiera que les algos ont bien regroupé les séquences dans les bonnes familles.

Ici, on a fait dans le sens connaissance clusters => séquences. Dans les algos, on va dans l'autre sens.
"""

import asymmetree.treeevolve as te
import asymmetree.seqevolve as se
import asymmetree.genome as g
import os,shutil
from asymmetree.visualize.TreeVis import visualize

class simulateGene:

    def __init__(self,folder_dest,n_species,n_families):
        self.folder_dest = folder_dest #là où seront stockés les gènes
        self.n_species = n_species
        self.n_families = n_families

    def generate_genes(self):
        if os.path.exists(self.folder_dest):
            shutil.rmtree(self.folder_dest)

        # 1 : CONSTRUCTION DE L'ARBRE PHYLOGÉNÉTIQUE DES ESPÈCES :
        # n=10 espèces actuellement vivantes (nombre de feuilles) à l'âge où on parle. L'arbre simule age = 2 millions d'années. Le modèle d'évolution est Yule
        species_tree = te.species_tree_n_age(n=self.n_species,age=2,model='yule')
        #visualize(species_tree, save_as='../figures/real_tree.png')

        # 2 : CONSTRUCTION DU GÉNOME DE CHACUNE DES ESPÈCES
        gs = g.GenomeSimulator(species_tree,outdir='genes')
        gs.simulate_gene_trees(n=self.n_families,dupl_rate=1,loss_rate=0.5)

        # 3 : GÉNÉRATION DES SÉQUENCES À PARTIR DES ARBRES DES GÈNES
        subst_model = se.SubstModel(model_type="n",model_name="JC69") #construction d'un modèle Markovien modélisant les changements de la séquence au cours du temps (n pour nucléotides, JC69 est un modèle). --> Ici, on modélise la substitution  (mutation) d'un nucléotide
        indel_model = se.IndelModel(insertion_rate=0.01, deletion_rate=0.01) #modélisation d'insertion ou délétion de nucléotides
        gs.simulate_sequences(subst_model=subst_model,indel_model=indel_model)
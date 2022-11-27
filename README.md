# BIN702 - notes d'utilisation

## Environnement virtuel :
Afin d'éviter tout conflit de versions, un environnement virtuel a été créé. Ci-dessous sont présentées les explications pour le lancer et le configurer.

### Créer l'environnement virtuel :
Depuis la racine du dépôt, saisir la commande :

````
python3 -m venv venv
````

### Lancement de l'environnement virtuel :
Les commandes à entrer selon le système d'exploitation sont mentionnées ici : https://docs.python.org/fr/3/library/venv.html
Cependant, on distingue 2 grands cas :

#### Windows :
Depuis la racine du dépôt, entrer la commande :

````
venv\Scripts\activate.bat (Terminal Windows)
````

````
venv\Scripts\activate.ps1 (PowerShell)
````

#### Linux :
Depuis la racine du dépôt, entrer la commande :

````
source venv/bin/activate
````

### Installation des librairies nécessaires de l'environnement virtuel :
Pré-requis : avoir l'environnement virtuel activé.
Pour installer les librairies nécessaires à l'exécution du code, taper, depuis la racine du dépôt, la commande :

````
pip install -r requirements.txt
````

Si, au cours du développement, une nouvelle librairie doit être installée, il suffit d'ajouter le nom de cette librairie dans le fichier ```requirements.txt```, et de réexécuter la commande précédente.

### Quitter l'environnement virtuel :
Entrer simplement la commande : 

````
deactivate
````

## Lancer les scripts :

Il suffit de lancer le programme ```main.py``` depuis le dossier ```src```:
````
python3 main.py
````
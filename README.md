# derivateurMorphoSyntaxique
Générateur de mots à partir de dérivations morphosyntaxiques en utilisant le réseau  [JeuxDeMots](http://www.jeuxdemots.org/jdm-accueil.php)


## Description

* Le programme commence par generer des mots a partir du fichier `ReglesDerivation.txt`.

* Ensuite il génère les mots relies avec le mot d'origine par une relation existante sur [JeuxDeMots](http://www.jeuxdemots.org/jdm-accueil.php) (r_agent, r_lieu; adj->adv, r_pos, etc).

* Il garde l'intersection des deux ensembles et vérifie si la nature des mots gardes est correcte.

* Il retourne l'ensemble obtenu apres cette verification.

## Prérequis

* La version python utilisée est python 3. Pour vérifier la version python installer sur votre machine : 
```
python --version
```
* Installer la version 3 : 

```
pip install python3.8
```

## Fichiers

* Le fichier `derivateur.py` contient le code qui génère des termes a partir du mot entre au debut du programme et vérifie si ces termes existent en accedant a JeuDeMot et retourne les mots correctement dérivés a la fin.



* Le fichier `ReglesDerivation.txt` contient l'ensemble des règles que nous avons utilisées pour générer les mots. Nous avons fait en sorte que ce fichier soit le plus détaillé possible, mais il demeure malgré cela non exaustif (il existe une infinite de règles de dérivation en francais !).

## Exécution du programme

* Pour lancer le programme, veuillez entrer la commande suivante dans le terminal :
```
python derivateur.py
```
* Une fois le programme lance, le message `veuillez entrer un terme: ` devrait s'afficher sur votre terminal. Vous devrez donc tapez le mot que vous voulez dériver et cliquez sur entrée.

**_Important_** : l'exécution du programme nécessite le fichier `ReglesDerivation.txt`. Il faut que ce dernier soit place dans le même répertoire que le dérivateur.

## Exemple de sortie

* Sur le mot "jardiner", on obtient l'ensemble suivant:

```python
{'jardinage': 'Nom', 'jardinable': 'Adj', 'jardinier': 'Nom', 'jardin': 'Nom'}
```


## Auteurs

* Nihed Bendahman
* Maroua Dorsaf Djelouat



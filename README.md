# Application Dash pour la visualisation des résultats de validation

#### Pour lancer l'application en local il faut tout d'abord cloner le repo puis installer les dependences:
```
git clone https://gitlab-bioinfo.aphp.fr/Seqoia-Diag-Pipelines/dashboard_validation.git
```
```
cd dashboard_validation
```

```
pip install -r requirements.txt
```
#### Afin de communiquer avec S3 la configuration aws doit être spécifiée sous:
```
/home/.aws/credentials
```
PS: Le user "spim-preprod" doit être présent dans le fichier de configuration aws

#### Afin de rendre l'application exécutable il faut entrer la commande suivante:
```
chmod +x app.py
```
#### Lancer l'application:
```
./app.py
```
## Filtres de dashboard

le dashboard utilise des filtres pour affichier les résultats des analyses:


**Afin d'afficher des résultats d'un pipeline il faut sélectionner une catégorie, une version de pipeline,une référence,un environnement et la date de l'analyse.**


Si plusieurs analyses ont été effectué avec la même version de pipeline à la même date, des histogrammes supporposés s'afficheront: Il est conseillé de différencier les analyses par la référence.
![capture!](/captures/1.png "Metrics d'une analyse")


**Afin de comparer les performances des différentes versions de pipeline vous pouvez choisir plusieurs versions qui sont exécutées avec la même référence et sous le même environnement de calcul. La date peut être ignorée dans ce cas**


![capture2!](/captures/2.png "Comparaison pipelines")


**Afin de visulaiser les résultats détaillés de l'outils hap.py Navigeur à la page détails et appliquer les filtres :**


![capture3!](/captures/3.png "details")

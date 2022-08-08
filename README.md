#Application Dash pour la visualisation des résultats de validation
Pour lancer l'application en local il faut tout d'abord cloner le repo puis installer les dependences:
```
pip install -r requirements.txt
```
Afin de communiquer avec S3 la configuration aws doit être spécifiée sous:
```
/home/.aws/credentials
```
PS: Le user "spim-dev" doit être présent dans le fichier de configuration aws

Afin de rendre l'application exécutable il faut entrer la commande suivante:
```
chmod +x app.py
```
Lancer l'application:
```
./app.py
```


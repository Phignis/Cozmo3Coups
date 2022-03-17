# Cozmo fait les 3 coups

## Matériel nécessaire, dépendances
>
> *   Hardware :
>     -   1 cozmo (chargé au préalable, sinon ralentissement très genant des animations)
>     -   1 téléphone (iOS / Android)
>     -   3 lightcubes cozmo avec motifs différents (chargés!)
>     -   1 cable USB pour relier votre téléphone à votre ordinateur
> *   Software : 
>     -   Python 3.5.1 minimum
>     -   l'application Android/iOS Cozmo
>     -   ADB (si téléphone Android)
>        
> *   Dépendances Python :
>     -   cozmo : ```pip3 install --user cozmo[camera]``` [plus de détails ici](http://cozmosdk.anki.com/docs/initial.html)
>     -   *optionnel* PyGObject (gtk3) : [procédure d'installation](https://pygobject.readthedocs.io/en/latest/getting_started.html)
>     -   Numpy
>     -   Pillow
>

## Lancer le projet
>
> 1.  Commencer par cloner le repository gitlab : `https://gitlab.iut-clermont.uca.fr/bafoucras/RF-cozmo-fait-les-3-coups.git`
> 2.  Pensez d'abord à mettre en place l'environement spécifié ci-dessus (dépendances, adb...)
> 3.  *   Pour android, mettez votre téléphone en mode développeur (7 appuis sur le numéro de build dans les paramètres)
>     *   Activer le déboguage par USB dans les options développeur
> 4.  Connecter (avec adb au besoin activé sur votre ordinateur) votre téléphone à votre ordinateur. Accepter le deboguage USB sur votre téléphone.
> 5.  Placer Cozmo sur son chargeur pour le démarrer
> 6.  Connectez votre téléphone au wifi du cozmo (secouer le bras du cozmo deux fois pour obtenir le code wifi) Attention au changement automatique de wifi
> 7.  Lancer l'application cozmo et connectez vous
> 8.  Démarrer le mode sdk (paramètres, activer le sdk)
> 9.  Lancer l'application (supposé depuis la racine du projet cloné)
>     *   avec gtk: ./Cozmo3Coups/src/Gtk_start.py
>     *   sans gtk: ./Cozmo3Coups/src/main.py
>

## Problèmes possibles
> *   Le robot cozmo 057D06 semble avoir tendance à fonctionner moins bien (crashs) que le robot 017912
> *   Si jamais vous ne voyez pas le message "Accepter le deboguage USB" lorsque vous connecter votre téléphone à l'ordinateur, assurez vous que adb est bien lancé (commande abd start-server). Lorsque vous faites adb-devices, vous devriez avoir l'identifiant de votre téléphone, en mode device pour attached.
> *   Le robot peut éteindre son écran tout à coup tout en continuant son mouvement, et sans continuer l'éxecution du programme. Cela signifie qu'il a planté. Empecher le de tomber, une fois arrêter reposer le sur son chargeur et retenter le programme après un certain temps.
> *   Si jamais vous avez des messages tel que PyGObject is not installed, gi is not installed, vous n'avez peut etre pas installer PyGObect, lancez le sans gtk 
>

## Contexte du projet
>
> Projet du module "Réalité Virtuelle" de la troisième période de 2eme année de DUT Informatique.
>
> Projet visant a créer une petite application pour Cozmo, pour le faire jouer au pierre-feuille-ciseaux avec vous.
>

## Présentation Commerciale du projet
>
> Cozmo a envie de jouer avec vous!
> Dites lui le nombre de manches de chaques parties, et essayez de prédire ce qu'il va jouer!
> 
>

## Présentation technique du projet
>
> 
>

## Membres du projet
> 
> Baptiste FOUCRAS
>
> Martin ROUAULT
>

## Technologies utilisées
>
> Python 3.7, Cozmo ainsi que son SDK Python
>

## Période du projet
>
> 26 janvier 2022 au 03 avril 2022
>

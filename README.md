# Projet Django

## Objectif
Le but de ce projet est de créer un site dans le style de Doctolib : 
- [x] authentification, pour deux types de profils : patient et praticien
- [x] prise de rendez vous, avec proposition de créneaux libres
- [] sélection de praticiens par zone géographique (optionnel)
- [] backoffice pour les praticiens :
    - [x] ajout de billets décrivant leurs différentes prestations
    - [x] interface de facturation
    - [] gestion de son agenda
    - [x] rédaction de page de présentation
- [] page d'accueil des patients :
    - [x] rappel des prochains rendez-vous
    - [] reprendre un rendez-vous avec un praticien déjà consulté
    - [x] chat/forum

Le site doit être fait avec du Django simple (pas d'API REST, pas de front avec framework type react ou angular), ignorer cette contrainte conduira à un zero automatiquement.

## Commande Django
Lancer serveur
````
python3 manage.py runserver
````

Appliquer les models / Create migration
```
python3 manage.py makemigrations {polls}
```

Voir la migration
```
python3 manage.py sqlmigrate {polls} {0001}
```

Appliquer la migration / Update DB
```
python3 manage.py migrate
```

Shell Pyhton
```
python3 manage.py shell
```

## Create admin
````
python3 manage.py createsuperuser
````



## Model DB
- Patient
- Praticien
- RendezVous
- Facture
- Prestation

## App
- BackOffice Praticien
- Chat
- PRINCIPAL ??

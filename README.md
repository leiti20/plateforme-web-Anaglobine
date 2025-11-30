Anaglobine est une plateforme web moderne permettant la gestion complète des analyses médicales : prise de rendez-vous, consultation des résultats, gestion des laboratoires, paiement en ligne et assistance via IA.
Elle propose une solution simple et intuitive destinée aux patients, laboratoires, réceptionnistes et administrateurs.

##Acteurs du Projet

###Visiteur	
- Consulter les informations sur les laboratoires et les analyses disponibles.
- Naviguer sur la plateforme sans inscription.
- Commencer le processus de prise de rendez-vous (inscription obligatoire pour finaliser).
### Patient	
- Créer et gérer son compte personnel.
- Prendre des rendez-vous selon la disponibilité des laboratoires.
- Consulter et télécharger ses résultats d’analyses.
- Recevoir des explications via l’IA et des notifications.
- Payer en ligne ou en laboratoire.
 ###Laboratoire	
- Gérer les comptes professionnels.
- Publier les résultats d’analyses.
- Gérer les types d’analyses disponibles.
- Suivre l’historique des rendez-vous.
 ###Réceptionniste	
- Assister les patients pour la prise de rendez-vous.
- Mettre à jour les disponibilités des laboratoires.
- Envoyer des notifications aux patients.
### Administrateur		
- Gérer tous les comptes utilisateurs et laboratoires.
- Superviser la plateforme.
- Configurer les paramètres techniques et l’IA.
	
Lancer le Projet en Local	
 ###Prérequis
- Python 3.8+
- Django
- pip
- Git
- MySQL (ex : WampServer / XAMPP)

### Étapes	
1.Cloner le projet :	
```bash
git clone https://github.com/leiti20/plateforme-web-Anaglobine.git	
cd plateforme-web-Anaglobine	
````
2.Créer et activer un environnement virtuel :
```bash	
python -m venv env	
env\Scripts\activate   # Windows		
# ou pour Linux/Mac: source env/bin/activate	
````	
3.Installer les dépendances :
```bash
pip install -r requirements.txt	
````	
4.Configurer la base de données dans settings.py
```bash
DATABASES = {	
    'default': {	
        'ENGINE': 'django.db.backends.mysql',	
        'NAME': 'anaglobine',	
        'USER': 'root',	
        'PASSWORD': '',		
        'HOST': 'localhost',	
        'PORT': '3306',	
    }	
}	
````	
5.Appliquer les migrations :
```bash	
python manage.py makemigrations	
python manage.py migrate	
````	
6.Lancer le serveur :
```bash	
python manage.py runserver	
````	
7. Accéder à l’application : http://127.0.0.1:8000
	


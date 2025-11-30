from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import check_password, make_password
import base64

class Administrateur(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    mot_de_passe = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nom or self.email

    def check_password(self, password):
        return check_password(password, self.mot_de_passe)


class Laboratoire(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nom

class Patient(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, default='Inconnu')
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)
    telephone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'anaglobine_patient'  # Personnaliser le nom de la table

    def __str__(self):
        return f"{self.nom} ({self.email})"  # Une seule définition de __str__

    def check_password(self, password):
        """Vérifie si le mot de passe correspond au mot de passe hashé."""
        return check_password(password, self.mot_de_passe)
    
    def set_password(self, password):
        """Hash le mot de passe et le sauvegarde dans la base de données."""
        self.mot_de_passe = make_password(password)
        self.save()

class Receptionniste(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mot_de_passe = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    laboratoire = models.ForeignKey(Laboratoire, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nom or f"Receptionniste {self.id}"
        
class TypeAnalyse(models.Model):
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.nom

class AnalyseLaboratoire(models.Model):
    laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE, related_name='analyses_disponibles')
    type_analyse = models.ForeignKey(TypeAnalyse, on_delete=models.CASCADE, related_name='laboratoires_disponibles')
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('laboratoire', 'type_analyse')

    def __str__(self):
        return f"{self.laboratoire.nom} - {self.type_analyse.nom} : {self.prix} DA"

class CreneauDisponible(models.Model):
    laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE, related_name='creneaux')
    type_analyse = models.ForeignKey(TypeAnalyse, on_delete=models.CASCADE, related_name='creneaux')
    date = models.DateField()  # Remplacer jour_semaine par date
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    est_reserve = models.BooleanField(default=False)

    class Meta:
        unique_together = ('laboratoire', 'type_analyse', 'date', 'heure_debut', 'heure_fin')

    def __str__(self):
        return f"{self.laboratoire.nom} - {self.type_analyse.nom} - {self.date} ({self.heure_debut} à {self.heure_fin})"

class Rendezvous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, related_name='rendezvous')
    laboratoire = models.ForeignKey(Laboratoire, on_delete=models.SET_NULL, null=True)
    type_analyse = models.ForeignKey(TypeAnalyse, on_delete=models.SET_NULL, null=True)
    creneau = models.ForeignKey(CreneauDisponible, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=10, choices=[('en_cours', 'En cours'), ('termine', 'Terminé')], default='en_cours')
    
    def __str__(self):
        return f"Rendez-vous {self.id} - {self.patient} - {self.laboratoire}- Creneau ID: {self.creneau.id if self.creneau else 'N/A'}"

class Paiement(models.Model):
    MOYENS_CHOICES = [
        ('especes', 'Espèces'),
        ('carte', 'Carte'),
        ('en_ligne', 'En ligne'),
    ]
    STATUT_CHOICES = [
        ('paye', 'Payé'),
        ('en_attente', 'En attente'),
        ('echoue', 'Échoué'),
    ]
    rendezvous = models.OneToOneField(Rendezvous, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    moyen_paiement = models.CharField(max_length=20, choices=MOYENS_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_paiement = models.DateTimeField(auto_now_add=True)
    name_on_card = models.CharField(max_length=100, blank=True, null=True)
    credit_card_number = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
       return f"Paiement {self.id} pour {self.rendezvous.patient}"
    

class ResultatAnalyse(models.Model):
    rendezvous = models.OneToOneField('Rendezvous', on_delete=models.CASCADE)
    fichier_pdf = models.BinaryField() # Utiliser BinaryField pour stocker les fichiers binaires (PDF)
    date_depot = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    laboratoire = models.ForeignKey('Laboratoire', on_delete=models.CASCADE)
    
    def get_fichier_pdf_base64(self):
        if self.fichier_pdf:
            return base64.b64encode(self.fichier_pdf).decode('utf-8')
        return ""

    class Meta:
        unique_together = ('rendezvous',)  # Assurer que chaque rendez-vous a un seul résultat

    def __str__(self):
        return f"Résultat d'analyse pour le rendez-vous {self.rendezvous.id} - Patient {self.patient.id}"
        
        
class Notification(models.Model):
    STATUT_CHOICES = [
        ('envoye', 'Envoyé'),
        ('lu', 'Lu'),
        ('non_lu', 'Non lu'),
    ]
    
    message = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='non_lu')
    date_envoi = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f"Notification pour {self.patient.nom} - {self.statut}"
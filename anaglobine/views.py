from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Prefetch
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Patient, Administrateur, Receptionniste , Laboratoire, TypeAnalyse , AnalyseLaboratoire , ResultatAnalyse, CreneauDisponible , Paiement, Rendezvous, Notification
from django.contrib.auth.hashers import check_password, make_password
from functools import wraps
from django.core.mail import send_mail , BadHeaderError
from django.conf import settings
from django.http import JsonResponse
from datetime import date ,datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import PaiementForm
from django.utils import timezone
from django.utils.translation import gettext as _

# la vue de page d'acceuil
def index(request):
    return render(request, 'anaglobine/index.html')

# partie de contacter 
def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if nom and email and message:
            subject = f"Nouveau message de {nom}"
            message_body = f"Nom: {nom}\nEmail: {email}\n\nMessage:\n{message}"
            try:
                send_mail(
                    subject,
                    message_body,
                    email,
                    ['glprojectanaglobine@gmail.com'],
                    fail_silently=False,
                )
                print("Redirection vers:", request.path + '?sent=1')
                return redirect(request.path + '?sent=1')  
            except BadHeaderError:
                messages.error(request, 'En-tête invalide.')
            except Exception as e:
                messages.error(request, f"Erreur lors de l'envoi : {e}")
        else:
            messages.error(request, "Veuillez remplir tous les champs.")
    
    return render(request, 'anaglobine/index.html')

# la vue des laboratoires
def laboratoire_view(request):
    return render(request, 'anaglobine/laboratoire.html')
    
# vue de laboratoire LaboMoualek
def LaboMoualek_view(request):
    labo = get_object_or_404(Laboratoire, id=1)  
    analyses = AnalyseLaboratoire.objects.filter(laboratoire=labo).select_related('type_analyse')
    context = {
        'labo': labo,
        'analyses': analyses  
    }
    return render(request, 'anaglobine/LaboMoualek.html', context)

# vue de laboratoire LabBouras
def LabBouras_view(request):
    labo = get_object_or_404(Laboratoire, id=2)
    analyses = AnalyseLaboratoire.objects.filter(laboratoire=labo).select_related('type_analyse')
    context = {
        'labo': labo,
        'analyses': analyses
    }
    return render(request, 'anaglobine/LabBouras.html', context)

# vue de laboratoire LaboKhellilAmrane
def LaboKhellilAmrane_view(request):
    labo = get_object_or_404(Laboratoire, id=3)  
    analyses = AnalyseLaboratoire.objects.filter(laboratoire=labo).select_related('type_analyse')
    context = {
        'labo': labo,
        'analyses': analyses
    }
    return render(request, 'anaglobine/LaboKhellilAmrane.html', context)

# vue de laboratoire LaboLalaoui
def LaboLalaoui_view(request):
    labo = get_object_or_404(Laboratoire, id=4)  
    analyses = AnalyseLaboratoire.objects.filter(laboratoire=labo).select_related('type_analyse')
    context = {
        'labo': labo,
        'analyses': analyses
    }
    return render(request, 'anaglobine/LaboLalaoui.html', context)

# vue de laboratoire LaboHocineSklab
def LaboHocineSklab_view(request):
    labo = get_object_or_404(Laboratoire, id=5)  
    analyses = AnalyseLaboratoire.objects.filter(laboratoire=labo).select_related('type_analyse')
    context = {
        'labo': labo,
        'analyses': analyses
    }
    return render(request, 'anaglobine/LaboHocineSklab.html', context)

# vue de laboratoire LaboKebbiche
def LaboKebbiche_view(request):
    labo = get_object_or_404(Laboratoire, id=6)  
    analyses = AnalyseLaboratoire.objects.filter(laboratoire=labo).select_related('type_analyse')
    context = {
        'labo': labo,
        'analyses': analyses
    }
    return render(request, 'anaglobine/LaboKebbiche.html', context)

# Vue pour la connexion et l'inscription des utilisateurs
def login_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        # INSCRIPTION D'UN PATIENT
        if action == 'register':
            # Récupérer les informations du formulaire
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            age = request.POST.get('age')
            email = request.POST.get('email')
            mot_de_passe = request.POST.get('password')
            telephone = request.POST.get('telephone')

            # Vérifier si l'email est déjà utilisé
            if Patient.objects.filter(email=email).exists():
                messages.error(request, _("Un patient avec cet email existe déjà."))
                return redirect('login')

            # Création du patient
            patient = Patient.objects.create(
                nom=nom,
                prenom=prenom,
                age=age,
                email=email,
                mot_de_passe=make_password(mot_de_passe),
                telephone=telephone,
            )
            request.session['user_id'] = patient.id
            request.session['user_type'] = 'patient'
            messages.success(request, _("Inscription réussie."))

            # Envoi de l'email de bienvenue
            subject = "Bienvenue sur Anaglobine"
            message = f"Bonjour {patient.prenom},\n\nBienvenue sur Anaglobine ! Nous sommes ravis de vous avoir parmi nous.\n\nVotre inscription a été réussie.\n\nL'équipe Anaglobine."

            from_email = settings.DEFAULT_FROM_EMAIL

            send_mail(subject, message, from_email, [patient.email])

            return redirect('patient')

        # CONNEXION D'UN UTILISATEUR
        elif action == 'login':
            email = request.POST.get('email')
            mot_de_passe = request.POST.get('password')

            # Vérifier si c'est un patient
            try:
                patient = Patient.objects.get(email=email)
                if check_password(mot_de_passe, patient.mot_de_passe):
                    request.session['user_id'] = patient.id
                    request.session['user_type'] = 'patient'
                    next_url = request.GET.get('next', 'patient')  # Rediriger vers 'patient' si aucun 'next' n'est défini
                    return redirect(next_url)
            except Patient.DoesNotExist:
                pass

            # Vérifier si c'est un administrateur
            try:
                admin = Administrateur.objects.get(email=email)
                if check_password(mot_de_passe, admin.mot_de_passe):
                    request.session['user_id'] = admin.id
                    request.session['user_type'] = 'admin'
                    return redirect('adminag')  # page admin
            except Administrateur.DoesNotExist:
                pass

            # Vérifier si c'est un réceptionniste
            try:
                receptionniste = Receptionniste.objects.get(email=email)
                if check_password(mot_de_passe, receptionniste.mot_de_passe):
                    request.session['user_id'] = receptionniste.id
                    request.session['user_type'] = 'receptionniste'
                    return redirect('receptionniste')  # page réceptionniste
            except Receptionniste.DoesNotExist:
                pass

            # Si aucune correspondance
            messages.error(request, _("Email ou mot de passe incorrect."))
            return redirect('login')

    return render(request, 'anaglobine/login.html')

# vue pour se deconnecter
def logout_view(request):
    request.session.flush()
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('login')

# les sessions 
def login_required(role=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Vérification de l'authentification de l'utilisateur
            if not request.session.get('user_id'):
                return redirect('login')  # Rediriger vers la page de login si l'utilisateur n'est pas connecté

            # Vérification du rôle (si un rôle est spécifié dans le décorateur)
            if role:
                # Vérifier si le rôle de l'utilisateur dans la session correspond au rôle requis
                if request.session.get('user_type') != role:
                    return redirect('login')  # Rediriger vers la page de login ou une autre page selon le rôle

            # Si tout va bien, appeler la vue demandée
            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator

# vue patient
def patient_view(request):
    if request.session.get('user_type') != 'patient':
        return redirect('login')

    try:
        patient = Patient.objects.get(id=request.session.get('user_id'))
    except Patient.DoesNotExist:
        messages.error(request, "Patient introuvable.")
        return redirect('login')

    if request.method == 'POST':
        patient.nom = request.POST.get('nom')
        patient.prenom = request.POST.get('prenom')
        patient.age = request.POST.get('age')
        patient.telephone = request.POST.get('telephone')
        patient.save()
        messages.success(request, "Vos informations ont été mises à jour avec succès.")
        return redirect('patient')

    historique = Rendezvous.objects.filter(patient=patient).order_by('-creneau__date')

    # Associer chaque rdv à son résultat (avec PDF non vide seulement)
    resultats_dict = {
        r.rendezvous_id: r
        for r in ResultatAnalyse.objects.filter(
            rendezvous__in=historique
        ).exclude(fichier_pdf__isnull=True)
        if r.fichier_pdf  # S'assurer qu'il n'est pas vide
    }

    return render(request, 'anaglobine/patient.html', {
        'patient': patient,
        'historique': historique,
        'resultats': resultats_dict,
    })


# vue de l'admin
def adminag_view(request):  
    if request.method == "POST":  # Si la méthode est POST, on traite la modification
        original_email = request.POST.get("originalEmail")  # Email original
        new_email = request.POST.get("modifierEmail")       # Nouvel email
        role = request.POST.get("modifierRole")
        nom = request.POST.get("modifierNom")
        prenom = request.POST.get("modifierPrenom") or ''   # Valeur par défaut

        try:
            # Recherche par email ORIGINAL selon le rôle
            if role == "Patient":
                compte = get_object_or_404(Patient, email=original_email)
                compte.email = new_email  # Mise à jour du nouvel email
                compte.prenom = prenom
            elif role == "Réceptionniste":
                compte = get_object_or_404(Receptionniste, email=original_email)
                compte.email = new_email
            elif role == "Administrateur":
                compte = get_object_or_404(Administrateur, email=original_email)
                compte.email = new_email

            # Mise à jour commune à tous les rôles
            compte.nom = nom
            compte.save()

            messages.success(request, f"Compte {role} mis à jour avec succès!")
            return redirect('adminag')

        except Exception as e:
            messages.error(request, f"Erreur de modification : {str(e)}")
            return redirect('adminag')

    else:  # Si la méthode n'est pas POST, on affiche les informations
        search_query = request.GET.get('search', '')  # Recherche de la requête
        comptes = []

        # Filtrer les comptes selon la recherche
        if search_query:
            # Recherche pour chaque modèle spécifique en fonction du rôle
            patients = Patient.objects.filter(
                Q(nom__icontains=search_query) | Q(email__icontains=search_query)
            )
            receptionnistes = Receptionniste.objects.filter(
                Q(nom__icontains=search_query) | Q(email__icontains=search_query)
            )
            administrateurs = Administrateur.objects.filter(
                Q(nom__icontains=search_query) | Q(email__icontains=search_query)
            )
        else:
            # Si aucune recherche, on prend tous les comptes
            patients = Patient.objects.all()
            receptionnistes = Receptionniste.objects.all()
            administrateurs = Administrateur.objects.all()

        # Ajouter les patients dans la liste des comptes
        for p in patients:
            comptes.append({
                'nom': p.nom,
                'prenom': p.prenom,
                'email': p.email,
                'role': 'Patient',
            })

        # Ajouter les réceptionnistes dans la liste des comptes
        for r in receptionnistes:
            comptes.append({
                'nom': r.nom,
                'prenom': '',  # Pas de champ prénom
                'email': r.email,
                'role': 'Réceptionniste',
            })

        # Ajouter les administrateurs dans la liste des comptes
        for a in administrateurs:
            comptes.append({
                'nom': a.nom,
                'prenom': '',  # Pas de champ prénom
                'email': a.email,
                'role': 'Administrateur',
            })

        # Compter le nombre de patients et de réceptionnistes
        nb_patients = Patient.objects.count()
        nb_receptionniste = Receptionniste.objects.count()

        # Rendre le template avec les données
        return render(request, 'anaglobine/adminag.html', {
            'comptes': comptes,
            'nb_patients': nb_patients,
            'nb_receptionniste': nb_receptionniste,
        })

# Supprimer un compte 
def supprimer_compte(request, role, email):
    try:
        if role == "Patient":
            compte = get_object_or_404(Patient, email=email)
        elif role == "Réceptionniste":
            compte = get_object_or_404(Receptionniste, email=email)
        elif role == "Administrateur":
            compte = get_object_or_404(Administrateur, email=email)
        else:
            messages.error(request, "Rôle inconnu.")
            return redirect('adminag')

        compte.delete()
        messages.success(request, f"Le compte {role} ({email}) a été supprimé avec succès.")
    except Exception as e:
        messages.error(request, f"Erreur lors de la suppression : {str(e)}")

    return redirect('adminag')
# vue receptionniste
def receptionniste_view(request):
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    if user_type != 'receptionniste':
        return redirect('login')

    # Récupération du réceptionniste et de ses informations
    receptionniste = Receptionniste.objects.get(id=user_id)
    laboratoire_id = receptionniste.laboratoire_id
    types_analyse = TypeAnalyse.objects.all()

    # GESTION DU TÉLÉVERSEMENT DE PDF POUR UN RÉSULTAT
    if request.method == 'POST' and 'fichier_pdf' in request.FILES:
        resultat_id = request.POST.get('resultat_id')
        fichier_pdf = request.FILES['fichier_pdf'].read()

        try:
            resultat = ResultatAnalyse.objects.get(id=resultat_id)
            resultat.fichier_pdf = fichier_pdf
            resultat.save()
            messages.success(request, "PDF mis à jour avec succès.")
        except ResultatAnalyse.DoesNotExist:
            messages.error(request, "Résultat introuvable.")
        return redirect('receptionniste')

    # AJOUT CRENEAU
    if 'ajouter_creneau' in request.POST:
        date = request.POST.get('dateCreneau')
        heure_debut = request.POST.get('heureDebutCreneau')
        heure_fin = request.POST.get('heureFinCreneau')
        type_analyse_id = request.POST.get('typeAnalyse')
        try:
            type_analyse = TypeAnalyse.objects.get(id=type_analyse_id)

            # Vérification d'un créneau déjà existant
            existe = CreneauDisponible.objects.filter(
                laboratoire_id=laboratoire_id,
                date=date,
                heure_debut=heure_debut,
                heure_fin=heure_fin
            ).exists()

            if existe:
                messages.error(request, "Un créneau avec les mêmes date et horaires existe déjà pour ce laboratoire.")
            else:
                CreneauDisponible.objects.create(
                    laboratoire_id=laboratoire_id,
                    type_analyse=type_analyse,
                    date=date,
                    heure_debut=heure_debut,
                    heure_fin=heure_fin
                )
                messages.success(request, "Créneau ajouté avec succès.")
        except TypeAnalyse.DoesNotExist:
            messages.error(request, "Type d'analyse invalide.")
        return redirect('receptionniste')

    # MODIFIER CRENEAU
    if 'modifier_creneau' in request.POST:
        creneau_id = request.POST.get('creneauId')
        date = request.POST.get('dateCreneau')
        heure_debut = request.POST.get('heureDebutCreneau')
        heure_fin = request.POST.get('heureFinCreneau')
        type_analyse_id = request.POST.get('typeAnalyse')

        try:
            creneau = CreneauDisponible.objects.get(id=creneau_id)
            if creneau.est_reserve:
                messages.error(request, "Impossible de modifier un créneau déjà réservé.")
            else:
                type_analyse = TypeAnalyse.objects.get(id=type_analyse_id)
                creneau.date = date
                creneau.heure_debut = heure_debut
                creneau.heure_fin = heure_fin
                creneau.type_analyse = type_analyse
                creneau.save()
                messages.success(request, "Créneau modifié avec succès.")
        except (CreneauDisponible.DoesNotExist, TypeAnalyse.DoesNotExist):
            messages.error(request, "Erreur lors de la modification du créneau.")
        return redirect('receptionniste')

    # SUPPRIMER CRENEAU
    if 'supprimer_creneau' in request.POST:
        creneau_id = request.POST.get('creneauId')
        try:
            creneau = CreneauDisponible.objects.get(id=creneau_id)
            if creneau.est_reserve:
                messages.error(request, "Impossible de supprimer un créneau déjà réservé.")
            else:
                creneau.delete()
                messages.success(request, "Créneau supprimé avec succès.")
        except CreneauDisponible.DoesNotExist:
            messages.error(request, "Créneau introuvable.")
        return redirect('receptionniste')

    # AFFICHAGE DES DONNÉES
    creneaux_reserves = CreneauDisponible.objects.filter(
        laboratoire_id=laboratoire_id, est_reserve=True
    ).select_related('rendezvous')

    rendezvous_reserves = Rendezvous.objects.filter(
        creneau__in=creneaux_reserves
    ).select_related('patient', 'type_analyse', 'creneau')

    patients_info = []
    for rdzv in rendezvous_reserves:
        paiement = Paiement.objects.filter(rendezvous=rdzv).first()
        paiement_statut = paiement.statut if paiement else 'Non payé'
        patients_info.append({
            'nom': rdzv.patient.nom,
            'prenom': rdzv.patient.prenom,
            'date': rdzv.creneau.date.strftime("%d/%m/%Y"),
            'heure_debut': rdzv.creneau.heure_debut.strftime("%H:%M"),
            'heure_fin': rdzv.creneau.heure_fin.strftime("%H:%M"),
            'type_analyse': rdzv.type_analyse.nom,
            'paiement': paiement_statut
        })

    creneaux_disponibles = CreneauDisponible.objects.filter(
        laboratoire_id=laboratoire_id, est_reserve=False
    )

    resultats = ResultatAnalyse.objects.select_related(
        'rendezvous', 'rendezvous__patient', 'rendezvous__type_analyse'
    ).filter(
        rendezvous__creneau__laboratoire_id=laboratoire_id
    )
    
    return render(request, 'anaglobine/receptionniste.html', {
        'receptionniste': receptionniste,
        'types_analyse': types_analyse,
        'patients_info': patients_info,
        'creneaux_disponibles': creneaux_disponibles,
        'resultats': resultats
    })

# Supprimer un crenaux disponible 
def supprimer_creneau(request, creneau_id):
    creneau = get_object_or_404(CreneauDisponible, id=creneau_id)
    creneau.delete()
    return redirect('receptionniste')  # Redirection vers la vue de gestion des créneaux

# Modifier les informations de receptionniste
def modifier_receptionniste(request):
    if request.method == 'POST':
        # Récupération des nouvelles données
        id = request.POST.get('id')
        receptionniste = Receptionniste.objects.get(id=id)

        receptionniste.nom = request.POST.get('modifierNom')
        receptionniste.email = request.POST.get('modifierEmail')
        receptionniste.telephone = request.POST.get('modifierTelephone')
        receptionniste.adresse = request.POST.get('modifierAdresse')

        receptionniste.save()
        messages.success(request, "Les informations ont été modifiées avec succès.")
        return redirect('receptionniste')  # Redirigez vers la vue principale du réceptionniste

    return redirect('receptionniste')  # Si la méthode n'est pas POST, rediriger vers la vue principale

# vue rendez-vous
def rendezvous_view(request):
    type_id = request.GET.get('type')  # ex: "?type=1"
    types_analyse = TypeAnalyse.objects.all()

    if type_id:
        creneaux = CreneauDisponible.objects.filter(type_analyse_id=type_id, est_reserve=False)
    else:
        creneaux = CreneauDisponible.objects.filter(est_reserve=False)

    return render(request, 'anaglobine/rendezvous.html', {
        'types_analyse': types_analyse,
        'creneaux': creneaux
    })


#vue paiement
from .decorators import patient_required 

@patient_required
def paiement_view(request, creneau_id):
    patient_id = request.session.get('user_id')
    patient = get_object_or_404(Patient, id=patient_id)
    creneau = get_object_or_404(CreneauDisponible, id=creneau_id)

    # On récupère le prix de l'analyse dès le début
    analyse_labo = get_object_or_404(
        AnalyseLaboratoire,
        laboratoire=creneau.laboratoire,
        type_analyse=creneau.type_analyse
    )
    montant = analyse_labo.prix

    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            # Créer un rendez-vous
            rendezvous = Rendezvous.objects.create(
                patient=patient,
                laboratoire=creneau.laboratoire,
                type_analyse=creneau.type_analyse,
                creneau=creneau
            )

            # Marquer le créneau comme réservé
            creneau.est_reserve = True
            creneau.save()

            # Récupérer le mode de paiement
            mode_paiement = form.cleaned_data['mode_paiement']

            # Créer un paiement simulé
            statut = 'paye' if mode_paiement == 'en_ligne' else 'en_attente'
            Paiement.objects.create(
                rendezvous=rendezvous,
                montant=montant,
                date_paiement=timezone.now(),
                statut=statut
            )

            # Créer un résultat vide
            ResultatAnalyse.objects.create(
                rendezvous=rendezvous,
                fichier_pdf=None,
                patient=patient,
                laboratoire=creneau.laboratoire
            )

            # Ajouter un message de succès
            messages.success(request, "Votre paiement a été simulé avec succès.")
            
            # Combine la date et l'heure dans un datetime pour formater proprement
            datetime_rdv = datetime.combine(creneau.date, creneau.heure_debut)
            
            # Envoi de l'email de confirmation du rendez-vous
            subject = "Confirmation de votre rendez-vous Anaglobine"
            message = f"Bonjour {patient.prenom},\n\n" \
                      f"Nous avons bien reçu votre paiement et votre rendez-vous avec le laboratoire {creneau.laboratoire.nom} pour l'analyse {creneau.type_analyse.nom} est confirmé.\n\n" \
                      f"Date du rendez-vous : {datetime_rdv.strftime('%d/%m/%Y %H:%M')}\n\n" \
                      f"Merci de votre confiance.\n\nL'équipe Anaglobine."
            from_email = settings.DEFAULT_FROM_EMAIL

            send_mail(subject, message, from_email, [patient.email])

            # Rediriger vers la page du patient
            return redirect('patient')
        else:
            error_message = "Le paiement n'a pas pu être effectué. Veuillez réessayer."

    else:
        form = PaiementForm()

    return render(request, 'anaglobine/paiement.html', {
        'form': form,
        'patient': patient,
        'creneau': creneau,
        'montant': montant,
        'error_message': locals().get('error_message')
    })
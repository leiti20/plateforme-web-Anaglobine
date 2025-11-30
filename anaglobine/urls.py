from django.urls import path
from . import views

urlpatterns = [
    #page acceuil
    path('', views.index, name='index'),
    path('index/', views.index),
    path('index/contact', views.contact, name='contact'),

    #page connexion/inscription
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    #page rendez-vous
    path('rendezvous/',views.rendezvous_view, name='rendezvous'),

    #page paiement
    path('paiement/<int:creneau_id>/', views.paiement_view, name='paiement_view'),

    #page admin
    path('adminag/',views.adminag_view, name='adminag'),
    path('supprimer-compte/<str:role>/<str:email>/', views.supprimer_compte, name='supprimer_compte'),
  
    # page patient
    path('patient/', views.patient_view, name='patient'),
    path('logout/', views.logout_view, name='logout'),

    # page receptionniste
    path('receptionniste/', views.receptionniste_view, name='receptionniste'),
    path('supprimer-creneau/<int:creneau_id>/', views.supprimer_creneau, name='supprimer_creneau'),
    path('modifier-receptionniste/', views.modifier_receptionniste, name='modifier_receptionniste'),

    # Pages labo
    path('laboratoire/', views.laboratoire_view, name='laboratoire'),
    path('LabBouras/', views.LabBouras_view, name='LabBouras'),
    path('LaboHocineSklab/', views.LaboHocineSklab_view, name='LaboHocineSklab'),
    path('LaboKebbiche/', views.LaboKebbiche_view, name='LaboKebbiche'),
    path('LaboKhellilAmrane/', views.LaboKhellilAmrane_view, name='LaboKhellilAmrane'),
    path('LaboLalaoui/', views.LaboLalaoui_view, name='LaboLalaoui'),
    path('LaboMoualek/', views.LaboMoualek_view, name='LaboMoualek'),
]

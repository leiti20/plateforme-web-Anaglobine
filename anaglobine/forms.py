from django import forms

class PaiementForm(forms.Form):
    MODE_PAIEMENT_CHOICES = [
        ('en_ligne', 'Paiement en ligne'),
        ('especes', 'Paiement en espèces'),
    ]
    mode_paiement = forms.ChoiceField(
        choices=MODE_PAIEMENT_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="Mode de paiement"
    )

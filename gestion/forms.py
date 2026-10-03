from django import forms
from .models import Client, Facture, Paiement


class ClientForm(forms.ModelForm):

    class Meta:

        model = Client

        fields = "__all__"


class FactureForm(forms.ModelForm):

    class Meta:

        model = Facture

        fields = "__all__"



class PaiementForm(forms.ModelForm):

    class Meta:

        model = Paiement

        fields = "__all__"
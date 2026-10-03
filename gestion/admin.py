from django.contrib import admin
from .models import Client, Facture, Paiement


admin.site.register(Client)
admin.site.register(Facture)
admin.site.register(Paiement)
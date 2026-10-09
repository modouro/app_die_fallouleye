from django.db import models
from datetime import datetime
import re


# ----------------------------
# Client
# ----------------------------
class Client(models.Model):

    code = models.CharField(max_length=20, unique=True, blank=True)
    prenoms = models.CharField(max_length=200)
    nom = models.CharField(max_length=150)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)

  
    def save(self, *args, **kwargs):

        if not self.code:

            dernier_code = (
                Client.objects.order_by('-id').values_list('code', flat=True).first()
            )

            if dernier_code:
                numero = int(dernier_code.split('-')[1]) + 1
            else:
                numero = 1

            self.code = f"CLI-{numero:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.prenoms} {self.nom}"


# ----------------------------
# Facture
# ----------------------------
class Facture(models.Model):

    numero = models.CharField(max_length=50, unique=True, blank=True)

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="factures"
    )

    date_facturation = models.DateField()
    date_echeance = models.DateField()

    designation = models.CharField(max_length=200)

    quantite = models.PositiveIntegerField(default=1)

    prix_unitaire = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # ----------------------------
    # Calcul automatique
    # ----------------------------

    @property
    def total(self):
        return self.quantite * self.prix_unitaire

    @property
    def montant_paye(self):

        total = sum(
            p.montant for p in self.paiements.all()
        )

        return total or 0

    @property
    def reste(self):

        reste = self.total - self.montant_paye

        return reste if reste > 0 else 0

    # ----------------------------
    # SAVE
    # ----------------------------

"""  def save(self, *args, **kwargs):

        if not self.numero:

            dernier = Facture.objects.count() + 1
            annee = datetime.now().year

            self.numero = f"FAC-{annee}-{dernier:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero """

def save(self, *args, **kwargs):

    if not self.numero:

        annee = datetime.now().year
        prefixe = f"FAC-{annee}-"

        # Récupérer tous les numéros de l'année
        numeros = Facture.objects.filter(
            numero__startswith=prefixe
        ).values_list("numero", flat=True)

        dernier_numero = 0

        for numero in numeros:
            match = re.search(r"(\d+)$", numero)

            if match:
                valeur = int(match.group(1))

                if valeur > dernier_numero:
                    dernier_numero = valeur

        # Générer le prochain numéro
        prochain_numero = dernier_numero + 1

        self.numero = f"{prefixe}{prochain_numero:04d}"

        # Sécurité supplémentaire contre un doublon
        while Facture.objects.filter(numero=self.numero).exists():
            prochain_numero += 1
            self.numero = f"{prefixe}{prochain_numero:04d}"

    super().save(*args, **kwargs)


# ----------------------------
# Paiement
# ----------------------------
class Paiement(models.Model):

    facture = models.ForeignKey(
        Facture,
        related_name="paiements",
        on_delete=models.CASCADE
    )

    date = models.DateField()

    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    type_paiement = models.CharField(max_length=50)

    def __str__(self):

        return (
            f"{self.facture.numero} - "
            f"{self.montant} ({self.type_paiement})"
        )
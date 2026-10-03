import os
import warnings
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Facture, Client, Paiement
from django.db.models import Sum, Q
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date
from weasyprint import HTML
from django.http import HttpResponse
import pandas as pd

os.environ["GIO_USE_VFS"] = "local"
os.environ["GTK_DEBUG"] = "none"
warnings.filterwarnings("ignore")

@login_required
def dashboard(request):
    factures = Facture.objects.all()  # récupère toutes les factures
    nb_factures = factures.count()
    ventes = sum(f.total for f in factures)  # total calculé via la propriété
    # 🔥 NOUVEAU : total payé
    total_paye = sum(f.montant_paye for f in factures)

    context = {
        "factures": nb_factures,
        "ventes": ventes,
        "total_paye": total_paye,
    }

    return render(request, "dashboard.html", context)

def is_admin(user):
    return user.is_superuser



def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Vérification mot de passe
        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return redirect("register")

        # Vérification utilisateur existant
        if User.objects.filter(username=username).exists():
            messages.error(request, "Nom d'utilisateur déjà utilisé")
            return redirect("register")

        # Création utilisateur
        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Compte créé avec succès")

        return redirect("login")

    return render(request, "register.html")

@user_passes_test(is_admin)
def factures(request):
    # code de la vue
    pass

@login_required
def clients(request):

    query = request.GET.get("q")

    data = Client.objects.all()

    if query:
        data = Client.objects.filter(
            Q(nom__icontains=query) |
            Q(prenoms__icontains=query)
        )

    return render(request, "clients.html", {"data": data})

@login_required
def client_create(request):
    if request.method == "POST":
        prenoms = request.POST.get("prenoms")
        nom = request.POST.get("nom")
        adresse = request.POST.get("adresse")
        telephone = request.POST.get("telephone")

        # Le code sera généré automatiquement
        Client.objects.create(
            prenoms=prenoms,
            nom=nom,
            adresse=adresse,
            telephone=telephone
        )

    return redirect("clients")  

@login_required
def clients_list(request):
    clients = Client.objects.all()
    return render(request, "clients.html", {"clients": clients})

@login_required
def client_update(request, id):

    client = get_object_or_404(Client, id=id)

    if request.method == "POST":

        client.code = request.POST.get("code")
        client.prenoms = request.POST.get("prenoms")
        client.nom = request.POST.get("nom")
        client.adresse = request.POST.get("adresse")
        client.telephone = request.POST.get("telephone")

        client.save()

    return redirect("clients")

@login_required
def client_delete(request, id):

    client = get_object_or_404(Client, id=id)

    if request.method == "POST":
        client.delete()

    return redirect("clients")

@login_required
def factures(request):
    """ factures = Facture.objects.all().order_by("-id") """
    factures = Facture.objects.all().prefetch_related("paiements").order_by("-id")
    clients = Client.objects.all()

    total_total = sum(f.total for f in factures)
    montant_paye = sum(f.montant_paye for f in factures)
    total_reste = total_total - montant_paye

    # 🔍 Recherche texte
    query = request.GET.get("q")
    if query:
        factures = factures.filter(
            Q(client__nom__icontains=query) |
            Q(client__prenoms__icontains=query)
        )

    # 🔍 Filtre statut
    statut = request.GET.get("statut")
    if statut == "payee":
        factures = [ f for f in factures if f.reste == 0]

    elif statut == "partielle":
        factures = [ f for f in factures if f.reste > 0]
        

    context = {
        "factures": factures,
        "clients": clients,
        "total_total": total_total,
        "montant_paye": montant_paye,
        "total_reste": total_reste
    }

    return render(request, "factures.html", context)

@login_required
def facture_create(request):
    if request.method == "POST":
        client_id = request.POST.get("client")
        date_facturation = request.POST.get("date_facturation")
        date_echeance = request.POST.get("date_echeance")

        designation = request.POST.get("designation")
        quantite = request.POST.get("quantite")
        prix_unitaire = request.POST.get("prix_unitaire")

        client = Client.objects.get(id=client_id)

        if designation and quantite and prix_unitaire:
            facture = Facture.objects.create(
                client=client,
                date_facturation=date_facturation,
                date_echeance=date_echeance,
                designation=designation,
                quantite=int(quantite),
                prix_unitaire=float(prix_unitaire)
            )
        else:
            facture = Facture.objects.create(
                client=client,
                date_facturation=date_facturation,
                date_echeance=date_echeance
            )

        return redirect("factures")

@login_required
def facture_update(request, id):
    if request.method == "POST":
        facture_id = request.POST.get("facture_id")
        facture = Facture.objects.get(id=facture_id)

        facture.client_id = request.POST.get("client")
        facture.date_facturation = request.POST.get("date_facturation")
        facture.date_echeance = request.POST.get("date_echeance")
        facture.designation = request.POST.get("designation")

        # 🔥 Conversion obligatoire
        quantite = request.POST.get("quantite")
        prix = request.POST.get("prix_unitaire")

        facture.quantite = int(quantite) if quantite else 0
        facture.prix_unitaire = float(prix) if prix else 0

        facture.save()

    return redirect("factures")


@login_required
def facture_delete(request, id):
    try:
        facture = Facture.objects.get(id=id)
    except Facture.DoesNotExist:
        return redirect("factures")  # ou message d'erreur

    if request.method == "POST":
        facture.delete()

    return redirect("factures")


@login_required
def paiement_create(request):
    if request.method == "POST":
        facture_id = request.POST.get("facture")
        montant = request.POST.get("montant")
        type_paiement = request.POST.get("type_paiement")

        facture = Facture.objects.get(id=facture_id)

        Paiement.objects.create(
            facture=facture,
            montant=float(montant),
            type_paiement=type_paiement,
            date=date.today()
        )

    return redirect("factures")

""" Export fichier Excel """

@login_required
def export_excel(request):

    factures = Facture.objects.all().values()

    df = pd.DataFrame(factures)

    response = HttpResponse(content_type='application/ms-excel')

    response['Content-Disposition'] = 'attachment; filename="factures.xlsx"'

    df.to_excel(response, index=False)

    return response

""" Export fichier PDF """

@login_required
def facture_pdf(request, id):

    facture = get_object_or_404(Facture, id=id)
    paiements = facture.paiements.all()
    total_paye = sum(p.montant for p in paiements)
    reste = facture.total - total_paye
    """ logo_path = os.path.abspath(os.path.join(settings.STATIC_ROOT, "images/image_fallou_01.jpeg")) """
    # 🔥 Chemin SIMPLE et fiable
    logo_path = os.path.join(settings.BASE_DIR, "static", "images", "image_fallou_01.jpeg")

    context = {
        "facture": facture,
        "paiements": paiements,
        "total_paye": total_paye,
        "reste": reste,
        "logo_path": logo_path,  
    }

    html_string = render_to_string("facture_pdf.html", context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'filename="facture_{facture.numero}.pdf"'

   # 🔥 Utilise le chemin absolu pour accélérer le PDF
    """ HTML(string=html).write_pdf(response) """
    """ HTML(string=html_string, base_url=settings.BASE_DIR).write_pdf(response) """
     # 🔥 VERSION ULTRA RAPIDE
    HTML(
        string=html_string,
        base_url=settings.BASE_DIR
    ).write_pdf(
        response,
        stylesheets=[]  # 🔥 désactive chargement externe
    )

    return response


   
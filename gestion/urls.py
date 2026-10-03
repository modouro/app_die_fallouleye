from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("register/", views.register, name="register"),

    path("clients/", views.clients, name="clients"),
    path('client/create/', views.client_create, name='client_create'),
    path("client/update/<int:id>/", views.client_update, name="client_update"),
    path("client/delete/<int:id>/", views.client_delete, name="client_delete"),

    path("factures/", views.factures, name="factures"),
    path('facture/create/', views.facture_create, name='facture_create'),
    path("facture/update/<int:id>/", views.facture_update, name="facture_update"),
    path("facture/delete/<int:id>/", views.facture_delete, name="facture_delete"),
    
    path("paiement/create/", views.paiement_create, name="paiement_create"),
    path("facture/pdf/<int:id>/", views.facture_pdf, name="facture_pdf"),
    
]

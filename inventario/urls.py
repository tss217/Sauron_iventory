from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "inventario"

urlpatterns = [
    path("",RedirectView.as_view(pattern_name="inventario:cadastro", permanent=False),name="home",),
    path("cadastro/", views.cadastro, name="cadastro"),

    path("controle/", views.controle, name="controle"),
    path("controle/equipamento/<str:hhid>/",views.buscar_equipamento,name="buscar_equipamento",),
    path("controle/<int:controle_id>/etapa/",views.controle_etapa,name="controle_etapa",),
]
from django.urls import path
from .views import home, buscar, detalhes, carregar_bairros, quemsomos, contato

urlpatterns = [
    path("", home, name="home"),
    path("quemsomos/", quemsomos, name="quemsomos"),
    path("contato/", contato, name="contato"),
    path("estabelecimentos/", buscar, name="buscar"),
    path("detalhes/<slug:slug>/", detalhes, name="detalhes"),
    path("carregar_bairros/", carregar_bairros, name="carregar_bairros"),
]

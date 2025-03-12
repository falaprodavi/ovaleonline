from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Cidade, Bairro, Categoria, Estabelecimento
from django.db.models import Count
from django.core.paginator import Paginator


def carregar_bairros(request):
    cidade_id = request.GET.get("cidade_id")
    bairros = Bairro.objects.filter(cidade_id=cidade_id).values("id", "nome")
    return JsonResponse(list(bairros), safe=False)

def home(request):
    cidades = Cidade.objects.annotate(num_estabelecimentos=Count("estabelecimento")).order_by("-num_estabelecimentos")[:4]
    categorias = Categoria.objects.filter(categoria_pai__isnull=True) 
    estabelecimentos_destaque = Estabelecimento.objects.filter(destaque=True).order_by("-id")[:6]
    
    return render(request, "home.html", {
        "cidades": cidades,
        "categorias": categorias,
        "estabelecimentos": estabelecimentos_destaque
    })

def buscar(request):
    titulo = request.GET.get("titulo", "")
    cidade_id = request.GET.get("cidade", "")
    bairro_id = request.GET.get("bairro", "")
    categorias_id = request.GET.getlist("categoria")
    subcategorias_id = request.GET.getlist("subcategoria")  # Captura subcategorias selecionadas

    # Remover valores vazios
    categorias_id = [cat for cat in categorias_id if cat.strip()]
    subcategorias_id = [subcat for subcat in subcategorias_id if subcat.strip()]

    estabelecimentos = Estabelecimento.objects.all()
    categorias = Categoria.objects.filter(categoria_pai__isnull=True).prefetch_related("subcategorias")
    bairros = Bairro.objects.all()
    cidades = Cidade.objects.all()

    if titulo:
        estabelecimentos = estabelecimentos.filter(titulo__icontains=titulo)

    if cidade_id:
        estabelecimentos = estabelecimentos.filter(cidade_id=cidade_id)

    if bairro_id:
        estabelecimentos = estabelecimentos.filter(bairro_id=bairro_id)

    if subcategorias_id:
        # O usuário escolheu uma subcategoria específica, então filtramos apenas por ela
        estabelecimentos = estabelecimentos.filter(categorias__id__in=subcategorias_id).distinct()
    elif categorias_id:
        # O usuário escolheu apenas a categoria pai, então pegamos todas as subcategorias dela
        subcategorias_das_categorias = Categoria.objects.filter(categoria_pai__id__in=categorias_id).values_list("id", flat=True)
        todas_categorias_id = list(categorias_id) + list(subcategorias_das_categorias)
        estabelecimentos = estabelecimentos.filter(categorias__id__in=todas_categorias_id).distinct()

    # Aplicar paginação (9 resultados por página)
    paginator = Paginator(estabelecimentos, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "resultados.html", {
        "estabelecimentos": estabelecimentos,
        "titulo": titulo,
        "cidade_id": cidade_id,
        "bairro_id": bairro_id,
        "categorias_id": categorias_id,
        "subcategorias_id": subcategorias_id,  # Passa as subcategorias selecionadas para o template
        "categorias": categorias,
        "bairros": bairros,
        "cidades": cidades,
        "page_obj": page_obj,
    })



def detalhes(request, slug):
    estabelecimento = get_object_or_404(Estabelecimento, slug=slug)
    categorias = Categoria.objects.all()
    cidades = Cidade.objects.all() 
    return render(request, 'detalhes.html', {
        'estabelecimento': estabelecimento,
        'categorias': categorias,
        "cidades": cidades, 
        })

def quemsomos(request):
    categorias = Categoria.objects.all()
    cidades = Cidade.objects.all() 
    return render(request, 'quemsomos.html', {
        'categorias': categorias,
        "cidades": cidades, 
        })

def contato(request):
    return render(request, 'contato.html')
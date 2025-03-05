from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from .models import Cidade, Bairro, Categoria, Estabelecimento, ImagemEstabelecimento
from adminsortable2.admin import SortableTabularInline 
from adminsortable2.admin import SortableAdminBase
from django.db import models
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.text import slugify


class BairroInline(admin.TabularInline):  
    model = Bairro
    extra = 1

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ("nome", "foto_preview") 
    inlines = [BairroInline]
    
    def foto_preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;">', obj.foto.url)
        return "(Sem foto)"

    foto_preview.short_description = "Foto"

class ImagemEstabelecimentoInline(SortableTabularInline):
    model = ImagemEstabelecimento
    extra = 3
    fields = ("imagem", "image_preview", "ordem")  # Exibe o campo ordem e prévia da imagem
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 5px;">', obj.imagem.url)
        return "(Sem imagem)"

    image_preview.short_description = "Prévia da Imagem"

    
@admin.register(Estabelecimento)
class EstabelecimentoAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ("titulo", "cidade", "bairro", "categorias_list", "duplicar_estabelecimento")
    list_filter = ["cidade", "bairro"]
    inlines = [ImagemEstabelecimentoInline]  # Inclui a opção de ordenação das imagens
    filter_horizontal = ("categorias",) 
    
    def categorias_list(self, obj):
        return ", ".join([categoria.nome for categoria in obj.categorias.all()])
    categorias_list.short_description = "Categorias"
    
    def duplicar_estabelecimento(self, obj):
        return format_html('<a href="duplicate/{}/" class="button">Duplicar</a>', obj.pk)
    duplicar_estabelecimento.short_description = "Duplicar"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('duplicate/<int:pk>/', self.duplicate_estabelecimento_view, name='duplicate_estabelecimento'),
        ]
        return custom_urls + urls
    
    def duplicate_estabelecimento_view(self, request, pk):
        estabelecimento = Estabelecimento.objects.get(pk=pk)
        novo_estabelecimento = Estabelecimento.objects.get(pk=pk)

        # Criando um novo objeto, mas sem salvar ainda
        novo_estabelecimento.pk = None
        novo_estabelecimento.titulo = f"{estabelecimento.titulo} (Cópia)"
        novo_estabelecimento.slug = slugify(novo_estabelecimento.titulo)

        novo_estabelecimento.save()  # Salva o novo objeto no banco

        # Duplicar as relações ManyToMany (categorias e bairros)
        novo_estabelecimento.categorias.set(estabelecimento.categorias.all())

        messages.success(request, "Estabelecimento duplicado com sucesso!")
        return redirect(f"/admin/{estabelecimento._meta.app_label}/{estabelecimento._meta.model_name}/")
    
    

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;">', obj.logo.url)
        return "(Sem logo)"

    logo_preview.short_description = "Logo"

    class Media:
        js = ("admin/js/filtro_bairros.js",)
        
    formfield_overrides = {
        models.TextField: {"widget": CKEditorWidget()},
    }
    

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nome", "categoria_pai", "categoria_imagem_preview"]
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ("nome",)

    def categoria_imagem_preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;">', obj.imagem.url)
        return "(Sem imagem)"

    categoria_imagem_preview.short_description = "Imagem"


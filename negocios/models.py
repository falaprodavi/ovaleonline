from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    foto = models.ImageField(upload_to="cidades/", blank=True, null=True)
    def __str__(self):
        return self.nome

class Bairro(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True) 
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, related_name="bairros")
    def __str__(self):
        return f"{self.nome} - {self.cidade.nome}"

""" class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)  # Remova unique=True por enquanto
    imagem = models.ImageField(upload_to="categorias/", blank=True, null=True)  # Adiciona imagem para a categoria

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome """
        
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    imagem = models.ImageField(upload_to="categorias/", blank=True, null=True)
    categoria_pai = models.ForeignKey(
        "self",  # Relacionamento com a própria model
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subcategorias"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.categoria_pai:
            return f"{self.categoria_pai.nome} > {self.nome}"  # Mostra a hierarquia no admin
        return self.nome



class Estabelecimento(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    descricao = RichTextField() 
    endereco = models.CharField(max_length=255)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
    categorias = models.ManyToManyField("Categoria")
    telefone = models.CharField(max_length=20, blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    destaque = models.BooleanField(default=False)
    logo = models.ImageField(upload_to="logos/")    
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)


class ImagemEstabelecimento(models.Model):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, related_name="imagens")
    imagem = models.ImageField(upload_to="estabelecimentos/")
    ordem = models.PositiveIntegerField(default=0)  # Campo para definir a ordem das imagens
    class Meta:
        ordering = ["ordem"]  # Ordena as imagens automaticamente pelo campo 'ordem'
    def __str__(self):
        return f"Imagem de {self.estabelecimento.titulo} ({self.ordem})"

    


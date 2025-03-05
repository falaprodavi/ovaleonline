from django.core.management.base import BaseCommand
from faker import Faker
from negocios.models import Cidade, Bairro, Categoria, Estabelecimento
import random

class Command(BaseCommand):
    help = "Popula o banco de dados com dados falsos para testes"

    def handle(self, *args, **kwargs):
        fake = Faker("pt_BR")  # Define a língua para português

        # Criar algumas cidades
        for _ in range(5):
            cidade = Cidade.objects.create(nome=fake.city())

            # Criar bairros para cada cidade
            for _ in range(3):
                Bairro.objects.create(nome=fake.street_name(), cidade=cidade)

        # Criar categorias
        categorias = [Categoria.objects.create(nome=fake.word()) for _ in range(5)]

        # Criar estabelecimentos
        for _ in range(10):
            cidade = random.choice(Cidade.objects.all())
            bairro = random.choice(Bairro.objects.filter(cidade=cidade))
            categoria = random.choice(categorias)

            Estabelecimento.objects.create(
                titulo=fake.company(),
                descricao=fake.text(),
                endereco=fake.address(),
                cidade=cidade,
                bairro=bairro,
                categoria=categoria,
                telefone=fake.phone_number(),
                whatsapp=fake.phone_number(),
                email=fake.email(),
                redes_sociais=fake.url(),
                destaque=random.choice([True, False]),
            )

        self.stdout.write(self.style.SUCCESS("Banco de dados populado com sucesso! 🚀"))

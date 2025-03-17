from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.

class User(models.Model):
    nome = models.CharField(max_length=300, unique=True)
    senha = models.CharField(max_length=129)
    data_criacao = models.DateField( auto_now_add=True )

    def save(self, *args, **kwargs):
        if not self.pk or not check_password(self.senha, User.objects.get(pk=self.pk).senha):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    def __srt__(self):
        return 

class Tarefa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anotacao = models.CharField(max_length=3000)
    concluido = models.BooleanField( default = False)
    descricao = models.CharField(max_length=200, default="Não tem descrição")
    prioridade = models.IntegerField( default = 1)
    data = models.DateField( auto_now_add=True )

    def __str__(self):
        return f"Descrição: {self.descricao} - Status: Concluído" if self.concluido else f"Descrição: {self.descricao} - Status: Em Andamento"

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
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

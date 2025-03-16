from django.db import models

class User(models.Model):
    nome = models.CharField(max_length=300 )
    idade = models.IntegerField()
    senha = models.CharField(max_length=30)

    def __str__(self):
        return f"User: {self.nome.title()} - Age: {self.idade}"

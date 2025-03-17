from rest_framework import serializers
from .models import User, Tarefa 
from  django.contrib.auth.hashers import make_password

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","nome","data_criacao")

class UserDetailSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(
            write_only=True,#somente escrita
            style={"input_type":"password"})

    class Meta:
        model = User
        fields = ("id","nome","senha","data_criacao")

    def creat(self, validated_data):
        return User.objects.create(**validated_data) 

    def update(self, instance, validated_data):
        instance.nome = validated_data.pop("nome", instance.nome)
        if validated_data.pop("senha", None) is not None: 
            hashed_password = make_password(validated_data.pop("senha",None))
            instance.senha = hashed_password
        instance.save()
        return instance

class TarefaListSerializer(serializers.ModelSerializer):
    models = Tarefas
    fields = ("concluido","prioridade","data")

class TarefaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefas
        fields = ("user",
                  "anotacao",
                  "concluido",
                  "descricao",
                  "prioridade",
                  "data",
                  ) 

    def create(self, validated_data):
        return Tarefa.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.anotacao = validated_data.pop("anotacao", instance.anotacao)
        instance.concluido = validated_data.pop("concluido", instance.concluido)
        instance.descricao = validated_data.pop("descricao", instance.descricao)
        instance.prioridade = validated_data.pop("prioridade", instance.prioridade)
        instance.save()
        return instance




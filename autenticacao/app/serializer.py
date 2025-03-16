from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nome', 'idade')  # Sem a senha

class UserDetailSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, style={'input_type': 'password'})  # A senha só pode ser escrita (POST/PUT)

    class Meta:
        model = User
        fields = ('id', 'nome', 'idade', 'senha')

    def create(self, validated_data):
        """Sobrescreve o método create para criar um usuário, aplicando hashing na senha."""
        password = validated_data.pop('senha')  # Extrai a senha
        hashed_password = make_password(password)  # Aplica o hashing
        user = User.objects.create(senha=hashed_password, **validated_data)  # Salva a senha hasheada
        return user

    def update(self, instance, validated_data):
        """Sobrescreve o método update para atualizar um usuário, aplicando hashing na senha."""
        password = validated_data.pop('senha', None)  # Tenta obter a senha
        if password is not None:
            hashed_password = make_password(password)  # Aplica o hashing se a senha foi fornecida
            instance.senha = hashed_password
        instance.nome = validated_data.get('nome', instance.nome)
        instance.idade = validated_data.get('idade', instance.idade)
        instance.save()
        return instance

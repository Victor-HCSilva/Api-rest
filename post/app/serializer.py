from rest_framework import serializers
from .models import User, Tarefa
from  django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model



class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id","username","is_admin","date_joined") # Use username ao invés de nome
        read_only_fields = ('is_admin',) # Garante que o campo is_admin não possa ser alterado via API

    def create(self, validated_data):
        if 'is_admin' in validated_data and not self.context['request'].user.is_superuser: #evitar que super usuários sejam alterados
            validated_data['is_admin'] = False # Define is_admin como False
        user = get_user_model().objects.create_user(**validated_data) # Use create_user para lidar com o hash da senha
        return user



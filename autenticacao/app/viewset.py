from rest_framework import viewsets, permissions
from . import serializer
from .models import User  # Importe seu modelo User
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """
        Retorna o serializer apropriado com base na ação.
        """
        if self.action == 'list':
            return serializer.UserListSerializer
        return serializer.UserDetailSerializer

    def get_permissions(self):
        """Define as classes de permissão para cada ação."""
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]  # Qualquer um pode listar
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated] # Ou IsAuthenticated, se necessario
        else:
            permission_classes = [permissions.IsAuthenticated] # Requer autenticação
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

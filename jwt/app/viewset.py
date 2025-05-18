# --- START OF FILE viewset.py ---
from rest_framework import viewsets
from . import permissions as custom_permissions
from rest_framework import permissions as drf_permissions
from .import serializer
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return serializer.UserListSerializer
        return serializer.UserDetailSerializer

    def get_permissions(self):
        """
        Define as classes de permissão para cada ação.
        """
        if self.action == 'list':
            permission_classes = [drf_permissions.IsAuthenticated]
        elif self.action == 'create':
            # APENAS ADMINS PODEM CRIAR USUÁRIOS
            permission_classes = [custom_permissions.IsAdminUser] # Alteração aqui!
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [custom_permissions.IsOwnerOrAdmin]
        else:
            permission_classes = [custom_permissions.IsAdminUser] # Ou outra padrão restritiva
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

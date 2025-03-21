from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .permissions import IsAdminUser, IsOwnerOrAdmin
from .serializer import User, PasswordVerificationSerializer
from django.contrib.auth import get_user_model
from . import serializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return serializer.UserListSerializer
        return serializer.UserListSerializer

    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAuthenticated(), IsAdminUser()]
        elif self.action == "create":
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        else:
            return [permissions.IsAuthenticated()]



from rest_framework import viewsets, permissions, status
from . import serializer
from .models import User,Tarefa 
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return serializer.UserListSerializer
        return serializer.UserDetailSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_delete(self, instance):
        instance.delete()

class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    permission_class = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return serializer.TarefaListSerializer
        return serializer.TarefaDetailSerializer

    def get_permissions(self):
        permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, serializer):
        serializer.save()

    def update(self, serializer):
        serializer.save()

    def delete(self, instance):
        instance.delete()

    


from django.urls import path
from . import viewset
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("users/", viewset.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user'), # CORRETO
     path('users/<pk>/', viewset.UserViewSet.as_view({ # Note o <pk> para pegar o ID
        'get': 'retrieve',      # Buscar um usuário específico
        'put': 'update',        # Atualizar completamente um usuário
        'patch': 'partial_update', # Atualizar parcialmente um usuário
        'delete': 'destroy'      # Deletar um usuário
    }), name='user-detail'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

]

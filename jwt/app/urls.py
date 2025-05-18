from django.urls import path
from . import viewset
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Para login e obtenção inicial dos tokens
    TokenRefreshView,     # Para usar o refresh token e obter um novo access token
    TokenVerifyView,      # (Opcional) Para verificar se um token é válido
)
from . import views
urlpatterns = [
    path('', views.home_or_login_view, name='home'), # Ou o nome que você usa para a página de login
    path('logout/', views.logout_view, name='logout'),
    path('main/<int:id_user>/', views.main, name='main'),
    path(
        "users/",
        viewset.UserViewSet.as_view({"get": "list", "post": "create"}),
        name="user",
    ),
    path(
        "users/<pk>/",
        viewset.UserViewSet.as_view(
            {
                "get": "retrieve",  # Buscar um usuário específico
                "put": "update",  # Atualizar completamente um usuário
                "patch": "partial_update",  # Atualizar parcialmente um usuário
                "delete": "destroy",  # Deletar um usuário
            }
        ),
        name="user-detail",
    ),
    #JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'), # Opcional
]

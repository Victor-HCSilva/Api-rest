from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login: retorna access e refresh tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),# Refresh: renova o access token usando o refresh token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Verifica a validade de um token
]

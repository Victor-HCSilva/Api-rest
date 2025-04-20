from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite que usuários admin façam qualquer operação,
    mas usuários não-admin só podem ler (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        if (
            request.method in permissions.SAFE_METHODS
        ):  # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            return True
        return request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para permitir que apenas o dono de um objeto possa editá-lo.
    """

    def has_object_permission(self, request, view, obj):
        # Permissões de leitura são permitidas para qualquer requisição,
        # então sempre permitir solicitações GET, HEAD ou OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True

        # A permissão é concedida apenas se o usuário for o dono do objeto.
        return (
            obj.owner == request.user
        )  # Assumindo que seu modelo tem um campo 'owner'


# Create your views here.

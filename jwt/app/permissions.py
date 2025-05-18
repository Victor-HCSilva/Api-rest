# --- START OF FILE permissions.py ---

from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permissão personalizada para permitir que:
    - Administradores (is_staff=True) realizem qualquer ação.
    - Proprietários de um objeto o acessem/modifiquem (para ações de detalhe).
    """

    def has_permission(self, request, view):
        # Garante que o usuário esteja autenticado para tentar qualquer ação
        # que use esta permissão.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admins podem fazer qualquer coisa
        if request.user.is_staff:
            return True

        # O proprietário do objeto (o próprio usuário, neste caso) pode acessá-lo/modificá-lo.
        # 'obj' aqui será uma instância do modelo User.
        return obj == request.user

class IsAdminUser(permissions.BasePermission): # Certifique-se que esta classe existe
    """
    Permite acesso apenas a usuários administradores (is_staff=True).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

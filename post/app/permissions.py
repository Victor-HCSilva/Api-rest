from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permissão para permitir acesso apenas a administradores.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_admin

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permissão para permitir que:
    - Administradores acessem qualquer objeto.
    - Usuários comuns acessem apenas seus próprios objetos.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True  # Administradores têm permissão total

        # Verifica se o objeto tem um atributo 'user' (como Tarefa)
        if hasattr(obj, 'user'):
            return obj.user == request.user  # Usuários só podem acessar seus próprios objetos Tarefa

        # Se não tiver 'user', assume que o próprio objeto é o usuário (como User)
        return obj == request.user

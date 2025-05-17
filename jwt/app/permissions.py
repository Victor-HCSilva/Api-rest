from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permissão personalizada para permitir que:
    - Administradores (is_staff=True) realizem qualquer ação.
    - Proprietários de um objeto o acessem/modifiquem (para ações de detalhe).
    """

    def has_permission(self, request, view):
        # Permite acesso se o usuário for autenticado.
        # A lógica de objeto específico será tratada em `has_object_permission`.
        # Para ações de `list`, a view precisará filtrar a queryset ou ter sua própria lógica de permissão.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Administradores (is_staff) têm acesso total a qualquer objeto.
        # Presumimos que o 'request.user' tem um atributo 'is_staff'.
        # Se seu modelo User customizado não tiver 'is_staff', você precisará
        # de outra forma para identificar administradores (ex: um campo booleano 'is_admin').
        if request.user.is_staff: # <<<< VERIFIQUE SE SEU MODELO USER TEM 'is_staff'
            return True

        # Permissão de acesso/modificação de detalhes apenas para o proprietário do objeto.
        # 'obj' aqui é a instância do seu modelo User.
        return obj == request.user

# API de Usuários

Esta documentação descreve a API REST para gerenciar informações de usuários. A API foi construída utilizando Django REST Framework e oferece endpoints para criar, visualizar, atualizar e excluir usuários.

## Model (models.py)

O modelo `User` representa um usuário com os seguintes atributos:

*   `nome` (CharField): Nome do usuário (máximo 300 caracteres).
*   `idade` (IntegerField): Idade do usuário.
*   `senha` (CharField): Senha do usuário (máximo 30 caracteres).

```python
from django.db import models

class User(models.Model):
    nome = models.CharField(max_length=300 )
    idade = models.IntegerField()
    senha = models.CharField(max_length=30)

    def __str__(self):
        return f"User: {self.nome.title()} - Age: {self.idade}"
```

## Serializers (serializers.py)

Os serializers são responsáveis por converter instâncias do modelo `User` em dados que podem ser facilmente renderizados em JSON e vice-versa.

*   **UserListSerializer**: Serializa os campos `id`, `nome` e `idade` para exibir listas de usuários.
*   **UserDetailSerializer**: Serializa todos os campos do modelo `User` para detalhes do usuário.  A senha é `write_only` para segurança.

```python
from rest_framework import serializers
from .models import User

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nome', 'idade')  # Sem a senha

class UserDetailSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, style={'input_type': 'password'})  # A senha só pode ser escrita (POST/PUT)

    class Meta:
        model = User
        fields = ('id', 'nome', 'idade', 'senha')

    def create(self, validated_data):
        """Sobrescreve o método create para criar um usuário."""
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        """Sobrescreve o método update para atualizar um usuário."""
        senha = validated_data.pop('senha', None)
        if senha is not None:
            instance.senha = senha
        instance.nome = validated_data.get('nome', instance.nome)
        instance.idade = validated_data.get('idade', instance.idade)
        instance.save()
        return instance
```

## ViewSet (viewset.py)

O `UserViewSet` fornece a lógica para as operações da API. Ele usa diferentes serializers dependendo da ação e define permissões para controlar o acesso aos endpoints.

```python
from rest_framework import viewsets, permissions
from . import serializer
from .models import User  # Importe seu modelo User
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """
        Retorna o serializer apropriado com base na ação.
        """
        if self.action == 'list':
            return serializer.UserListSerializer
        return serializer.UserDetailSerializer

    def get_permissions(self):
        """Define as classes de permissão para cada ação."""
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]  # Qualquer um pode listar
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated] # Ou IsAuthenticated, se necessario
        else:
            permission_classes = [permissions.IsAuthenticated] # Requer autenticação
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
```

## Endpoints (urls.py)

A API expõe os seguintes endpoints:

*   `GET /users/`: Lista todos os usuários (requer autenticação).
*   `POST /users/`: Cria um novo usuário (requer autenticação).
*   `GET /users/<pk>/`: Obtém detalhes de um usuário específico (requer autenticação).
*   `PUT /users/<pk>/`: Atualiza um usuário completamente (requer autenticação).
*   `PATCH /users/<pk>/`: Atualiza parcialmente um usuário (requer autenticação).
*   `DELETE /users/<pk>/`: Deleta um usuário (requer autenticação).
*   `POST /api-token-auth/`: Obtém um token de autenticação para um usuário existente.

```python
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
```

**Autenticação:**

A API utiliza autenticação por token. Para obter um token, envie um POST request para `/api-token-auth/` com um username e senha válidos. O token retornado deve ser incluído no cabeçalho `Authorization` de cada requisição como `Token <seu_token>`.

**Permissões:**

*   `GET /users/`: Permissão `AllowAny` (Qualquer um pode listar os usuários).
*   `POST /users/`, `GET /users/<pk>/`, `PUT /users/<pk>/`, `PATCH /users/<pk>/`, `DELETE /users/<pk>/`: Permissão `IsAuthenticated` (Requer autenticação).

## Configurações (settings.py)

O arquivo `settings.py` contém as configurações do projeto Django, incluindo a configuração do banco de dados, das aplicações instaladas e do Django REST Framework.  É importante configurar corretamente a autenticação e as permissões no `REST_FRAMEWORK`.

```python
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ... (outras configurações)

INSTALLED_APPS = [
    # ...
    "rest_framework",
    'rest_framework.authtoken',
    "app", # Seu app
]

# ... (outras configurações)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication', # Opcional, para a Browsable API
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 3,
}
```

## Exemplos de Requisição

**1. Obter a lista de usuários (GET /users/)**

```
curl -X GET http://localhost:8000/users/ \
  -H 'Authorization: Token <seu_token>'
```

**2. Criar um novo usuário (POST /users/)**

```
curl -X POST http://localhost:8000/users/ \
  -H 'Authorization: Token <seu_token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "nome": "Novo Usuario",
    "idade": 30,
    "senha": "senha123"
  }'
```

**3. Obter um usuário específico (GET /users/<pk>/)**

```
curl -X GET http://localhost:8000/users/1/ \
  -H 'Authorization: Token <seu_token>'
```

**4. Atualizar um usuário (PUT /users/<pk>/)**

```
curl -X PUT http://localhost:8000/users/1/ \
  -H 'Authorization: Token <seu_token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "nome": "Usuario Atualizado",
    "idade": 35,
    "senha": "nova_senha"
  }'
```

**5. Deletar um usuário (DELETE /users/<pk>/)**

```
curl -X DELETE http://localhost:8000/users/1/ \
  -H 'Authorization: Token <seu_token>'
```

**6. Obter um token de autenticação (POST /api-token-auth/)**

```
curl -X POST http://localhost:8000/api-token-auth/ \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "seu_username",
    "password": "sua_senha"
  }'
```

## Notas

*   Substitua `<pk>` pelo ID do usuário desejado.
*   Certifique-se de substituir `<seu_token>` pelo seu token de autenticação.
*   A API requer autenticação para todas as operações, exceto para listar usuários.
*   Este exemplo usa `curl` para fazer as requisições. Você pode usar qualquer ferramenta HTTP client.
*   A senha é enviada/atualizada apenas quando explicitamente fornecida no corpo da requisição (POST/PUT/PATCH).
*   Use um sistema de autenticação robusto em ambientes de produção, como o OAuth2.
*   Valide e sanitize os dados de entrada para evitar vulnerabilidades de segurança.


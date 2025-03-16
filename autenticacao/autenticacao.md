Ok, vamos adicionar autenticação ao seu projeto Django REST Framework (DRF). Existem diversas formas de fazer isso, dependendo do nível de segurança e complexidade que você precisa.  Vou te mostrar as opções mais comuns e como implementá-las no seu código.

**Opções de Autenticação no Django REST Framework:**

1.  **Token Authentication:**  Uma forma simples de autenticação que usa tokens para identificar os usuários.  Cada usuário recebe um token único que deve ser incluído nos headers das requisições.

2.  **Session Authentication:** Usa o sistema de sessões padrão do Django.  Funciona bem para APIs que são consumidas por navegadores web, pois aproveita os cookies de sessão.

3.  **JSON Web Token (JWT) Authentication:**  Uma abordagem mais moderna e flexível, onde um token JWT é usado para transmitir informações sobre o usuário e validar a requisição.  Ótimo para APIs que serão consumidas por diversos clientes, incluindo aplicativos mobile.

4.  **OAuth2:** Um padrão robusto para autorização delegada.  Permite que aplicativos de terceiros acessem os recursos da sua API em nome dos usuários, sem que eles precisem compartilhar suas credenciais diretamente.

**Implementando a Autenticação por Token (Opção mais Simples para Começar):**

1.  **Instalar o Token Authentication:**

    ```bash
    pip install djangorestframework djangorestframework-simplejwt
    ```

2.  **Adicionar `rest_framework.authtoken` aos `INSTALLED_APPS` no `settings.py`:**

    ```python
    INSTALLED_APPS = [
        ...
        'rest_framework',
        'rest_framework.authtoken', # Adicione esta linha
        'app',
    ]
    ```

3.  **Adicionar o middleware de autenticação padrão do REST Framework e a autenticação por token no `REST_FRAMEWORK`:**

    ```python
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': 100,
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication',  # Autenticação por token
            'rest_framework.authentication.SessionAuthentication', # Autenticação por sessão
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated', # Permite apenas usuários autenticados
        ]
    }
    ```

    *   `DEFAULT_AUTHENTICATION_CLASSES`:  Define os métodos de autenticação que serão usados por padrão.
    *   `DEFAULT_PERMISSION_CLASSES`:  Define as permissões padrão.  `IsAuthenticated` garante que apenas usuários autenticados possam acessar a API.

4.  **Executar as migrações para criar a tabela de tokens:**

    ```bash
    python manage.py migrate
    ```

5.  **Criar tokens para os usuários:**

    Você pode criar tokens manualmente no shell do Django:

    ```python
    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token

    user = User.objects.get(username='seu_usuario')  # Substitua 'seu_usuario'
    token, created = Token.objects.get_or_create(user=user)
    print(token.key)
    ```

    Ou, você pode criar um endpoint para gerar tokens automaticamente quando um usuário faz login.  Veja o exemplo abaixo.

6. **Criar um endpoint de login para gerar tokens**

Adicione ao seu `core/urls.py`

```python
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token  # Importe a view para obter o token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include (route.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # Adicione esta linha
]
```

7. **Testar a Autenticação:**

*   Para acessar os endpoints protegidos, inclua o token no header da requisição:

    ```
    Authorization: Token SEU_TOKEN
    ```

    Substitua `SEU_TOKEN` pelo token do usuário. Você pode usar ferramentas como `curl`, `Postman` ou `Insomnia` para testar a API.

**Autenticação com JWT (JSON Web Tokens):**

JWT é uma abordagem mais moderna, especialmente útil para APIs que servem aplicativos mobile e outros clientes que não usam cookies.

1.  **Instale o pacote `djangorestframework-simplejwt`:**

    ```bash
    pip install djangorestframework-simplejwt
    ```

2.  **Adicione `rest_framework_simplejwt` aos `INSTALLED_APPS`:**

    ```python
    INSTALLED_APPS = [
        ...
        'rest_framework_simplejwt',
        'app',
    ]
    ```

3.  **Configure o `REST_FRAMEWORK` para usar a autenticação JWT:**

    ```python
    from datetime import timedelta

    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': 100,
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ]
    }

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # Tempo de vida do token de acesso
        'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # Tempo de vida do token de refresh
        'ROTATE_REFRESH_TOKENS': False,
        'BLACKLIST_AFTER_ROTATION': True,
    }
    ```

4.  **Adicione os endpoints para obter e atualizar os tokens JWT no `core/urls.py`:**

    ```python
    from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

    urlpatterns = [
        path("admin/", admin.site.urls),
        path("", include (route.urls)),
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]
    ```

5. **Testar a autenticação**

*   Envie uma requisição POST para `/api/token/` com seu `username` e `password` no corpo da requisição (em formato JSON).
*   Você receberá um token de acesso (`access`) e um token de refresh (`refresh`).
*   Para acessar os endpoints protegidos, inclua o token de acesso no header `Authorization`:

    ```
    Authorization: Bearer SEU_TOKEN_DE_ACESSO
    ```

*   Quando o token de acesso expirar, use o token de refresh para obter um novo token de acesso, enviando uma requisição POST para `/api/token/refresh/` com o token de refresh no corpo (em JSON).

**Outras Considerações:**

*   **Permissões:** Além de autenticação, você também pode usar permissões para controlar o acesso a diferentes recursos da sua API.  O DRF oferece diversas classes de permissão, como `IsAuthenticatedOrReadOnly` (permite acesso de leitura para usuários não autenticados e acesso total para usuários autenticados) e `IsAdminUser` (permite apenas administradores).

*   **Segurança:** Implemente medidas de segurança adicionais, como HTTPS, validação de dados e proteção contra ataques CSRF.

*   **Testes:** Escreva testes automatizados para garantir que a autenticação e a autorização funcionem corretamente.

**Qual opção escolher?**

*   **Token Authentication:** Boa para começar rapidamente, mas menos flexível que JWT.

*   **JWT:**  Recomendado para APIs mais complexas e que precisam suportar diferentes tipos de clientes.

*   **OAuth2:**  Necessário se você precisar permitir que aplicativos de terceiros acessem a API em nome dos usuários.

Lembre-se de adaptar as configurações e o código aos seus requisitos específicos.  Se precisar de ajuda com uma configuração específica, me diga qual opção você escolheu e como quer configurar seus endpoints, e eu te darei um exemplo mais detalhado.


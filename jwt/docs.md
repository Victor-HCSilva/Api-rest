## Documentação da API de Gerenciamento de Usuários com JWT

Esta documentação descreve uma API construída com Django e Django REST Framework (DRF), utilizando JSON Web Tokens (JWT) para autenticação, com os tokens sendo gerenciados via cookies HTTP-only.

### Índice
1.  Visão Geral
2.  Tecnologias Utilizadas
3.  Fluxo de Autenticação
    *   Login (Obtenção de Tokens)
    *   Acesso a Recursos Protegidos
    *   Refresh de Token
    *   Logout
    *   Gerenciamento de Cookies
4.  Endpoints da API (`UserViewSet`)
    *   `GET /users/` (Listar Usuários)
    *   `POST /users/` (Criar Usuário)
    *   `GET /users/<pk>/` (Detalhar Usuário)
    *   `PUT /users/<pk>/` (Atualizar Usuário)
    *   `PATCH /users/<pk>/` (Atualizar Parcialmente Usuário)
    *   `DELETE /users/<pk>/` (Deletar Usuário)
5.  Endpoints Adicionais de JWT (Opcionais para Acesso Direto)
    *   `POST /api/token/`
    *   `POST /api/token/refresh/`
    *   `POST /api/token/verify/`
6.  Views Django Tradicionais
    *   `GET, POST /` (Página de Login/Home)
    *   `GET /main/<id_user>/` (Página Principal do Usuário)
    *   `GET /logout/` (Logout do Usuário)
7.  Sistema de Permissões
    *   `IsOwnerOrAdmin`
    *   `IsAdminUser`
8.  Serializers
    *   `UserListSerializer`
    *   `UserDetailSerializer`
9.  Considerações Importantes

---

### 1. Visão Geral

O sistema oferece funcionalidades para gerenciamento de usuários (CRUD - Criar, Ler, Atualizar, Deletar) e um sistema de autenticação robusto baseado em JWT. A autenticação é primariamente gerenciada através de views Django que interagem com o `django-rest-framework-simplejwt` para gerar e validar tokens, armazenando-os em cookies seguros.

### 2. Tecnologias Utilizadas

*   **Django:** Framework web Python de alto nível.
*   **Django REST Framework (DRF):** Toolkit poderoso e flexível para construir APIs Web.
*   **Simple JWT (django-rest-framework-simplejwt):** Pacote para fornecer autenticação JWT para DRF.
*   **Cookies HTTP-only:** Para armazenamento seguro dos tokens JWT no cliente.

### 3. Fluxo de Autenticação

#### Login (Obtenção de Tokens)
*   **View Responsável:** `home_or_login_view` (acessível via `GET /` para formulário, `POST /` para submissão).
*   **Processo:**
    1.  O usuário submete `username` e `password` através de um formulário na página inicial.
    2.  A view `home_or_login_view` tenta autenticar o usuário usando `django.contrib.auth.authenticate`.
    3.  Se a autenticação for bem-sucedida e o usuário estiver ativo, a função `get_tokens_for_user` (que utiliza `RefreshToken.for_user` do Simple JWT) gera um par de tokens: `access` e `refresh`.
    4.  A função `_set_auth_cookies` define estes tokens em cookies HTTP-only:
        *   `ACCESS_TOKEN_COOKIE_NAME` (ex: `my_access_token`)
        *   `REFRESH_TOKEN_COOKIE_NAME` (ex: `my_refresh_token`)
    5.  O usuário é redirecionado para a página principal (`/main/<id_user>/`).
*   **Nota:** O endpoint `POST /api/token/` também está disponível para obter tokens diretamente via API, mas o fluxo principal da aplicação web usa a view `home_or_login_view`.

#### Acesso a Recursos Protegidos
*   Para as views Django protegidas (ex: `main`), o decorator `@jwt_cookie_required` é utilizado. Este decorator (cuja implementação não está totalmente visível, mas presume-se que) verifica a presença e validade do cookie de `access token`. Se válido, `request.user` é populado.
*   Para os endpoints da API DRF (ex: `/users/`), o `access token` deve ser enviado no cookie `ACCESS_TOKEN_COOKIE_NAME`. DRF, configurado adequadamente (presumivelmente através de `settings.SIMPLE_JWT` e `REST_FRAMEWORK` em `settings.py`), irá extrair e validar o token do cookie para autenticar a requisição.

#### Refresh de Token
*   **Endpoint:** `POST /api/token/refresh/`
*   **Processo:**
    1.  Quando o `access token` expira, o cliente (ou uma lógica no frontend/decorator) pode fazer uma requisição para este endpoint.
    2.  A requisição deve incluir o `refresh token` (que é enviado automaticamente se o cookie `REFRESH_TOKEN_COOKIE_NAME` estiver configurado com o `path` correto, como `/api/token/refresh/`).
    3.  Se o `refresh token` for válido, um novo `access token` é retornado.
    4.  A aplicação (através da função `_set_auth_cookies` ou similar) deve então atualizar o cookie do `access token`.
*   **Nota:** O decorator `@jwt_cookie_required` pode, opcionalmente, implementar a lógica de refresh automático se o access token expirar e um refresh token válido existir.

#### Logout
*   **View Responsável:** `logout_view` (acessível via `GET /logout/`).
*   **Processo:**
    1.  A view cria uma resposta de redirecionamento para a página inicial (`home`).
    2.  Os cookies `ACCESS_TOKEN_COOKIE_NAME` e `REFRESH_TOKEN_COOKIE_NAME` são deletados do navegador do cliente.
    3.  (Opcional) O `refresh_token_value` é lido dos cookies, indicando que poderia haver uma lógica para invalidar o token no backend (blacklist), mas não está implementada no código fornecido.

#### Gerenciamento de Cookies
A função `_set_auth_cookies` é central para configurar os cookies de autenticação:
*   **HTTPOnly:** `True` - Previne acesso ao cookie via JavaScript no cliente.
*   **Secure:** `True` em produção (se `settings.DEBUG` for `False`) - O cookie só é enviado sobre HTTPS.
*   **SameSite:** `Lax` (ou configurável) - Ajuda a mitigar ataques CSRF.
*   **Max-Age:** Definido com base nos `*_TOKEN_LIFETIME` do `settings.SIMPLE_JWT`.
*   **Path (para Refresh Token):** Configurado para `/api/token/refresh/` para garantir que o cookie de refresh só seja enviado para o endpoint de refresh.

### 4. Endpoints da API (`UserViewSet`)

Localizados sob o prefixo `/users/`.

#### `GET /users/` (Listar Usuários)
*   **Descrição:** Retorna uma lista de usuários.
*   **Permissões:** Requer autenticação (`drf_permissions.IsAuthenticated`).
*   **Lógica de Queryset:**
    *   Se o usuário não estiver autenticado, retorna uma lista vazia.
    *   Se o usuário for `is_staff` (admin), retorna todos os usuários.
    *   Caso contrário (usuário comum autenticado), retorna apenas o próprio usuário.
*   **Serializer:** `UserListSerializer` (campos: `id`, `username`, `first_name`, `last_name`, `email`).

#### `POST /users/` (Criar Usuário)
*   **Descrição:** Cria um novo usuário.
*   **Permissões:** Apenas administradores (`custom_permissions.IsAdminUser`).
*   **Serializer:** `UserDetailSerializer`.
*   **Tratamento de Senha:** A senha fornecida no campo `senha` é hasheada antes de salvar o usuário (feito no método `create` do serializer).

#### `GET /users/<pk>/` (Detalhar Usuário)
*   **Descrição:** Retorna os detalhes de um usuário específico.
*   **Permissões:** `custom_permissions.IsOwnerOrAdmin` (o próprio usuário ou um administrador).
*   **Serializer:** `UserDetailSerializer`.

#### `PUT /users/<pk>/` (Atualizar Usuário)
*   **Descrição:** Atualiza completamente os dados de um usuário específico.
*   **Permissões:** `custom_permissions.IsOwnerOrAdmin`.
*   **Serializer:** `UserDetailSerializer`.
*   **Tratamento de Senha:** Se uma nova senha for fornecida no campo `senha`, ela será hasheada e atualizada (feito no método `update` do serializer). A senha é opcional na atualização.

#### `PATCH /users/<pk>/` (Atualizar Parcialmente Usuário)
*   **Descrição:** Atualiza parcialmente os dados de um usuário específico.
*   **Permissões:** `custom_permissions.IsOwnerOrAdmin`.
*   **Serializer:** `UserDetailSerializer`.
*   **Tratamento de Senha:** Similar ao `PUT`.

#### `DELETE /users/<pk>/` (Deletar Usuário)
*   **Descrição:** Remove um usuário específico.
*   **Permissões:** `custom_permissions.IsOwnerOrAdmin`.

### 5. Endpoints Adicionais de JWT (Opcionais para Acesso Direto)

Estes são os endpoints padrão do Simple JWT e podem ser usados por clientes de API que não passam pelo fluxo de login baseado em formulário.

*   **`POST /api/token/` (`TokenObtainPairView`)**
    *   Usado para obter um par de tokens (access e refresh) fornecendo `username` e `password` no corpo da requisição.
*   **`POST /api/token/refresh/` (`TokenRefreshView`)**
    *   Usado para obter um novo `access token` fornecendo um `refresh token` válido.
*   **`POST /api/token/verify/` (`TokenVerifyView`)**
    *   (Opcional) Usado para verificar se um `access token` é válido.

### 6. Views Django Tradicionais

Estas views não são parte da API RESTful, mas sim da aplicação web Django.

#### `GET, POST /` (`home_or_login_view`)
*   **Descrição:** Página inicial que serve como formulário de login.
    *   `GET`: Exibe o formulário de login (presumivelmente `UserForm`).
    *   `POST`: Processa as credenciais de login, gera tokens JWT, define cookies e redireciona para a página principal do usuário.
*   **Template:** `index.html`

#### `GET /main/<id_user>/` (`main`)
*   **Descrição:** Página principal do usuário, acessível após o login.
*   **Proteção:** Decorada com `@jwt_cookie_required`, exigindo um cookie de access token válido.
*   **Lógica:**
    *   Verifica se o `request.user.id` (usuário autenticado pelo JWT) corresponde ao `id_user` da URL. Se não, retorna `HttpResponseForbidden`.
    *   Exibe informações do usuário atual e uma lista de todos os usuários (esta última parte pode ser uma falha de segurança/privacidade se não for intencional que qualquer usuário logado veja todos os outros).
*   **Template:** `main.html`

#### `GET /logout/` (`logout_view`)
*   **Descrição:** Realiza o logout do usuário.
*   **Processo:** Deleta os cookies de autenticação (`ACCESS_TOKEN_COOKIE_NAME`, `REFRESH_TOKEN_COOKIE_NAME`) e redireciona para a página inicial.

### 7. Sistema de Permissões

Duas classes de permissão personalizadas são usadas:

#### `IsOwnerOrAdmin` (`permissions.BasePermission`)
*   **`has_permission`:** Garante que o usuário esteja autenticado.
*   **`has_object_permission`:**
    *   Permite acesso se `request.user.is_staff` (administrador).
    *   Permite acesso se o objeto (`obj`) sendo acessado for o próprio `request.user` (o proprietário do objeto). Usado para ações de detalhe, atualização e deleção de um usuário.

#### `IsAdminUser` (`permissions.BasePermission`)
*   **`has_permission`:** Permite acesso apenas se `request.user.is_staff` for `True` e o usuário estiver autenticado. Usado para ações como criação de novos usuários via API.

No `UserViewSet`, o método `get_permissions` define dinamicamente qual classe de permissão aplicar com base na ação (`list`, `create`, `retrieve`, etc.).

### 8. Serializers

#### `UserListSerializer` (`serializers.ModelSerializer`)
*   **Modelo:** `User`
*   **Campos:** `id`, `username`, `first_name`, `last_name`, `email`.
*   **Uso:** Para a ação `list` do `UserViewSet`, fornecendo uma representação concisa dos usuários.

#### `UserDetailSerializer` (`serializers.ModelSerializer`)
*   **Modelo:** `User`
*   **Campos:** `id`, `username`, `first_name`, `last_name`, `email`, `senha`.
*   **Campo `senha`:**
    *   `write_only=True`: Não é incluído na resposta da API.
    *   `required=False`: Opcional para atualizações.
    *   Usado para receber a senha em texto plano.
*   **Método `create`:**
    *   Remove o campo `senha` dos dados validados.
    *   Cria o usuário usando `User.objects.create_user()` (que pode lidar com a senha se fornecida como 'password').
    *   Se `senha` foi explicitamente fornecida, usa `user.set_password(password)` para hashear e definir a senha.
*   **Método `update`:**
    *   Remove o campo `senha` dos dados validados.
    *   Atualiza os outros campos do usuário.
    *   Se `senha` foi fornecida, usa `instance.set_password(password)` para hashear e atualizar a senha.
*   **Uso:** Para todas as ações do `UserViewSet` exceto `list`.

### 9. Considerações Importantes

*   **Segurança de Cookies:** O uso de `HttpOnly`, `Secure` (em produção) e `SameSite` para cookies é uma boa prática de segurança.
*   **Configuração de `SIMPLE_JWT`:** As configurações em `settings.py` para `SIMPLE_JWT` (como `ACCESS_TOKEN_LIFETIME`, `REFRESH_TOKEN_LIFETIME`, `AUTH_COOKIE`, `AUTH_COOKIE_SECURE`, `AUTH_COOKIE_SAMESITE`, `AUTH_HEADER_TYPES`) são cruciais para o correto funcionamento e segurança. O código atual parece gerenciar os cookies manualmente, o que é uma alternativa válida à configuração `AUTH_COOKIE` do `simple-jwt`.
*   **Decorator `@jwt_cookie_required`:** A implementação exata deste decorator não foi fornecida nos arquivos, mas seu papel é fundamental para proteger as views Django que dependem de autenticação via JWT em cookies.
*   **Listagem de Usuários em `main` view:** A view `main` atualmente busca `User.objects.all()` e passa para o template. Isso significa que um usuário logado, mesmo não sendo administrador, teria acesso à lista completa de usernames (ou outros dados, dependendo do template `main.html`). Isso pode ser uma questão de privacidade/segurança a ser revisada.
*   **UserForm:** O `UserForm` é importado em `views.py` mas não utilizado explicitamente no fluxo de login (que pega `username` e `password` diretamente de `request.POST`). Ele pode ser usado para registro de novos usuários ou como parte do contexto do template `index.html`. Se for para registro, a lógica de criação de usuário com hashing de senha precisaria ser implementada nessa view.

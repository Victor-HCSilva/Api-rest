 // A versão pode variarra limitar o tempo dos tokens de acesso e criar tokens de refresh no Django REST Framework (DRF), a biblioteca mais recomendada e amplamente utilizada é a `djangorestframework-simplejwt`. Ela substitui o sistema de token padrão do DRF por tokens JWT (JSON Web Tokens), que têm datas de expiração embutidas e suportam o conceito de tokens de refresh.

 Veja como implementá-la:

 **1. Instalação:**

 ```bash
 pip install djangorestframework-simplejwt
 ```

 **2. Configuração no `settings.py`:**

 Adicione `rest_framework_simplejwt` às suas `INSTALLED_APPS`:

 ```python
# settings.py

 INSTALLED_APPS = [
     # ... outras apps
         'rest_framework',
             'rest_framework_simplejwt',
                 'rest_framework_simplejwt.token_blacklist', # Para funcionalidade de logout/blacklist
                     # ... suas apps
                     ]
                     ```

                     Configure o DRF para usar `JWTAuthentication` como a classe de autenticação padrão (ou para views específicas):

                     ```python
# settings.py

                     REST_FRAMEWORK = {
                             'DEFAULT_AUTHENTICATION_CLASSES': (
                                     'rest_framework_simplejwt.authentication.JWTAuthentication',
                                         ),
                                             # ... outras configurações do DRF
                     }
                     ```

                     Configure os tempos de vida dos tokens. Você pode personalizar outros aspectos também:

                     ```python
# settings.py

                     from datetime import timedelta

                     SIMPLE_JWT = {
                             'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),       # Tempo de vida do token de acesso
                                 'REFRESH_TOKEN_LIFETIME': timedelta(days=1),        # Tempo de vida do token de refresh
                                     'ROTATE_REFRESH_TOKENS': False,                     # Se True, um novo refresh token é retornado ao usar o refresh token antigo
                                         'BLACKLIST_AFTER_ROTATION': True,                   # Se True, o refresh token antigo é adicionado à blacklist após a rotação
                                             'UPDATE_LAST_LOGIN': False,                         # Se True, atualiza o campo last_login do usuário ao logar

                                                 'ALGORITHM': 'HS256',
                                                     'SIGNING_KEY': SECRET_KEY,                          # Use sua SECRET_KEY
                                                         'VERIFYING_KEY': None,
                                                             'AUDIENCE': None,
                                                                 'ISSUER': None,
                                                                     'JWK_URL': None,
                                                                         'LEEWAY': 0,

                                                                             'AUTH_HEADER_TYPES': ('Bearer',),                   # Tipo de header de autenticação (Bearer <token>)
                                                                                 'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
                                                                                     'USER_ID_FIELD': 'id',
                                                                                         'USER_ID_CLAIM': 'user_id',
                                                                                             'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

                                                                                                 'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
                                                                                                     'TOKEN_TYPE_CLAIM': 'token_type',
                                                                                                         'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

                                                                                                             'JTI_CLAIM': 'jti',

                                                                                                                 'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
                                                                                                                     'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
                                                                                                                         'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
                     }
                     ```
                     *   **`ACCESS_TOKEN_LIFETIME`**: Define quanto tempo um token de acesso é válido. Após esse período, ele expira e não pode mais ser usado para acessar recursos protegidos.
                     *   **`REFRESH_TOKEN_LIFETIME`**: Define quanto tempo um token de refresh é válido. Ele é usado para obter um novo token de acesso sem que o usuário precise se autenticar novamente com credenciais.
                     *   **`ROTATE_REFRESH_TOKENS`**: Se `True`, cada vez que um token de refresh é usado para obter um novo token de acesso, um novo token de refresh também é emitido. O token de refresh antigo pode ser invalidado (dependendo de `BLACKLIST_AFTER_ROTATION`). Isso aumenta a segurança, pois os tokens de refresh têm uma vida útil efetiva menor.
                     *   **`BLACKLIST_AFTER_ROTATION`**: Requer que `rest_framework_simplejwt.token_blacklist` esteja em `INSTALLED_APPS`. Se `True` e `ROTATE_REFRESH_TOKENS` for `True`, o token de refresh antigo usado para obter um novo par de tokens será adicionado à blacklist, impedindo seu reuso.

                     **3. Migrações:**

                     Como adicionamos `rest_framework_simplejwt.token_blacklist` (opcional, mas recomendado para logout), precisamos rodar as migrações:

                     ```bash
                     python manage.py migrate
                     ```

                     **4. URLs:**

                     A biblioteca fornece views prontas para obter e atualizar tokens. Adicione-as ao seu `urls.py` principal ou de uma app específica:

                     ```python
# urls.py (do projeto ou de uma app)

                     from django.urls import path
                     from rest_framework_simplejwt.views import (
                         TokenObtainPairView,
                             TokenRefreshView,
                                 TokenVerifyView, # Opcional, para verificar um token
                                 )

                     urlpatterns = [
                         # ... suas outras urls
                             path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                                 path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                                     path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'), # Opcional
                                     ]
                                     ```

                                     **5. Fluxo de Autenticação:**

                                     *   **Login (Obter Tokens):**
                                         O cliente envia uma requisição `POST` para `/api/token/` com `username` e `password` no corpo da requisição:
                                             ```json
                                                 {
                                                             "username": "seu_usuario",
                                                                     "password": "sua_senha"
                                                                         }
                                                                             ```
                                                                                 Se as credenciais forem válidas, a resposta será:
                                                                                     ```json
                                                                                         {
                                                                                                     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", // Token de refresh (longa duração)
                                                                                                             "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  // Token de acesso (curta duração)
                                                                                                                 }
                                                                                                                     ```
                                                                                                                         O cliente deve armazenar ambos os tokens de forma segura. O token de acesso é usado nas requisições subsequentes.

                                                                                                                         *   **Acessar Recursos Protegidos:**
                                                                                                                             Para acessar um endpoint protegido, o cliente envia o token de acesso no header `Authorization`:
                                                                                                                                 `Authorization: Bearer <access_token>`

                                                                                                                                 *   **Refresh do Token de Acesso:**
                                                                                                                                     Quando o token de acesso expirar (configurado por `ACCESS_TOKEN_LIFETIME`), o cliente receberá um erro `401 Unauthorized`.
                                                                                                                                         Nesse momento, o cliente deve enviar uma requisição `POST` para `/api/token/refresh/` com o token de refresh no corpo:
                                                                                                                                             ```json
                                                                                                                                                 {
                                                                                                                                                             "refresh": "<seu_refresh_token>"
                                                                                                                                                                 }
                                                                                                                                                                     ```
                                                                                                                                                                         Se o token de refresh for válido e não tiver expirado, a resposta será um novo token de acesso:
                                                                                                                                                                             ```json
                                                                                                                                                                                 {
                                                                                                                                                                                             "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." // Novo token de acesso
                                                                                                                                                                                                     // Se ROTATE_REFRESH_TOKENS=True, um novo refresh token também pode ser retornado:
                                                                                                                                                                                                             // "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                                                                                                                                                                                                                 }
                                                                                                                                                                                                                     ```
                                                                                                                                                                                                                         O cliente substitui o token de acesso antigo pelo novo e pode tentar novamente a requisição original.

                                                                                                                                                                                                                         *   **Logout (Invalidar Token de Refresh):**
                                                                                                                                                                                                                             Para implementar um logout seguro, você precisa invalidar o token de refresh. Isso é feito adicionando-o à "blacklist". Crie uma view para isso:

                                                                                                                                                                                                                                 ```python
                                                                                                                                                                                                                                     # Em uma das suas apps, por exemplo, `accounts/views.py`

                                                                                                                                                                                                                                         from rest_framework.views import APIView
                                                                                                                                                                                                                                             from rest_framework.response import Response
                                                                                                                                                                                                                                                 from rest_framework import status
                                                                                                                                                                                                                                                     from rest_framework.permissions import IsAuthenticated
                                                                                                                                                                                                                                                         from rest_framework_simplejwt.tokens import RefreshToken

                                                                                                                                                                                                                                                             class LogoutView(APIView):
                                                                                                                                                                                                                                                                     permission_classes = (IsAuthenticated,) # Opcional, garante que o usuário está logado para deslogar

                                                                                                                                                                                                                                                                             def post(self, request):
                                                                                                                                                                                                                                                                                         try:
                                                                                                                                                                                                                                                                                                         refresh_token = request.data["refresh"]
                                                                                                                                                                                                                                                                                                                         token = RefreshToken(refresh_token)
                                                                                                                                                                                                                                                                                                                                         token.blacklist()
                                                                                                                                                                                                                                                                                                                                                         return Response(status=status.HTTP_205_RESET_CONTENT)
                                                                                                                                                                                                                                                                                                                                                                     except Exception as e:
                                                                                                                                                                                                                                                                                                                                                                                     return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': str(e)})

                                                                                                                                                                                                                                                                                                                                                                                         # Adicione a URL para LogoutView em seu `urls.py`
                                                                                                                                                                                                                                                                                                                                                                                             # from .views import LogoutView
                                                                                                                                                                                                                                                                                                                                                                                                 # path('api/logout/', LogoutView.as_view(), name='logout'),
                                                                                                                                                                                                                                                                                                                                                                                                     ```
                                                                                                                                                                                                                                                                                                                                                                                                         O cliente envia o token de refresh para este endpoint. No lado do cliente, após o logout bem-sucedido, os tokens de acesso e refresh devem ser removidos do armazenamento.

                                                                                                                                                                                                                                                                                                                                                                                                         **6. Protegendo Views:**

                                                                                                                                                                                                                                                                                                                                                                                                         Para proteger suas views, use as classes de permissão do DRF, como `IsAuthenticated`:

                                                                                                                                                                                                                                                                                                                                                                                                         ```python
# views.py (de uma app)

                                                                                                                                                                                                                                                                                                                                                                                                         from rest_framework.views import APIView
                                                                                                                                                                                                                                                                                                                                                                                                         from rest_framework.response import Response
                                                                                                                                                                                                                                                                                                                                                                                                         from rest_framework.permissions import IsAuthenticated

                                                                                                                                                                                                                                                                                                                                                                                                         class MinhaViewProtegida(APIView):
                                                                                                                                                                                                                                                                                                                                                                                                             permission_classes = [IsAuthenticated] # Só usuários autenticados com token válido podem acessar

                                                                                                                                                                                                                                                                                                                                                                                                                 def get(self, request):
                                                                                                                                                                                                                                                                                                                                                                                                                         return Response({"message": f"Olá, {request.user.username}! Você tem acesso."})
                                                                                                                                                                                                                                                                                                                                                                                                                         ```

                                                                                                                                                                                                                                                                                                                                                                                                                         **Resumo do Fluxo no Cliente:**

                                                                                                                                                                                                                                                                                                                                                                                                                         1.  Usuário faz login -> Cliente envia credenciais para `/api/token/`.
                                                                                                                                                                                                                                                                                                                                                                                                                         2.  Servidor retorna `access_token` e `refresh_token`.
                                                                                                                                                                                                                                                                                                                                                                                                                         3.  Cliente armazena os tokens (e.g., `access_token` em memória/cookie, `refresh_token` em `localStorage` ou cookie `HttpOnly`).
                                                                                                                                                                                                                                                                                                                                                                                                                         4.  Para cada requisição a um endpoint protegido, cliente envia `access_token` no header `Authorization: Bearer <token>`.
                                                                                                                                                                                                                                                                                                                                                                                                                         5.  Se o servidor retorna `401 Unauthorized` (token de acesso expirou):
                                                                                                                                                                                                                                                                                                                                                                                                                             a.  Cliente envia `refresh_token` para `/api/token/refresh/`.
                                                                                                                                                                                                                                                                                                                                                                                                                                 b.  Servidor retorna um novo `access_token` (e opcionalmente um novo `refresh_token`).
                                                                                                                                                                                                                                                                                                                                                                                                                                     c.  Cliente atualiza seu `access_token` e tenta a requisição original novamente.
                                                                                                                                                                                                                                                                                                                                                                                                                                     6.  Se o refresh falhar (e.g., `refresh_token` expirou ou foi invalidado):
                                                                                                                                                                                                                                                                                                                                                                                                                                         a.  Cliente deve redirecionar o usuário para a tela de login.
                                                                                                                                                                                                                                                                                                                                                                                                                                         7.  Logout:
                                                                                                                                                                                                                                                                                                                                                                                                                                             a.  Cliente envia o `refresh_token` para o endpoint de logout (ex: `/api/logout/`).
                                                                                                                                                                                                                                                                                                                                                                                                                                                 b.  Servidor adiciona o `refresh_token` à blacklist.
                                                                                                                                                                                                                                                                                                                                                                                                                                                     c.  Cliente remove ambos os tokens do seu armazenamento.

                                                                                                                                                                                                                                                                                                                                                                                                                                                     Essa configuração oferece um sistema de autenticação robusto com tokens de curta duração para acesso e tokens de longa duração para renovação, melhorando a segurança da sua API.

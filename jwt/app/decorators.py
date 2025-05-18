from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.conf import settings
from django.http import HttpResponseForbidden

# Nomes dos cookies (melhor definir em settings.py e importar)
ACCESS_TOKEN_COOKIE_NAME = getattr(settings, 'SIMPLE_JWT_ACCESS_COOKIE_NAME', 'access_token_cookie')
REFRESH_TOKEN_COOKIE_NAME = getattr(settings, 'SIMPLE_JWT_REFRESH_COOKIE_NAME', 'refresh_token_cookie')

def jwt_cookie_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        access_token_value = request.COOKIES.get(ACCESS_TOKEN_COOKIE_NAME)

        if not access_token_value:
            # Tentar usar o refresh token para obter um novo access token
            # (Lógica de refresh pode ser mais complexa e movida para um helper)
            refresh_token_value = request.COOKIES.get(REFRESH_TOKEN_COOKIE_NAME)
            if refresh_token_value:
                try:
                    refresh = RefreshToken(refresh_token_value)
                    refresh.verify() # Verifica se o refresh token é válido

                    # Se o refresh token for válido, gere novos tokens
                    user = User.objects.get(id=refresh['user_id']) # O refresh token contém o user_id

                    new_access_token = str(refresh.access_token)
                    new_refresh_token = str(refresh) # Se ROTATE_REFRESH_TOKENS=True, este será um novo refresh token

                    # Chamar a view original, mas antes preparar uma resposta para setar os novos cookies
                    # Isso é um pouco complicado porque o decorator não cria a resposta.
                    # Uma abordagem seria redirecionar para a mesma URL com os novos cookies
                    # ou, se for uma requisição AJAX, retornar os novos tokens para o cliente.
                    # Para uma navegação simples, pode ser melhor redirecionar para o login se o access token expirou.

                    # Simplificação: Se o access token expirou, e temos um refresh,
                    # vamos popular request.user e deixar a view decidir.
                    # A view, ao retornar, deveria setar os novos cookies.
                    # Isso requer que a view tenha acesso aos novos tokens.
                    # Por agora, vamos apenas redirecionar para login se o access token falhar.
                    # O refresh automático é um passo mais avançado.
                    # print("Access token expirado, refresh token presente. Implementar lógica de refresh aqui.")
                    # return redirect('home') # Ou uma URL de "refresh_session"

                    # Por simplicidade aqui, se o access token falhou, redireciona para login.
                    # O refresh silencioso é mais complexo de implementar em um decorator simples para views HTML.
                    return redirect('home') # Ou para onde você faz login

                except (TokenError, InvalidToken, AuthenticationFailed, User.DoesNotExist):
                    # Refresh token inválido ou expirado
                    response = redirect('home')
                    response.delete_cookie(REFRESH_TOKEN_COOKIE_NAME) # Limpa cookie inválido
                    response.delete_cookie(ACCESS_TOKEN_COOKIE_NAME) # Limpa cookie inválido
                    return response

            # Se não há access nem refresh token válido
            return redirect('home')

        try:
            access_token = AccessToken(access_token_value)
            access_token.verify() # Verifica validade e expiração

            user_id = access_token['user_id']
            request.user = User.objects.get(id=user_id)
            if not request.user.is_active:
                # return HttpResponseForbidden("Sua conta está desativada.")
                # Melhor redirecionar para login com uma mensagem
                response = redirect('home')
                # Adicionar mensagem de erro se estiver usando Django messages framework
                # messages.error(request, "Sua conta está desativada.")
                return response


        except (TokenError, InvalidToken, AuthenticationFailed, User.DoesNotExist):
            # Token inválido, expirado ou usuário não existe
            # Aqui também seria um bom lugar para tentar o refresh token, se implementado.
            response = redirect('home')
            response.delete_cookie(ACCESS_TOKEN_COOKIE_NAME) # Limpa cookie inválido
            # messages.error(request, "Sessão inválida ou expirada. Por favor, faça login novamente.")
            return response
        except Exception as e:
            # Outro erro
            print(f"Erro inesperado na autenticação JWT por cookie: {e}")
            return redirect('home')

        return view_func(request, *args, **kwargs)
    return _wrapped_view

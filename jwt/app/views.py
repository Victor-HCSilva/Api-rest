from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import UserForm # Mantenha se usar para registro
from django.contrib.auth import authenticate
from django.contrib import messages
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .decorators import jwt_cookie_required, ACCESS_TOKEN_COOKIE_NAME, REFRESH_TOKEN_COOKIE_NAME


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Para configurar cookies de forma consistente
def _set_auth_cookies(response, access_token, refresh_token=None):
    access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        max_age=access_token_lifetime.total_seconds(),
        httponly=True,
        secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', not settings.DEBUG), # True em prod
        samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax')
    )
    if refresh_token:
        refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        response.set_cookie(
            key=REFRESH_TOKEN_COOKIE_NAME,
            value=refresh_token,
            max_age=refresh_token_lifetime.total_seconds(),
            httponly=True,
            secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', not settings.DEBUG), # True em prod
            samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax'),
            path=settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH_PATH', '/api/token/refresh/') # Ou '/' se mais simples
        )


def home_or_login_view(request):
    form = UserForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password) # request é opcional mas bom

        if user is not None:
            if user.is_active:
                tokens = get_tokens_for_user(user)

                # Redirecionar para a página principal e definir cookies
                response = redirect('main', id_user=user.id)
                _set_auth_cookies(response, tokens['access'], tokens['refresh'])

                messages.success(request, 'Login realizado com sucesso!')
                return response
            else:
                messages.error(request, 'Esta conta está desativada.')
        else:
            messages.error(request, 'Nome do usuário ou senha inválidos!')
            print(form.errors)

    form = UserForm()
    return render(request, "index.html", {"form": form})


@jwt_cookie_required
def main(request, id_user):
    usuarios = User.objects.all()
    user = get_object_or_404(User, id=id_user)

    if request.user.id != id_user:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.") # Opção 2

    context = {"current_user_info":request.user,
               "usuarios":usuarios,
               "user":user
               }
    return render(request, "main.html", context)


def logout_view(request):
    response = redirect('home')

    refresh_token_value = request.COOKIES.get(REFRESH_TOKEN_COOKIE_NAME)
    if refresh_token_value:
        pass

    response.delete_cookie(ACCESS_TOKEN_COOKIE_NAME)
    response.delete_cookie(REFRESH_TOKEN_COOKIE_NAME, path=settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH_PATH', '/api/token/refresh/')) # Certifique-se que o path corresponde ao usado no set_cookie

    messages.info(request, "Você foi desconectado com sucesso.")
    return response

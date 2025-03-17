from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import viewset

urlpatterns = [
    path("users/", viewset.UserViewSet.as_view({"get":"list", "post":"create"}),
         name="users"),
    path("user/<pk>/",
         viewset.UserViewSet.as_view(
            {
                "get":"retrieve",
                "put":"update",
                "path":"partial_update",
                "delete":"destroy",
            }
        ),
         name="user_detail"),
    path("get-token/", obtain_auth_token, name="token_auth"),

    path("tarefas_existentes/", viewset.TarefaViewSet.as_view({"get":"list", "post": "create"}),
         name="tarefas"),
    path("tarefa/<pk>/",
         viewset.TarefaViewSet.as_view(
            {
                "get":"retrieve",
                "put":"update",
                "path":"partial_update",
                "delete":"destroy",
            }
        ),
        name="tarefa_detail" )
]


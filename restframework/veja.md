# API REST com Django REST Framework

## Configurações deste projeto

Este guia descreve os passos para criar uma API RESTful usando Django e Django REST Framework.

**Passos:**

1.  **Criar o Model:** Defina a estrutura de dados no arquivo `models.py` do seu app.
2.  **Criar arquivos `api/viewset.py`:**  Implemente a lógica da API usando ViewSets do Django REST Framework.
3.  **Criar arquivos `api/serializer.py`:**  Defina os Serializers para converter objetos do model em JSON e vice-versa.
4.  **Adicionar os apps ao `settings.py`:**  Registre seu app e o Django REST Framework na lista `INSTALLED_APPS`.
5.  **Configurar as URLs:**  Configure as URLs da API no arquivo `urls.py` do seu projeto.
6.  **Configurar a Paginação (opcional):**  Personalize a paginação no arquivo `settings.py`.

**Exemplos de Código:**

### 1. Model (`app/models.py`)

```python
from django.db import models
from uuid import uuid4

class Books(models.Model):
    id_book = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    age = models.IntegerField()
    state = models.CharField(max_length=50)
    pages = models.IntegerField()
    publishing_company = models.CharField(max_length=255)
    create_at = models.DateField(auto_now_add=True)

    def __str__(self): #Adicionei para representação mais fácil do objeto
        return self.title
```

### 2. Serializer (`app/api/serializer.py`)

```python
from rest_framework import serializers
from app import models

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Books
        fields = "__all__"
```

### 3. ViewSet (`app/api/viewset.py`)

```python
from rest_framework import viewsets
from app.api import serializer
from app import models

class BooksViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.BooksSerializer
    queryset = models.Books.objects.all()
```

### 4. URLs (`core/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from app.api import viewsets as booksviewset

route = routers.DefaultRouter()
route.register(r"books", booksviewset.BooksViewSet, basename="books")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(route.urls)),
]
```

### 5. Paginação (`core/settings.py`)

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}
```

### 6. Adicionar apps (`core/settings.py`)

Dentro de `INSTALLED_APPS` adicionar `'rest_framework'` e o nome do seu app, exemplo `'app'`

**Exemplo de Logs de URLs:**

```
[07/Mar/2025 02:48:55] "GET /books/ HTTP/1.1" 200 9808
[07/Mar/2025 02:50:18] "POST /books/ HTTP/1.1" 201 10236
[07/Mar/2025 02:50:56] "GET /books/aa4effe8-cc11-4426-b7f8-ab9aed7481b5 HTTP/1.1" 301 0
[07/Mar/2025 02:50:56] "GET /books/aa4effe8-cc11-4426-b7f8-ab9aed7481b5/ HTTP/1.1" 200 11995
[07/Mar/2025 02:50:58] "GET /books/aa4effe8-cc11-4426-b7f8-ab9aed7481b5/ HTTP/1.1" 200 11995
[07/Mar/2025 02:52:00] "POST /books/ HTTP/1.1" 201 10248
```



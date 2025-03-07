
# API REST
## configurações

- criar model
- criar arquivos api/viewset.py
- criar arquivos api/serializer.py

- Adicionar os apps -nome do app e rest_framework

- Esta configuração do rest_framework em core/urls:

```py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from app.api import viewsets as booksviewset   

route = routers.DefaultRouter()
route.register(r"books",booksviewset.BooksViewSet,basename="books")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include (route.urls)),
]
```

- Urls (Log):

```bash
[07/Mar/2025 02:48:55] "GET /books/ HTTP/1.1" 200 9808
[07/Mar/2025 02:50:18] "POST /books/ HTTP/1.1" 201 10236
[07/Mar/2025 02:50:56] "GET /books/aa4effe8-cc11-4426-b7f8-ab9aed7481b5 HTTP/1.1" 301 0
[07/Mar/2025 02:50:56] "GET /books/aa4effe8-cc11-4426-b7f8-ab9aed7481b5/ HTTP/1.1" 200 11995
[07/Mar/2025 02:50:58] "GET /books/aa4effe8-cc11-4426-b7f8-ab9aed7481b5/ HTTP/1.1" 200 11995
[07/Mar/2025 02:52:00] "POST /books/ HTTP/1.1" 201 10248

```



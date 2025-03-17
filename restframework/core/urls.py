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

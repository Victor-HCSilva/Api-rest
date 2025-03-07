from rest_framework import viewsets
from app.api import serializer
from app import models

class BooksViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.BooksSerializer
    queryset = models.Books.objects.all()

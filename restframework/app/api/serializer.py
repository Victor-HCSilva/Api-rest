from  rest_framework import serializers
from app import models

class BooksSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.Books
        fields = "__all__"



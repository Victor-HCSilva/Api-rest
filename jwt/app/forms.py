from django.forms import ModelForm
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        #fields = "__all__"
        fields = ["username","password"]

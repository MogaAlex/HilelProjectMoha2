
from django.contrib.auth.forms import UserCreationForm
from .models import ExampleUser

class ExampleUserCreationForm(UserCreationForm):
    class Meta:
        model = ExampleUser
        fields = ('email', 'first_name', 'last_name')
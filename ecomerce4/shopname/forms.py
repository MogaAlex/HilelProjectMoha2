from django import  forms
from shopname.orders.models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',

        ]
    widgets = {
        'address': forms.TextInput(attrs={'rows':3}),
    }

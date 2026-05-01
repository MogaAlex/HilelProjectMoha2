import pytest
from shopname.forms import OrderCreateForm

class TestOrderCreateForm:
    def test_form_is_valid(self):
        data = {
            'first_name': 'John',
            'last_name': 'Watson',
            'email': 'Bakerstreet@gmail.com',
            'phone_number': '380990000',
            'address': 'London'
        }
        form = OrderCreateForm(data=data)
        assert form.is_valid()

    def test_form_invalid_email(self):
        data = {'email': 'not-an-email'}
        form = OrderCreateForm(data=data)
        assert not form.is_valid()
        assert 'email' in form.errors

    def test_address_widget_attributes(self):
        form = OrderCreateForm()
        assert form.fields['address'].widget.attrs['rows'] == 3
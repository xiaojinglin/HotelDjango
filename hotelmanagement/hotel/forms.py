from django import forms
from hotel.models import Customers


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['firstname', 'lastname', 'phone']
    def clean(self):
        super(CustomerForm, self).clean()
        phone = self.cleaned_data.get('phone')
        if len(phone)!=10:
            self.errors['phone'] = self.error_class(['Enter valid phone number eg:5022222222'])
        return self.cleaned_data
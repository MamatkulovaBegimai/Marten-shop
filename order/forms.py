from django import forms
from order.models import BillingInformation, ShippingInformation, ShippingMethod, PaymentInformation, CreditCard

class BillingInformationForm(forms.ModelForm):
    class Meta:
        model = BillingInformation
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'state', 'zip_code', 'phone_number']


class ShippingInformationForm(forms.ModelForm):
    class Meta:
        model = ShippingInformation
        fields = ['address', 'phone_number']


class ShippingMethodForm(forms.ModelForm):
    class Meta:
        model = ShippingMethod
        fields = ['name', 'price']


class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['card_name', 'card_type', 'card_number', 'expiration_month', 'expiration_year', 'cvv']

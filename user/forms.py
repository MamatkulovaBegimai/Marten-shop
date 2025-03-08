from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import CustomUser

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput, help_text="Введите пароль")
    password2 = forms.CharField(label="Пароль", widget=forms.PasswordInput, help_text="Введите пароль ещё раз для подтверждения")

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


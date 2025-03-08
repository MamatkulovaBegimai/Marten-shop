from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from user.forms import RegistrationForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView



class RegisterView(FormView):
    template_name = 'login-register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Регистрация прошла успешно!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Исправьте ошибки в форме')
        return super().form_invalid(form)


class MyAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'my-account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_form = kwargs.get('user_form') or UserProfileForm(instance=self.request.user)
        password_form = kwargs.get('password_form') or PasswordChangeForm(user=self.request.user)
        context.update({
            'user_form': user_form,
            'password_form': password_form,
            'user': self.request.user
        })
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
        if 'update_profile' in request.POST:
            user_form = UserProfileForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Профиль успешно обновлен!')
                return redirect('account')
            else:
                messages.error(request, 'Исправьте ошибки')
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save(commit=False)
                user.set_password(password_form.cleaned_data['new_password1'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно обновлен!')
                return redirect('account')
            else:
                messages.error(request,
                               'Исправьте ошибки при смене пароля')

        return self.render_to_response(self.get_context_data(user_form=user_form, password_form=password_form))



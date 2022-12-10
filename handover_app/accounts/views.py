from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.contrib.auth import login
from django.shortcuts import redirect
from .models import User


class Login(LoginView):

    form_class = LoginForm
    template_name = 'accounts/login.html'


class Logout(LoginRequiredMixin, LogoutView):

    template_name = 'accounts/login.html'


def GuestLogin(request):
    guest_user = User.objects.get(username='guest')
    login(request, guest_user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('handover:top')






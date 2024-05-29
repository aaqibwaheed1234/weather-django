from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from .forms import RegisterForm
from django.urls import reverse_lazy, reverse
# Create your views here.
User=get_user_model


class SignUpView(CreateView):
    template_name="registration/signup.html"
    model=User
    form_class= RegisterForm
    success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("login"))
        return super().get(request, *args, **kwargs)
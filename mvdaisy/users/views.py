from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy


class LoginUser(LoginView):
    extra_context = {"tite": "Вход"}
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("expert_list")


class LogoutUser(LogoutView):
    def get_success_url(self):
        return reverse_lazy("main:index")



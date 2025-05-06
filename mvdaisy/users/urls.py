from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import LoginUser, LogoutUser



app_name = "users"
urlpatterns = [
    path("login/", LoginUser.as_view(), name="login_user"),
    # path("logout/", LogoutView.as_view(next_page='login_user'), name="logout_user"),
    path("logout/", LogoutUser.as_view(), name="logout_user"),


]
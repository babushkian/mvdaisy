from django.urls import path
from expertizes.views import index

app_name = "expertizes"
urlpatterns = [
    path("", index, name="index"),
]
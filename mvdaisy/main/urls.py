from django.urls import path
from main.views import ExpertListView, RanksView

app_name = "main"
urlpatterns = [
    path("", ExpertListView.as_view(), name="index"),
    path("ranks/", RanksView.as_view(), name="ranks"),
]
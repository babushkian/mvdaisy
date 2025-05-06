from django.urls import path

from expert.views import (
    ExpertView,
    AddExpertView,
    ExpertListView,
    EditExpertView,
    ExpertDelete,
    custom_edit_expert,
    laboratory_edit,
    LabsListView,
    LabEditView,
    CustomCreateExpert,
)
app_name = "expert"
urlpatterns = [
    path("", ExpertListView.as_view(), name="expert_list"),
    path("add_expert/", AddExpertView.as_view(), name="expert_add"),
    path("edit_expert/<int:pk>/", EditExpertView.as_view(), name="expert_edit"),
    path("expert/<int:pk>/", ExpertView.as_view(), name="expert"),
    path("expert_delete/<int:pk>/", ExpertDelete.as_view(), name="expert_delete"),
    path("custom_edit/", CustomCreateExpert.as_view(), name="custom_edit"),
    path("laboratory_edit/", laboratory_edit, name="laboratory_edit"),
    path("labs/", LabsListView.as_view(), name="labs"),
    path("lab_edit/<int:pk>/", LabEditView.as_view(), name="lab_edit"),


]

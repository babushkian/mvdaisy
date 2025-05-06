
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.db.models import Window, Count, ProtectedError, OuterRef, Subquery, Prefetch
from django.db.models.functions import RowNumber
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, UpdateView, ListView, DeleteView, CreateView
from django.forms.models import model_to_dict
from django.core.handlers.wsgi import WSGIRequest
from django.utils.timezone import make_aware

from users.models import Expert
from main.models import RankAndType, RankType, Rank
from expert.models import ExpertLaboratory, ExpertExpertiseArea, Laboratory, ExpertiseArea
from expert.forms import RankTypeLink, ExpertForm, PermissionLaboratoryFormSet


def index(request):
    return HttpResponse("Начало разработки")


class ExpertListView(ListView):
    model = Expert
    template_name = "expert/expert_list.html"
    extra_context = {"active": "experts"}

    def get_queryset(self):
        return Expert.objects.select_related("rank", "rank_type", "position")


class AddExpertView(CreateView):
    model = Expert
    template_name = "expert/expert_add.html"
    fields = ["username", "last_name", "first_name", "second_name",  "sex",  "birth_date",  "rank", "rank_type", "position"]
    success_url = reverse_lazy("experts:expert_list")



class EditExpertView(UpdateView):
    model = Expert
    template_name = "expert/expert_add.html"
    fields = ["last_name", "first_name", "second_name", "sex", "birth_date", "rank", "rank_type", "position"]
    success_url = reverse_lazy("experts:expert_list")

    def get(self, request, *args, **kwargs):
        print("anus")
        return super().get(request, *args, **kwargs)


class ExpertView(DetailView):
    model = Expert
    template_name = "expert/expert_datail.html"


    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = (
            self.model.objects
            .filter(pk=pk)
            .select_related("rank", "rank_type", "position")
        )
        perm_rel = Prefetch("expert_expertisearea",
                            queryset=ExpertExpertiseArea.objects.select_related("expertisearea"))
        lab_rel = Prefetch("expert_laboratory", queryset=ExpertLaboratory.objects.select_related("laboratory"))
        obj = obj.prefetch_related(perm_rel, lab_rel)
        obj = obj.first()
        return obj

    def _table_with_header(self, parent, child:str, title:str=""):
        table = {"title": f"{title.capitalize()}:",
                 "header": {"name": "Название", "start_date": "Начало", "end_date": "Конец"}
        }
        data = []
        for item in parent.all():
            item_dict = {"name": getattr(item, child).name, "start_date":item.start_date, "end_date": item.end_date}
            data.append(item_dict)
        table["data"] = data
        return table


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expert = {
            "fio": f"{self.object.last_name} {self.object.first_name} {self.object.second_name}",
            "sex": "мужской" if self.object.sex else "женский",
            "rank": f"{self.object.rank.name} {self.object.rank_type.name}",
            "position": self.object.position.name,
        }

        laboratories = self._table_with_header(self.object.expert_laboratory, "laboratory", "лаборатории")
        permissions = self._table_with_header(self.object.expert_expertisearea, "expertisearea", "допуска")
        context.update({"expert": expert, "laboratories": laboratories, "permissions": permissions})
        return context




class ExpertDelete(DeleteView):
    model = Expert
    success_url = reverse_lazy("experts:expert_list")
    template_name = "expert/expert_delete.html"


def custom_edit_expert(request):
    form = ExpertForm()
    context = {"form": form}
    return render(request, "expert/expert_custom_edit.html", context)


class CustomCreateExpert(CreateView):
    model = Expert
    form_class = ExpertForm

    template_name = "expert/expert_custom_edit.html"
    success_url = reverse_lazy("experts:expert_list")



def laboratory_edit(request):
    """
    Здесь можно реализовать ввод через Formset: в одной лвборатории несколько направлений
    :param request:
    :return:
    """
    lab = Laboratory.objects.get(pk=2)
    if request.method =="POST":
        formset = PermissionLaboratoryFormSet(request.POST, instance=lab)
        if formset.is_valid():
            formset.save()
            return redirect("expert_list")
    else:
        formset = PermissionLaboratoryFormSet(instance=lab)
    context = {"formset": formset, "laboratory": lab}
    return render(request, "expert/laboratory_edit.html", context=context)

class LabsListView(ListView):
    extra_context = {"active": "laboratories"}
    template_name = "expert/labs.html"
    model = Laboratory

class LabEditView(DetailView):
    template_name = "expert/lab_edit.html"

    def get_queryset(self):
        pk = self.kwargs['pk']
        # query = Laboratory.objects.filter(pk=pk).prefetch_related("experts")
        query = Laboratory.objects.prefetch_related(Prefetch("experts", queryset=Expert.objects.distinct()), "expertiseareas")
        return query
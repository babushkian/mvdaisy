from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, TemplateView
from django.db.models import OuterRef, Subquery, Exists
from users.models import Expert
from expert.models import ExpertLaboratory, Laboratory

class ExpertListView(ListView):
    model = Expert
    template_name = "main/index.html"
    extra_context = {"active": "main"}

    def get_queryset(self):
        expert_labs =  (ExpertLaboratory.objects.
                        filter(end_date__isnull=True)
                        .select_related("expert", "laboratory")
                        .order_by("laboratory__name", "expert__last_name")
                        .all()
                        )
        return expert_labs


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        experts={}
        for i in self.object_list:
            if experts.get(i.expert):
                experts[i.expert].append(i.laboratory)
            else:
                experts[i.expert] = [i.laboratory]
        expert_strings=[]
        for ex in experts:
            expert_strings.append({
                "expert": str(ex) + " (" + ", ".join(map(lambda x: x.name, experts[ex])) + ")",
                "username": ex.username
            })
        context["experts"] = expert_strings
        return context


class RanksView(TemplateView):
    template_name = "main/ranks.html"
    extra_context = {"active": "ranks"}
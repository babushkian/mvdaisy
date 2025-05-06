from django.contrib import admin

from django import forms
from django.contrib import admin
from main.models import Rank, RankType, RankAndType,  Position
from .models import Laboratory, ExpertiseArea, ExpertExpertiseArea, ExpertLaboratory



class ExpertLaboratoryInline(admin.TabularInline):
    model = ExpertLaboratory
    extra = 0


class ExpertiseAreaInlineForm(forms.ModelForm):
    class Meta:
        model = ExpertiseArea
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.Select(choices=self.get_department_choices())

    @staticmethod
    def get_department_choices():
        # Получаем список всех кафедр из базы для выпадающего списка
        departments = ExpertiseArea.objects.values_list('name', flat=True).distinct()
        return [(department, department) for department in departments]

class ExpertiseAreaLaboratoryInline(admin.TabularInline):
    model = ExpertiseArea
    form = ExpertiseAreaInlineForm
    extra = 0
    can_delete = True

class RankAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ["id", "name"]
    list_editable = ["name"]
    ordering = ["id"]

class RankAndTypeAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ["id", "type", "rank" ]
    list_editable = ["rank", "type"]
    ordering = ["type"]

    class Meta:
        model = RankAndType


class ExpertExpertiseAreaAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ["id", "expert", "expertisearea",  "start_date", "end_date"]
    ordering = ["id"]




class LaboratoryAdmin(admin.ModelAdmin):
    inlines = [ExpertiseAreaLaboratoryInline, ExpertLaboratoryInline]
    save_on_top = True
    list_display = ["id", "name"]
    list_editable = ["name"]
    ordering = ["id"]

    class Meta:
        model = Laboratory

class ExpertiseAreaAdmin (admin.ModelAdmin):
    save_on_top = True
    list_display = ["id", "name", "laboratory"]
    ordering = ["id"]

admin.site.register(Rank, RankAdmin)
admin.site.register(RankType, RankAdmin)
admin.site.register(RankAndType, RankAndTypeAdmin)
admin.site.register(Position, RankAdmin)
admin.site.register(Laboratory, LaboratoryAdmin)



admin.site.register(ExpertiseArea, ExpertiseAreaAdmin)
admin.site.register(ExpertExpertiseArea, ExpertExpertiseAreaAdmin)





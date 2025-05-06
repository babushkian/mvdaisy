from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Expert

from expert.models import ExpertExpertiseArea, ExpertLaboratory


class ExpertLaboratoryInline(admin.TabularInline):
    model = ExpertLaboratory
    extra = 0
class ExpertExpertiseAreaInline(admin.TabularInline):
    model = ExpertExpertiseArea
    extra = 0

class ExpertAdmin(UserAdmin):
    inlines = [ExpertLaboratoryInline, ExpertExpertiseAreaInline]
    save_on_top = True
    list_display = ["id", "last_name", "first_name", "second_name", "rank", "rank_type", "position", "sex", "working"]
    list_editable = ["last_name", "first_name", "second_name", "rank", "rank_type", "position", "sex", "working"]
    ordering = ["id"]
    fieldsets = (
        ("Имя", {
            "fields": ("username", "last_name", "first_name", "second_name", "sex", "birth_date")
        }),
        ("Звание и должность", {
            "fields": ("rank", "rank_type", "position", "working")
        })
    )

    class Meta:
        model = get_user_model()


# admin.site.register(Expert, UserAdmin)
admin.site.register(Expert, ExpertAdmin)


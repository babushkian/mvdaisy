from django import forms
from django.forms import inlineformset_factory
from main.models import Rank, RankType
from expert.models import Laboratory, ExpertiseArea
from users.models import Expert



class RankTypeLink(forms.Form):
	type_qs = RankType.objects.all()
	type = forms.ModelChoiceField(type_qs, label="Тип звания")

	rank_qs = Rank.objects.all()
	rank = forms.ModelChoiceField(rank_qs, label="Звание")


class ExpertForm(forms.ModelForm):

	class Meta:
		model = Expert
		fields = ["first_name", "second_name", "last_name", "sex", "working", "rank", "rank_type", "position",]


class ExpertiseAreaForm(forms.ModelForm):
	name = forms.ModelChoiceField(ExpertiseArea.objects.all())
	class Meta:
		model = ExpertiseArea
		fields = ["name"]



PermissionLaboratoryFormSet = inlineformset_factory(Laboratory, ExpertiseArea, form=ExpertiseAreaForm, fields=("name",), extra=3, can_delete=True)


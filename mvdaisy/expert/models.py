from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

Expert = get_user_model()


class Laboratory(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название лаборатории")
	experts = models.ManyToManyField(Expert, related_name='laboratories', through="ExpertLaboratory")

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse_lazy("experts:lab_edit", kwargs={'pk': self.pk})

	class Meta:
		verbose_name = "Лаборатория"
		verbose_name_plural = "Лаборатории"


class ExpertiseArea(models.Model):
	name = models.CharField(max_length=100, verbose_name="Название допуска")
	experts = models.ManyToManyField(Expert, through="ExpertExpertiseArea", related_name="expertiseareas")
	laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name="expertiseareas")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Допуск"
		verbose_name_plural = "Допуска"


class ExpertExpertiseArea(models.Model):
	expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name="expert_expertisearea")
	expertisearea = models.ForeignKey(ExpertiseArea, on_delete=models.CASCADE, related_name="expert_expertisearea")
	start_date = models.DateField(null=True, blank=True,  verbose_name="Дата начала допуска")
	end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания допуска")

	class Meta:
		verbose_name = "Эксперт-допуск"
		verbose_name_plural = "Эксперт-допуск"


class ExpertLaboratory(models.Model):
	expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name="expert_laboratory")
	laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name="expert_laboratory")
	start_date = models.DateField(null=True, blank=True, verbose_name="Начало работы в лаборатории")
	end_date = models.DateField(null=True, blank=True,  verbose_name="Конец работы в лаюоратории")


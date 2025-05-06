from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from main.models import Rank, RankType, Position

class Expert(AbstractUser):
	first_name = models.CharField(max_length=100, verbose_name="Имя")
	second_name = models.CharField(max_length=100, verbose_name="Отчество")
	last_name = models.CharField(max_length=100, verbose_name="Фамилия")
	sex = models.BooleanField(choices=[(True, "мужской"), (False, "женский")], null=True, verbose_name="Пол")
	working = models.BooleanField(choices=[(True, "да"), (False, "нет")], default=True,
								  verbose_name="Действующий сотрудник")
	employment_datetime = models.DateField(null=True, blank=True, verbose_name="Дата начала работы")
	dismiss_date = models.DateField(null=True, blank=True, verbose_name="Дата увольнения")
	birth_date = models.DateField(null=True, blank=True, verbose_name="День рождения")


	rank = models.ForeignKey(Rank, on_delete=models.CASCADE, default=9, verbose_name="Звание") # вольный найм
	rank_type = models.ForeignKey(RankType, on_delete=models.CASCADE, default=6 , verbose_name="Тип звания") # гражданский
	position = models.ForeignKey(Position, on_delete=models.CASCADE, default=1, verbose_name="Должность")


	def get_absolute_url(self):
		return reverse_lazy("experts:expert", kwargs={"pk": self.pk})

	def __str__(self):
		return self.last_name + " " + self.first_name + " " + self.second_name

	class Meta:
		verbose_name = "Эксперт"
		verbose_name_plural = "Эксперты"


from django.db import models
from django.db.models import UniqueConstraint


class Rank(models.Model):
	"""
	Звание: майор, лейтенант, служащий
	"""
	name = models.CharField(max_length=100, verbose_name="Имя")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Звание"
		verbose_name_plural = "Звания"


class RankType(models.Model):
	"""Тип звания: полиции, юстиции, внутренней службы """
	name = models.CharField(max_length=100, verbose_name="Имя")
	ranks = models.ManyToManyField(Rank, related_name="types", through="RankAndType")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Тип звания"
		verbose_name_plural = "Типы званий"


class RankAndType(models.Model):
	rank = models.ForeignKey(Rank, on_delete=models.PROTECT, related_name="linked_type")
	type = models.ForeignKey(RankType, on_delete=models.PROTECT, related_name="linked_rank")

	class Meta:
		constraints = [
			UniqueConstraint(fields=("rank", "type"), name='rank_type_constraint')
		]

	def __str__(self):
		return self.rank.name + " " + self.type.name


class Position(models.Model):
	"""Должность"""
	name = models.CharField(max_length=100, verbose_name="Имя")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Должность"
		verbose_name_plural = "Должности"


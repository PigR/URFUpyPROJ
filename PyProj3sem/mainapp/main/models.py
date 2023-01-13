from django.db import models

# Create your models here.

# Графики динамики зарплат по годам
class Charts(models.Model):
	title = models.CharField("Название", max_length=128)
	chart = models.ImageField(upload_to="images/charts")

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "График"
		verbose_name_plural = "Все графики"



#==================================Вкладка О профессии==================================
class ContentAbout(models.Model):
	title = models.CharField("Название", max_length=50)
	content = models.TextField("Информация")
	image = models.ImageField("Изображение", upload_to="images/")

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Контент"
		verbose_name_plural = "О профессии"
# ========================================================================================

#==================================Вкладка Востребованность==================================
# Динамика зарплат по годам
class TableSalaryYear(models.Model):
	currencies = (
		("BYR", "BYR"), ("RUR", "RUR"), 
		("USD", "USD"), ("EUR", "EUR"), 
		("KZT", "KZT"), ("UAH", "UAH"), 
		("UZS", "UZS")
	)

	currency = models.CharField("Валюта", max_length=128, choices=currencies)
	year = models.PositiveIntegerField("Год")
	salary = models.FloatField("Зарплата", default=0)

	def __str__(self):
		return self.currency

	class Meta:
		verbose_name = "Строку"
		verbose_name_plural = "Динамика зарплат по годам (backend-разработчик)"


class TablesVacanciesYears(models.Model):
	year = models.PositiveIntegerField("Год")
	vacanсies = models.PositiveIntegerField("Кол-во вакансий")

	class Meta:
		verbose_name = "Строку"
		verbose_name_plural = "Динамика кол-ва вакансий по годам (backend-разработчик)"
# ==============================================================================================

#==================================Вкладка География==================================

class TableVacanciesInCityYear(models.Model):
	title = models.CharField("Город", max_length=128)
	year = models.PositiveIntegerField("Год")
	salary = models.FloatField("Зарплата", default=0)

	class Meta:
		verbose_name = "Строку"
		verbose_name_plural = "Динамика зарплат в разных городах по годам (backend-разработчик)"


# ====================================================================================

#==================================Вкладка Навыки==================================

class TableSkillsInYear(models.Model):
	year = models.PositiveIntegerField("Год")
	title = models.CharField("Название навыка", max_length=256)
	counter = models.PositiveIntegerField("Кол-во вакансий с этим навыком")

	class Meta:
		verbose_name = "Строку"
		verbose_name_plural = "Топ-10 навыков в году"

# =================================================================================
from .models import ContentAbout, Charts, TableSalaryYear, TablesVacanciesYears, TableVacanciesInCityYear, TableSkillsInYear

from django.shortcuts import render

from datetime import date
import requests
import json

def index(request):
	return render(request, "main/index.html", {"article": ContentAbout.objects.all()})


def demand(request):
	#получаем графики из бд
	salary_year_charts_backend = dict()
	for item in Charts.objects.all():
		if item.title == "qnt_vacancies_year":
			qnt_vacancies_year_chart_backend = item.chart.url
		else:
			salary_year_charts_backend[item.title] = item.chart.url
	
	#таблица динамики зарпла по годам (бэкэнд-разработчик)
	salary_year_backend = dict()
	for item in sorted([(item.currency, item.year, item.salary) for item in TableSalaryYear.objects.all()], key=lambda pack: pack[1]):
		if salary_year_backend.get(item[0], None) is None:
			salary_year_backend.setdefault(item[0], {item[1]: item[2], "chart": salary_year_charts_backend[item[0]]})
		else:
			salary_year_backend[item[0]][item[1]] = item[2]

	# таблица кол-ва вакансий по годам (бэкэнд-разработчик)
	qnt_vacancies_year_backend = {item.year: item.vacanсies for item in TablesVacanciesYears.objects.all()}
	
	return render(request, "main/demand.html", {
			"salary_year_backend": salary_year_backend.items(),
			"qnt_vacancies_year_backend": sorted(qnt_vacancies_year_backend.items(), key=lambda pack: pack[0]),
			"qnt_vacancies_year_chart_backend": qnt_vacancies_year_chart_backend
		})


def geography(request):
	
	# вот эта дич берёт json и загружает его в бд в виде строк
	# with open("top_10_city_on_qnt_vacans.json", encoding="utf-8") as file:
	# 	data = json.load(file)

	# for city, pack in data:
	# 	for year, item in sorted(pack.items(), key=lambda pack: pack[0]):
	# 		row = TableVacanciesInCityYear(title=city, year=year, salary=item["middle_salary_vacancies"])
	# 		row.save()
	
	years = (year for year in range(2010, 2022, 1))
	salary_city_charts_backend, tables = {item.title: item.chart.url for item in Charts.objects.all()}, dict()
	for item in TableVacanciesInCityYear.objects.all():
		if item.title not in ("qnt_vacancies_year", "RUR", "EUR", "USD", "KZT", "BYR", "UAH", "UZS"):
			if tables.get(item.title, None) is None:
				tables.setdefault(item.title, dict()).setdefault(item.year, item.salary)
				tables[item.title].setdefault("chart", salary_city_charts_backend[item.title])
			else:
				tables[item.title][item.year] = item.salary
	
	return render(request, "main/geography.html", {"tables": tables.items()})


def skills(request):
	# вот эта дич берёт json и загружает его в бд в виде строк
	# with open("top_10_skills_in_year.json", encoding="utf-8") as file:
	# 	data = json.load(file)
	
	# for year, skills in data.items():
	# 	for skill, qnt in skills.items():
	# 		row = TableSkillsInYear(year=year, title=skill, counter=qnt)
	# 		row.save()

	skills_charts_backend = {item.title: item.chart.url for item in Charts.objects.all() if item.title.split('_')[0] == "skills"}

	tables = dict()
	for item in TableSkillsInYear.objects.all():
		tables.setdefault(( (item.year, skills_charts_backend[f"skills_{item.year}"]), (1, 2) ), list()).append( (item.title, item.counter) )

	return render(request, "main/skills.html", {
			"tables": tables.items(), 
			"skills": tables,
		})


#HH API
def latest_vacancies(request):
	

	def remove_html_tags(text: str) -> str:
		"""удаляет html теги из текста"""
		result = str()
		for word in text.split():
			for html_tag in ["<highlighttext>", "</highlighttext>"]:
				if html_tag in word:
					word = "\n".join(word.split(html_tag))
				else:
					word = "\n" + word
			result += word
		return result


	url = "http://api.hh.ru/vacancies?clusters=true&only_with_salary=true&enable_snipprts=true&st=searchVacancy" \
				"&text=backend+OR+бэкэнд+OR+бекэнд+OR+бэкенд+OR+бекенд+OR+back end+OR+бэк энд+OR+бэк енд+OR+django+"\
				"OR+flask+OR+laravel+OR+yii+OR+symfony&search_field=name&per_page=100&area=1"
	
	salary = int()
	data, result = requests.get(url, timeout=5).json(), list()
	for item in data["items"]:
		now_date = date.today()
		published_at = date.fromisoformat(item["published_at"].split("T")[0])
		if (published_at.weekday() not in(6, 7)) and (now_date.toordinal() > published_at.toordinal()):
			if item["snippet"]["responsibility"] and item["snippet"]["requirement"] and item["employer"]["name"] \
				and (item["salary"]["from"] not in [0 , None] or item["salary"]["to"] not in [0, None]) \
					and item["salary"]["currency"] and item["area"]["name"]:

				if item["salary"]["from"] and item["salary"]["to"]:
					salary = round( (item["salary"]["to"] + item["salary"]["to"])  / 2)
				elif item["salary"]["to"] and not item["salary"]["to"]:
					salary = item["salary"]["to"]
				elif not item["salary"]["to"] and item["salary"]["to"]:
					salary = item["salary"]["to"]
				
				# print(salary)
				if salary:
					result.append({
						"title": item["name"],
						"description": remove_html_tags(text=item["snippet"]["responsibility"]),
						"skills": remove_html_tags(text=item["snippet"]["requirement"]),
						"company": item["employer"]["name"],
						"salary": salary,
						"currency": item["salary"]["currency"],
						"city": item["area"]["name"],
						"published_at": item["published_at"].split("T")[0], 
					})
				##print(result)
	
	return render(request, "main/latest_vacancies.html", {
			"vacancies": sorted(result, key=lambda pack: date.fromisoformat(pack["published_at"]))
		})


import csv
from datetime import date
from functools import reduce

import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np
import pandas as pd
import json


def get_csv_data(unload_from: str) -> list:
	# принимает имя csv файла и получает его содержимое в виде списка словарей
	with open(unload_from, encoding="utf-8") as file:
		data = list(csv.DictReader(file))
	return data


def vacancies_sort_backend(data: list, load_to: str, word_variants: list, key_sorted: str) -> None:
	# проверяет названия вакансий на наличие конкретных слов
	# принимает список словарей, имя файла в который будет сохранён результат, слова сортировки и ключ сортировки
	# создаёт файл с результатом
	
	result = list()
	# сортировка
	for item in data:
		for check in word_variants:
			if check in item[key_sorted]:
				result.append(item)

	# упаковка
	with open(load_to, "w", encoding="utf-8", newline="") as file:
		writer = csv.DictWriter(file, fieldnames=result[0].keys())
		writer.writeheader()
		for item in result:
			writer.writerow(item)

	print("Файл отсортирован!")


def create_chart_salary_year_backend(data: list) -> None:
	# строит график уровня зарплат по годам
	# принимает список словарей

	salary_year = list() #список кортежей (средняя зарплата) / год
	# отсекает вакансии где не указана зарплата
	for item in data:
		salary_vacancies = float()
	
		if item["salary_from"] or item["salary_to"]: #если они есть
			if item["salary_from"] and item["salary_to"]:
				salary_vacancies = ( float(item["salary_from"]) + float(item["salary_to"]) ) / 2
			elif item["salary_from"] and not item["salary_to"]:
				salary_vacancies = float(item["salary_from"])
			elif not item["salary_from"] and item["salary_to"]:
				salary_vacancies = float(item["salary_to"])

			status_salary = True
		else:
			status_salary = False

		if status_salary: #если нету зарплаты то скипаем вакансию
			published = date.fromisoformat(item["published_at"].split("T")[0]).year
			salary_year.append( (salary_vacancies, item["salary_currency"], published) )
	
	amount_year_qty = dict() #где ключ - это кортеж (год/валюта), 
	# а значение словарь - сумма всех зарплат(одного типа валюты) за год и кол-во вакансий
	# суммирует зарплаты вакансий и их кол-во за все года
	for pack in sorted(salary_year, key=lambda pack: pack[2]):
		salary_vacancies, currency, published = pack

		if amount_year_qty.get( (published, currency), None) is None:
			amount_year_qty.setdefault( (published, currency), {
					"salary": salary_vacancies, 
					"quan": 1,
				})
		else:
			amount_year_qty[(published, currency)]["salary"] += salary_vacancies
			amount_year_qty[(published, currency)]["quan"] += 1

	# получаем словарь год/средняя зарплата
	proto_coords = {key: round(value["salary"] / value["quan"], 2) for key, value in amount_year_qty.items()}
	currencies = sorted(list({key[1] for key, value in proto_coords.items()}))
	years = sorted(list({key[0] for key, value in proto_coords.items()}))

	proto_coords_2 = dict()
	# короче эта часть нужна чтобы заполнить нулями те валюты которые есть не во всех годах(это нужно для графика)
	for year in years: #идём по годам
		for valuta in currencies: #идём по валютам
			if proto_coords.get( (year, valuta), None ) is None:
				proto_coords_2[ (year, valuta) ] = 0
			else:
				proto_coords_2[ (year, valuta) ] = proto_coords[ (year, valuta) ]
	
	for valuta in currencies:
		salary_year = filter(lambda pack: True if pack[0][1] == valuta else False, proto_coords_2.items())
		salary_year = [value for key, value in sorted(salary_year, key=lambda pack: pack[0][0])]
		plt.title(f"Динамика уровня зарплат по годам. Валюта - {valuta}")
		plt.xlabel("Год")
		plt.ylabel("Зарплата")
		plt.bar(years, salary_year)
		plt.show()	
	print("Графики построены!")

	table = dict()
	for key, value in proto_coords_2.items():
		table.setdefault(key[1], list()).append([key[0], round(value)])

	column = ["Год", "Зарплата"]
	for key, value in table.items():
		print(key)
		print(tabulate(value, headers=column, tablefmt="fancy_grid"))
	print("Таблицы построены!")


def create_chart_vacansies_year_backend(data: list) -> None:
	# строит график и таблицу динамики кол-ва вакансий по годам
	# берём только те вакансии у которых указан год публикации
	vacancies_with_date = [item for item in data if item["published_at"]] #список словарей
	years = sorted({date.fromisoformat(item["published_at"].split("T")[0]).year for item in vacancies_with_date}) #получаем года через множество
	
	counter = dict.fromkeys(years, 0)
	for item in vacancies_with_date: #считаем число вакансий по годам
		year = date.fromisoformat(item["published_at"].split("T")[0]).year
		counter[year] = counter.get(year, 0) + 1

	plt.title("Динамика кол-ва вакансий по годам")
	plt.xlabel("Год")
	plt.ylabel("Число вакансий")
	plt.bar(counter.keys(), counter.values())
	plt.show()	
	print("Графики построены!")

	print(counter)
	print(tabulate(counter.items(), headers=("Год", "Число вакансий"), tablefmt="fancy_grid"))
	print("Таблицы построены!")


def vacancies_sort_backend_with_city(data: list) -> list:
	# отсекает те вакансии бэкэндеров у которых не указан город, год публикации и зарплата
	return [item for item in data if (item["area_name"] and item["published_at"]) and (item["salary_from"] or item["salary_to"])]


def create_chart_salary_city_backend(data: list) -> None:
	# строит графики и таблицы зарплаты по годам, и городам
	salary_city = dict()
	for item in data:
		#рассчитываем среднюю зарплату(в списке data она есть у любой вакансии 100%)
		if item["salary_from"] and item["salary_to"]:
			salary_vacancies = ( float(item["salary_from"]) + float(item["salary_to"]) ) / 2
		elif item["salary_from"] and not item["salary_to"]:
			salary_vacancies = float(item["salary_from"])
		elif not item["salary_from"] and item["salary_to"]:
			salary_vacancies = float(item["salary_to"])

		year = date.fromisoformat(item["published_at"].split("T")[0]).year #дата публикации

		if item["area_name"] not in ("Россия", "Германия", "США", "Япония", "Кипр", "Таиланд" "Доминиканская Республика", "Канада", "Израиль"): #Я не знаю что делать с этим..
			if ( salary_city.get( item["area_name"], None ) is None ) or ( salary_city.get( item["area_name"], None ).get(year, None) is None ):		
				salary_city.setdefault(item["area_name"], dict()).setdefault(year, {
						"middle_salary_vacancies": salary_vacancies,
						"counter": 1, #если есть несколько вакансий в одном городе в ту же дату, то нужно вычислить сред. зп через counter
					})
			else:
				middle_salary_old = salary_city[item["area_name"]][year]["middle_salary_vacancies"]
				quan_vacancies = salary_city[item["area_name"]][year]["counter"]
				#формула считает ср. арифм. через старое значение ср. арифм. раньше бы её откопать...
				middle_salary_new = round(( ( middle_salary_old * quan_vacancies ) + salary_vacancies) / (quan_vacancies + 1), 2)

				salary_city[item["area_name"]][year]["middle_salary_vacancies"] = middle_salary_new
				salary_city[item["area_name"]][year]["counter"] += 1

	#очередное заполнение нулями тех годов в которые нету вакансий в некоторых городах
	years = sorted({date.fromisoformat(item["published_at"].split("T")[0]).year for item in data})
	for city, values in dict(salary_city).items():
		for year in years:
			if salary_city[city].get(year, None) is None:
				salary_city[city].setdefault(year, {
						"middle_salary_vacancies": 0,
						"counter": 0
					})

	# это чудо отбирает 10 городов с самым большим числом вакансий(слишком их уж много)
	top_10_city_on_qnt_vacans = sorted( salary_city.items(), key=lambda city: reduce( lambda start, item: start + item[1]["counter"], city[1].items(), 0), reverse=True )[0:11]

	cities = tuple(salary_city.keys())
	index = np.arange(12)
	plt.xlabel("Год")
	plt.ylabel("Зарплата")
	
	#строим графики
	chart_frame = dict()
	for pack in top_10_city_on_qnt_vacans:
		city, value = pack
		print(value)
		chart_frame[city] = [item["middle_salary_vacancies"] for item in value.values()]
		plt.title(f"Зарплаты в городе {city} по годам")
		df = pd.DataFrame(chart_frame)
		df.plot(kind="bar")
		plt.xticks(index, years)
		del chart_frame[city]

		plt.show()
	print("Графики построены!")

	#строим таблицы
	for city, pack in top_10_city_on_qnt_vacans:
		table = {year: round(item["middle_salary_vacancies"]) for year, item in sorted(pack.items(), key=lambda elem: elem[0]) }
		print(f"Город - {city}")
		print(tabulate(table.items(), headers=("Год", "Зарплата"), tablefmt="fancy_grid"))
	print("Таблицы построены!")

	with open("top_10_city_on_qnt_vacans.json", 'w', encoding="utf-8") as file:
		json.dump(top_10_city_on_qnt_vacans, fp=file, indent=2, ensure_ascii=False)


def create_chart_table_skills_backend(data: list) -> None:
	# строит график и таблицу самых популярных навыков

	#отбираем только те вакансии в которых указаны навыки и год публикации и считаем все варинты навыков	
	skills_counter = dict()
	for item in list(filter(lambda pack: True if pack["key_skills"] else False, data)):
		year = date.fromisoformat(item["published_at"].split("T")[0]).year
		skills_counter.setdefault(year, dict())
		for skill in item["key_skills"].split('\n'):	
			skills_counter[year][skill] = skills_counter[year].get(skill, 0) + 1

	# отбираем 10 навыком с самым большим счётчиком в каждом году
	top_10_skills = dict()
	for year, skills in skills_counter.items():
		top_10_skills.setdefault(year, dict())
		for _, skill_count in zip(range(10), sorted(skills.items(), key=lambda pack: pack[1], reverse=True)):
			skill, count = skill_count
			top_10_skills[year][skill] = count

	# строим графики
	for year, top_10_skills_in_year in top_10_skills.items():
		index = np.arange(10)
		plt.title(f"Топ-10 самых популярных навыков за {year} год")
		plt.xlabel("Навык")
		plt.ylabel("Вакансий с навыком")
		df = pd.DataFrame(sorted(top_10_skills_in_year.items(), key=lambda pack: pack[1]))
		df.plot(kind="barh")
		plt.yticks(index, top_10_skills_in_year.keys())

		plt.show()
	print("Графики построены!")

	#лучше запилим json чем таблицу
	with open("top_10_skills_in_year.json", 'w', encoding="utf-8") as file:
		json.dump(top_10_skills, fp=file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
	# получение нужных вакансий (backend-разработчик)
	# word_variants =	["backend", "бэкенд", "бекенд", "бекэнд", "back end", "бэк энд", "бэк енд", "django", "flask", "laravel", "yii", "symfony"]
	# vacancies_sort_backend(data=get_csv_data(unload_from="vacancies_with_skills.csv"), load_to="result_sorted.csv", word_variants=word_variants, key_sorted="name")
	
	# построение графиков и таблиц зарплат по годам (backend-разработчик)
	# data = get_csv_data(unload_from="result_sorted.csv")
	# create_chart_salary_year_backend(data=data)
	
	# построение графиков и таблиц числа вакансий по годам (backend-разработчик)
	# data = get_csv_data(unload_from="result_sorted.csv")
	# create_chart_vacansies_year_backend(data=data)

	# построение графиков и таблиц уровня зарплаты по городам, и городам
	# data = vacancies_sort_backend_with_city(data=get_csv_data(unload_from="result_sorted.csv"))
	# create_chart_salary_city_backend(data=data)
	
	# построение графика и таблицы необходимых навыков
	# data = get_csv_data(unload_from="result_sorted.csv")
	# create_chart_table_skills_backend(data=data)
	pass

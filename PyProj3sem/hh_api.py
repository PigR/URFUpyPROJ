import random

import json
from datetime import date

import requests


def get_data_from_hh(url: str) -> list:
	data = requests.get(url, timeout=5).json()

	result = list()
	for item in data["items"]:
		now_date = date.today()
		published_at = date.fromisoformat(item["published_at"].split("T")[0])
		if (published_at.weekday() not in(6, 7)) and (now_date.toordinal() > published_at.toordinal()):
			if item["snippet"]["responsibility"] and item["snippet"]["requirement"] and item["employer"]["name"] \
				and (item["salary"]["from"] or item["salary"]["to"]) and item["salary"]["currency"] and item["area"]["name"]:
				result.append({
					"title": item["name"],
					"description": item["snippet"]["responsibility"],
					"skills": item["snippet"]["requirement"],
					"company": item["employer"]["name"],
					"salary_from": item["salary"]["from"],
					"salary_to": item["salary"]["to"],
					"currency": item["salary"]["currency"],
					"city": item["area"]["name"],
					"published_at": item["published_at"] 
				})
		
	return result


if __name__ == "__main__":
	url = "http://api.hh.ru/vacancies?clusters=true&only_with_salary=true&enable_snipprts=true&st=searchVacancy" \
				"&text=backend+OR+бэкэнд+OR+бекэнд+OR+бэкенд+OR+бекенд+OR+back end+OR+бэк энд+OR+бэк енд+OR+django+"\
				"OR+flask+OR+laravel+OR+yii+OR+symfony&search_field=name&per_page=100&area=1"
	data = get_data_from_hh(url=url)
	print(data)
	# with open("vacancies_hh_api.json", 'w', encoding="utf-8") as file:
	# 	json.dump(data, fp=file, indent=2, ensure_ascii=False)

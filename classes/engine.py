import requests
import json
from abc import ABC, abstractmethod


class Engine(ABC):

    @abstractmethod
    def __init__(self, vacancy):
        pass

    @abstractmethod
    def get_request(self):
        pass


class HH(Engine):
    vacancies_all = []
    vacancies_dicts = []

    def __init__(self, vacancy, range):
        self.vacancy = vacancy
        self.range = range  # Метод для инициализации переменных

    def get_request(self):
        for num in range(self.range):
            url = 'https://api.hh.ru/vacancies'
            vacancies_per_page = 20
            params = {
                'text': {self.vacancy},
                'areas': 113,
                'per_page': vacancies_per_page,
                'page': num,
                'only with salary': True
            }
            response = requests.get(url, params=params)
            info = response.json()  # метод делает запрос и добавлеят результат в переменную info
            if info is None:
                return "Данные не получены!"
            elif 'errors' in info:
                return info['errors'][0]['value']
            elif info['found'] == 0:
                return "Нет вакансий"
            else:
                for vacancy in range(
                        vacancies_per_page):  # если запрос получен без ошибок до данные из info записываются в словарь vacancies_dicts
                    self.vacancies_all.append(vacancy)
                    if info['items'][vacancy]['salary'] is not None \
                            and info['items'][vacancy]['salary']['currency'] == 'RUR':
                        vacancy_dict = {'employer': info['items'][vacancy]['employer']['name'],
                                        'name': info['items'][vacancy]['name'],
                                        'url': info['items'][vacancy]['alternate_url'],
                                        'requirement': info['items'][vacancy]['snippet']['requirement'],
                                        'salary_from': info['items'][vacancy]['salary']['from'],
                                        'salary_to': info['items'][vacancy]['salary']['to']}
                        if vacancy_dict['salary_from'] is None:
                            vacancy_dict['salary_from'] = 0
                        elif vacancy_dict['salary_to'] is None:
                            vacancy_dict['salary_to'] = "не указано"
                        self.vacancies_dicts.append(vacancy_dict)
        return self.vacancies_dicts  # метод возвращает словарь vacancies_dicts

    @staticmethod
    def make_json(vacancy, vacancies_dicts):  # метод принимает название вакансии и словарь vancies_dicts
        with open(f"{vacancy}_hh_ru.json", 'w',
                  encoding='utf-8') as file:  # метод создает файл json из словаря vancies_dict
            json.dump(vacancies_dicts, file, indent=2, ensure_ascii=False)
        return f"Вакансии добавлены в файл: {vacancy}_hh_ru.json"  # метод возвращает файл json

    @staticmethod
    def unsorted(filename, vacancies, num_of_vacancies=None):  # метод принимает имя файла и словарь vacancies
        vacancies_list = []
        for vacancy in vacancies:
            vacancies_list.append(f"""
        Наниматель: {vacancy['employer']}
        Вакансия: {vacancy['name']}
        Описание/Требования: {vacancy['requirement']}               
        Заработная плата от {vacancy['salary_from']} до {vacancy['salary_to']}      
        Ссылка на вакансию: {vacancy['url']}""")  # создает список vacancies_list
        with open(f'{filename}_unsorted_vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies_list, file, indent=2,
                      ensure_ascii=False)  # создает отдельный json файл из списка vacancies_list
        return vacancies_list  # возвращает список vacancies_list

    @staticmethod
    def sorting(filename, vacancies, num_of_vacancies=None):  # метод принимает имя файла и словарь vacancies
        vacancies_list = []
        vacancies_sort = sorted(vacancies, key=lambda vacancy: vacancy['salary_from'],
                                reverse=True)  # метод сортирует словарь по зарплате
        for vacancy in vacancies_sort:
            vacancies_list.append(f"""
        Наниматель: {vacancy['employer']}
        Вакансия: {vacancy['name']}
        Описание/Требования: {vacancy['requirement']}
        Заработная плата от {vacancy['salary_from']} до {vacancy['salary_to']}
        Ссылка на вакансию: {vacancy['url']}""")  # создает список vacancies_list
        with open(f'{filename}_sorted_vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies_sort, file, indent=2, ensure_ascii=False)
        return vacancies_list  # возвращает список vacancies_list

from classes.engine import HH

vacancy_to_search = input("Введите вакансию ")
Range = int(input("Сколько вакансий просмотреть от 20 до 200 Введите количество вакансий кратное 20 "))
Range = int(Range / 20)

hh = HH(vacancy_to_search, Range)
my_vacaincies = hh.get_request()
print(hh.make_json(vacancy_to_search, my_vacaincies))
x = input("Нужна ли сортировка по зарплате 1 - да 2 - нет ")
if x == "1":
    sorted_vacancies = hh.sorting(vacancy_to_search, my_vacaincies)
    a = int(input("Сколько отсортированных вакансий вывести "))
    for i in range(0, a):
        vacancy = sorted_vacancies[i]
        print(vacancy)
elif x == "2":
    unsorted_vacancies = hh.unsorted(vacancy_to_search, my_vacaincies)
    a = int(input("Сколько неотсортированных вакансий вывести "))
    for i in range(0, a):
        vacancy = unsorted_vacancies[i]
        print(vacancy)
else:
    print("Ошибка ввода")

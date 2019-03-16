import requests
import json

def average_salary(vacancy):
    min_salary = vacancy["salary"]["from"]
    max_salary = vacancy["salary"]["to"]
    if min_salary and max_salary:
        return(int(min_salary) + int(max_salary)) // 2
    elif min_salary and not max_salary:
        return int(min_salary)
    else:
        return None


def sort_vacancies_by_title(vacancies_info, currency):
    result = {}
    for vacancy in vacancies_info:
        if vacancy["salary"]["currency"] == currency:
            if vacancy["name"] in result.keys():
                result[vacancy["name"]].append(vacancy)
            else:
                result[vacancy["name"]] = [vacancy]
    return result


def average_salarys_vacancies(vacancies_info, currency):
    result = {}
    sorted_vacancies = sort_vacancies_by_title(vacancies_info, currency)
    for name in sorted_vacancies.keys():
        average_salarys = []
        for vacancy in sorted_vacancies[name]:
            if average_salary(vacancy):
                average_salarys.append(average_salary(vacancy))
        result[name] = {"Вакансий": len(sorted_vacancies[name]),
                        "Средняя зарплата": float(sum(average_salarys)) / max(len(average_salarys), 1)}
    return result


def main():
    max_num_vacancies = 2000
    per_page = 100
    only_with_salary = True
    my_list = []
    for page in range(max_num_vacancies//per_page):
        info = {'per_page': per_page, 'page': page, 'only_with_salary': only_with_salary}
        site = "https://api.hh.ru/"
        section = "vacancies/"
        r = requests.get(site + section, params=info)
        if r.status_code == requests.codes.ok:
            vacancies_on_page = r.json()["items"]
            for vacancy_info in vacancies_on_page:
                my_list.append(vacancy_info)
        print(page)
    result = average_salarys_vacancies(my_list, "RUR")
    output_file = open("average_salary.txt", 'w', encoding="utf-8")
    json.dump(result, output_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()

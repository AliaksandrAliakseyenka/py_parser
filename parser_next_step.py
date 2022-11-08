import requests
from bs4 import BeautifulSoup
import lxml
import json

#for use offset in url

# for i in range(0, 12):
#     url = f"https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset={i}"
#     #Проверил, что ссылки есть
#     # print(url)
#
#     req = requests.get(url)
#     result = req.content
#
#     soup = BeautifulSoup(result, "lxml")
#
#     persons = soup.findAll('a')
#     # print(persons)
#
#     persons_url_list = list()
#     for person in persons:
#         person_page_url = person.get('href')
#         persons_url_list.append(person_page_url)
#
# with open('persons_url_list.txt', 'a') as file:
#     for line in persons_url_list:
#         file.write(f"{line}\n")

with open('persons_url_list.txt') as file:

    lines = [line.strip() for line in file.readlines()]

    data_dict = list()
    count = 0
    for line in lines:
        req_pars = requests.get(line)
        result = req_pars.content
        soup = BeautifulSoup(result, 'lxml')

        get_info_person = soup.find(class_="col-xs-8 col-md-9 bt-biografie-name").find('h3').text
        person_name_company = get_info_person.strip().split(',')
        person_name = person_name_company[0]
        person_company = person_name_company[1].strip()

        linklist = soup.find_all(class_="bt-link-extern")

        social_linklist = list()
        for item in linklist:
            social_linklist.append(item.get('href'))


        data = {
            "person_name":person_name,
            "person_company":person_company,
            "social_linklist":social_linklist
        }
        count += 1
        print(f'{count}:{line} is done!!!')
        data_dict.append(data)

        with open('data.json', 'w') as json_file:
            json.dump(data_dict, json_file, indent=4)







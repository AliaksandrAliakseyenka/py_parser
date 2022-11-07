import csv
import random

import requests
from bs4 import BeautifulSoup
import lxml
import json
import time


# url = "http://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
}

# req = requests.get(url, headers=headers)
# src = req.text
#
# # print(src)
#
# with open('index.html', 'w') as file:
#     file.write(src)

# with open('index.html') as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
#
# all_prod_hrefs = soup.findAll('a', class_="mzr-tc-group-item-href")
#
# all_categories_dict = {}
# for item in all_prod_hrefs:
#     item_text = item.text
#     item_href = "http://health-diet.ru" + item.get('href')
#     all_categories_dict[item_text] = item_href
#
# with open("all_categories_dict.json", "w") as file:
#     #Запомнить параметры!!! иначе будет сохранять в строку / ensure_ascii=False могу быть проблемы с кодировкой
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)


with open("all_categories_dict.json") as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
count = 0
print(f"Всего итераций: {iteration_count}")
for category_name, category_hraf in all_categories.items():

#Тест, что все работает (if count == 0)
# if count == 0:
    rep_symbol = [",", " ", "-", "'"]
    for item in rep_symbol:
        if item in category_name:
            category_name = category_name.replace(item, "_")

    req = requests.get(url=category_hraf, headers=headers)
    src = req.text

    with open(f"data/{count}_{category_name}.html", 'w') as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html",) as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    #Проверка страницы на наличие таблицы с данными
    alert_block = soup.find(class_="uk-alert uk-alert-danger uk-h1 uk-text-center mzr-block mzr-grid-3-column-margin-top")
    if alert_block is not None:
        continue


    # соберу заголовки таблицы
    table_head = soup.find(class_ = "uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed").find("tr").find_all("th")
    # print(table_head)
    product = table_head[0].text
    calories = table_head[1].text
    protein = table_head[2].text
    fat = table_head[3].text
    carbohydrates = table_head[4].text
    # print(carbohydrates)

    #Запись headers
    with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (product,
             calories,
             protein,
             fat,
             carbohydrates)
        )

    #собираем данные product
    products_data = soup.find(class_ = "uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed").find('tbody').find_all('tr')

    products_info = list()
    for item in products_data:
        product_tds = item.find_all('td')

        product = product_tds[0].text
        calories = product_tds[1].text
        protein = product_tds[2].text
        fat = product_tds[3].text
        carbohydrates = product_tds[4].text
        products_info.append({"Product": product,
                              "Calories": calories,
                              "Protein": protein,
                              "Fat": fat,
                              "Carbohydrates": carbohydrates}
                             )


        # print(product)

        # Запись данных
        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (product,
                 calories,
                 protein,
                 fat,
                 carbohydrates)
            )
    with open(f"data/{count}_{category_name}.json", "a", encoding="utf-8") as file:
        json.dump(products_info, file, indent=4, ensure_ascii=False)
    count += 1
    print(f"# Итерация {count}. {category_name} записан...")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Работа завершена")
        break

    print(f"Осталось итераций: {iteration_count}")
    time.sleep(random.randrange(2, 4))














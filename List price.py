import os
import csv
from tabulate import tabulate


class PriceMachine():

    def __init__(self):
        self.data = []

    def load_prices(self, file_path):

        for file_name in os.listdir(file_path):  # проходим по всем файлам директории
            if "price" in file_name:  # проверяем, содержит ли имя слово 'price'
                with open(os.path.join(file_path, file_name), 'r', newline='',
                          encoding='utf-8') as csv_file:  # открываем файл для чтения
                    data = csv.DictReader(csv_file)  # загружаем данные в формате CSV
                    for row in data:  # проходим по каждому элементу данных в файле
                        product_name = None
                        price = None
                        weight = None
                        price_kg = None
                        for key, value in row.items():  # проходим ключ-значение в каждом элементе данных
                            # проверяем соответсвует ли ключ названию продукта
                            if key in ['товар', 'название', 'наименование', 'продукт']:
                                product_name = value
                            elif key in ['розница', 'цена']:
                                price = float(value)
                            elif key in ['вес', 'масса', 'фасовка']:
                                weight = float(value)

                        if product_name and price and weight:
                            # Добавляются найденные данные  в список данных объекта класса для последующего анализа.
                            self.data.append(
                                {
                                    'Наименование': product_name,
                                    'Цена': price,
                                    'Вес': weight,
                                    'Файл': file_name,
                                    'Цена за кг': price / weight
                                }
                            )

    def export_to_html(self, output_file):

        with open(output_file, 'w', encoding='utf-8') as html_file:  # Открывается файл для записи в формате HTML.
            # Добавление тега <meta> для корректного отображения кириллицы
            html_file.write("<html><head><meta charset='utf-8'></head><body>")
            html_file.write("<table>")
            html_file.write(
                "<tr><th>Наименование</th><th>Цена</th><th>Вес</th><th>Файл</th><th>Цена за кг</th></tr>")
            for item in self.data:
                html_file.write("<tr>")
                html_file.write(f"<td>{item['Наименование']}</td>")
                html_file.write(f"<td>{item['Цена']}</td>")
                html_file.write(f"<td>{item['Вес']}</td>")
                html_file.write(f"<td>{item['Файл']}</td>")
                html_file.write(f"<td>{item['Цена за кг']}</td>")
                html_file.write("</tr>")
            html_file.write("</table>")
            html_file.write("</body></html>")

    def table(self):
        print(tabulate(self.data, headers='keys', tablefmt='grid'))

    def find_text(self, text):
        filtered_results = []
        for item in self.data:
            if text in item['Наименование'].lower():  # проверка, содержит ли поле 'Наименование' 'text'
                filtered_results.append(item)
                self.data = filtered_results
        # результат сортируется по ключу, предствляющий отношение "Цены" к "Весу"
        sorted_result = sorted(filtered_results, key=lambda x: x['Цена'] / x['Вес'])
        return sorted_result


pm = PriceMachine()
pm.load_prices('C:\\Users\\PycharmProjects\\List price\\Analys_list\\')
output_file = 'C:\\Users\\PycharmProjects\\List price\\Analys_list\\output.html'
file_path = 'C:\\Users\\PycharmProjects\\List price\\Analys_list\\'

while True:
    user_input = input("Введите текст для поиска (для выхода введите 'exit'): ").lower()
    if user_input != 'exit':
        # Если пользователь не ввел 'exit', выполняется поиск текста в прайс-листах
        search_results = pm.find_text(user_input)
        pm.table()
        pm.export_to_html(output_file)

    else:
        # Если пользователь ввел 'exit', программа завершает работу
        print("Работа завершена.")
        break
# Экспорт данных в HTML
pm.export_to_html(output_file)

import os
import json
from bs4 import BeautifulSoup


# Парсинг HTML-файла
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    data = {
        'Тип': soup.find('div', class_='chess-wrapper').find('span').text.strip(),
        'Турнир': soup.find('h1', class_='title').text.strip(),
        'Город': soup.find('p', class_='address-p').text.strip().replace('Город: ', ''),
        'Количество туров': int(soup.find('span', class_='count').text.strip().split(':')[-1]),
        'Контроль времени': soup.find('span', class_='year').text.strip().split(':')[-1],
        'Минимальный рейтинг для участия': int(soup.find_all('span')[-1].text.strip().split(':')[-1]),
        'Рейтинг': float(soup.find_all('span')[-2].text.strip().split(':')[-1]),
        'Просмотры': int(soup.find_all('span')[-3].text.strip().split(':')[-1]),
        'Изображение': soup.find('img')['src'],
    }

    return data


def process_html_files(directory):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                html_content = file.read()
                data = parse_html(html_content)
                all_data.append(data)

    return all_data


def write_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


html_directory = '.'
json_output_file = 'output.json'
all_data = process_html_files(html_directory)

write_to_json(all_data, json_output_file)
sorted_data = sorted(all_data, key=lambda x: x['Просмотры'])


# Фильтрация данных по "Тип: circular"
def filter_data_by_type(all_data, target_type):
    filtered_data = [item for item in all_data if item['Тип'] == target_type]
    return filtered_data


target_type = 'Тип: circular'
filtered_data_by_type = filter_data_by_type(all_data, target_type)
filtered_json_output_file = 'filtered_output.json'
with open(filtered_json_output_file, 'w', encoding='utf-8') as json_file:
    json.dump(filtered_data_by_type, json_file, ensure_ascii=False, indent=2)
write_to_json(filtered_data_by_type, filtered_json_output_file)

rating_values = [item['Рейтинг'] for item in all_data]
statistics = {
    'Сумма': sum(rating_values),
    'Минимум': min(rating_values),
    'Максимум': max(rating_values),
    'Среднее': sum(rating_values) / len(rating_values),
}

city_frequency = {}
for item in all_data:
    city = item['Город']
    city_frequency[city] = city_frequency.get(city, 0) + 1

# print('Сортировка по Просмотрам:', sorted_data)
# print('Статистика по Рейтингу:', statistics)
# print('Частота меток по Городу:', city_frequency)

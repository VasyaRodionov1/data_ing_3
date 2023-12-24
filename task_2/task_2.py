import os
import json
from bs4 import BeautifulSoup
import statistics
from collections import Counter


def parse_product_item(product_item):
    data = {}
    data['id'] = product_item.find('a', class_='add-to-favorite')['data-id']
    name_element = product_item.find('span')
    data['name'] = name_element.text.strip() if name_element else None
    price_element = product_item.find('price')
    data['price'] = price_element.text.strip() if price_element else None
    ul_element = product_item.find('ul')
    if ul_element:
        li_elements = ul_element.find_all('li')
        for li_element in li_elements:
            li_type = li_element.attrs.get('type')
            li_text = li_element.text.strip()
            data[li_type] = li_text

    return data


script_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = script_dir

all_products = []

for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        product_items = soup.find_all('div', class_='product-item')
        for item in product_items:
            product_data = parse_product_item(item)
            all_products.append(product_data)

output_path = os.path.join(script_dir, 'output.json')
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_products, json_file, ensure_ascii=False, indent=2)

sorted_by_price = sorted(all_products, key=lambda x: x.get('price', 0))
sorted_output_path = os.path.join(script_dir, 'sorted_by_price.json')
with open(sorted_output_path, 'w', encoding='utf-8') as sorted_json_file:
    json.dump(sorted_by_price, sorted_json_file, ensure_ascii=False, indent=2)

filtered_by_processor = [product for product in all_products if product.get('processor') == '8x1.2 ГГц']
filtered_output_path = os.path.join(script_dir, 'filtered_by_processor.json')
with open(filtered_output_path, 'w', encoding='utf-8') as filtered_json_file:
    json.dump(filtered_by_processor, filtered_json_file, ensure_ascii=False, indent=2)

acc_values = [float(product.get('acc', '').replace('мА * ч', '').replace(' ', '')) for product in all_products if
              'acc' in product]
acc_statistics = {
    'sum': sum(acc_values),
    'min': min(acc_values),
    'max': max(acc_values),
    'mean': statistics.mean(acc_values),
}
statistics_output_path = os.path.join(script_dir, 'acc_statistics.json')
with open(statistics_output_path, 'w', encoding='utf-8') as statistics_json_file:
    json.dump(acc_statistics, statistics_json_file, ensure_ascii=False, indent=2)

matrix_values = [product.get('matrix', '') for product in all_products]
matrix_frequency = Counter(matrix_values)
frequency_output_path = os.path.join(script_dir, 'matrix_frequency.json')
with open(frequency_output_path, 'w', encoding='utf-8') as frequency_json_file:
    json.dump(matrix_frequency, frequency_json_file, ensure_ascii=False, indent=2)

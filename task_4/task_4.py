import os
import json
import xml.etree.ElementTree as ET
import statistics
from collections import Counter


def clean_text(text):
    return text.strip()


def parse_clothing(xml_root):
    clothing_data = []
    for clothing_element in xml_root.findall('.//clothing'):
        item_data = {}
        for child in clothing_element:
            tag = child.tag
            text = clean_text(child.text)
            if tag in ['price', 'rating', 'reviews']:
                # Приведение типов для price, rating и reviews
                item_data[tag] = float(text) if '.' in text else int(text)
            else:
                item_data[tag] = text
        clothing_data.append({'clothing': item_data})
    return clothing_data


script_dir = os.path.dirname(os.path.abspath(__file__))
xml_folder_path = script_dir
all_clothing = []

for filename in os.listdir(xml_folder_path):
    if filename.endswith('.xml'):
        file_path = os.path.join(xml_folder_path, filename)
        tree = ET.parse(file_path)
        root = tree.getroot()
        clothing_data = parse_clothing(root)
        all_clothing.extend(clothing_data)

output_path = os.path.join(script_dir, 'full_output.json')
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_clothing, json_file, ensure_ascii=False, indent=2)

sorted_by_name = sorted(all_clothing, key=lambda x: x.get('clothing', {}).get('name', ''))
sorted_output_path = os.path.join(script_dir, 'sorted_by_name.json')
with open(sorted_output_path, 'w', encoding='utf-8') as sorted_json_file:
    json.dump(sorted_by_name, sorted_json_file, ensure_ascii=False, indent=2)

filtered_by_category = [item for item in all_clothing if item.get('clothing', {}).get('category') == 'Socks']
filtered_output_path = os.path.join(script_dir, 'filtered_by_category.json')
with open(filtered_output_path, 'w', encoding='utf-8') as filtered_json_file:
    json.dump(filtered_by_category, filtered_json_file, ensure_ascii=False, indent=2)

price_values = [float(item.get('clothing', {}).get('price', 0)) for item in all_clothing]
price_statistics = {
    'sum': sum(price_values),
    'min': min(price_values),
    'max': max(price_values),
    'mean': statistics.mean(price_values),
}
statistics_output_path = os.path.join(script_dir, 'price_statistics.json')
with open(statistics_output_path, 'w', encoding='utf-8') as statistics_json_file:
    json.dump(price_statistics, statistics_json_file, ensure_ascii=False, indent=2)

category_values = [item.get('clothing', {}).get('category', '') for item in all_clothing]
category_frequency = Counter(category_values)
frequency_output_path = os.path.join(script_dir, 'category_frequency.json')
with open(frequency_output_path, 'w', encoding='utf-8') as frequency_json_file:
    json.dump(category_frequency, frequency_json_file, ensure_ascii=False, indent=2)

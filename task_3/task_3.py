import os
import json
import xml.etree.ElementTree as ET
import statistics
from collections import Counter


def clean_text(text):
    return text.strip()


def parse_star(xml_root):
    star_data = {}
    star_data['name'] = clean_text(xml_root.findtext('name'))
    star_data['constellation'] = clean_text(xml_root.findtext('constellation'))
    star_data['spectral_class'] = clean_text(xml_root.findtext('spectral-class'))
    star_data['radius'] = float(clean_text(xml_root.findtext('radius')))
    star_data['rotation'] = clean_text(xml_root.findtext('rotation'))
    star_data['age'] = clean_text(xml_root.findtext('age'))
    star_data['distance'] = float(clean_text(xml_root.findtext('distance').split()[0]))
    star_data['absolute_magnitude'] = float(clean_text(xml_root.findtext('absolute-magnitude').split()[0]))
    return star_data


script_dir = os.path.dirname(os.path.abspath(__file__))
xml_folder_path = script_dir

all_stars = []

# Loop through XML files
for filename in os.listdir(xml_folder_path):
    if filename.endswith('.xml'):
        file_path = os.path.join(xml_folder_path, filename)
        tree = ET.parse(file_path)
        root = tree.getroot()
        star_data = parse_star(root)
        all_stars.append(star_data)

output_path = os.path.join(script_dir, 'full_output.json')
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_stars, json_file, ensure_ascii=False, indent=2)

sorted_by_constellation = sorted(all_stars, key=lambda x: x.get('constellation', ''))
sorted_output_path = os.path.join(script_dir, 'sorted_by_constellation.json')
with open(sorted_output_path, 'w', encoding='utf-8') as sorted_json_file:
    json.dump(sorted_by_constellation, sorted_json_file, ensure_ascii=False, indent=2)

filtered_by_constellation = [star for star in all_stars if star.get('constellation') == 'Рыбы']
filtered_output_path = os.path.join(script_dir, 'filtered_by_constellation.json')
with open(filtered_output_path, 'w', encoding='utf-8') as filtered_json_file:
    json.dump(filtered_by_constellation, filtered_json_file, ensure_ascii=False, indent=2)

distance_values = [star.get('distance', 0) for star in all_stars]
distance_statistics = {
    'sum': sum(distance_values),
    'min': min(distance_values),
    'max': max(distance_values),
    'mean': statistics.mean(distance_values),
}
statistics_output_path = os.path.join(script_dir, 'distance_statistics.json')
with open(statistics_output_path, 'w', encoding='utf-8') as statistics_json_file:
    json.dump(distance_statistics, statistics_json_file, ensure_ascii=False, indent=2)

constellation_values = [star.get('constellation', '') for star in all_stars]
constellation_frequency = Counter(constellation_values)
frequency_output_path = os.path.join(script_dir, 'constellation_frequency.json')
with open(frequency_output_path, 'w', encoding='utf-8') as frequency_json_file:
    json.dump(constellation_frequency, frequency_json_file, ensure_ascii=False, indent=2)

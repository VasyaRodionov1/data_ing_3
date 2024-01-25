import os
import requests
from bs4 import BeautifulSoup
import json
from collections import Counter


def get_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text

# Парсинг данных о книгах
def parse_books(url):
    page_content = get_page(url)
    if not page_content:
        return None

    soup = BeautifulSoup(page_content, "html.parser")
    books = []

    # Находим все элементы с информацией о книгах
    book_elements = soup.select("article.product-card")

    for book_elem in book_elements:
        book_info = {
            "id": book_elem.get("data-chg-product-id", ""),
            "name": book_elem.get("data-chg-product-name", ""),
            "brand": book_elem.get("data-chg-product-brand", ""),
            "price": int(book_elem.get("data-chg-product-price", 0)),
            "old_price": int(book_elem.get("data-chg-product-old-price", 0)),
            "image_url": book_elem.select_one("img.product-picture__img")["data-src"] if book_elem.select_one("img.product-picture__img") else "",
        }

        books.append(book_info)

    return books

# Функция для записи данных в JSON файл
def write_to_json(data, filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, filename)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

# Основная функция с операциями
def go_operations(url):
    catalog_data = parse_books(url)

    if catalog_data:
        write_to_json(catalog_data, "all_books.json")

        # Сортировка по цене
        sorted_data_price = sorted(catalog_data, key=lambda x: x["price"])
        write_to_json(sorted_data_price, "sorted_by_price.json")

        # Фильтрация по полю "brand" со значением "Clever"
        brand_to_filter = "Clever"
        filtered_data_brand = [book for book in catalog_data if book["brand"] == brand_to_filter]
        write_to_json(filtered_data_brand, "filtered_by_brand.json")

        # Показатели статистики для числового поля "price"
        prices = [book["price"] for book in catalog_data]
        average_price = sum(prices) / len(prices)
        max_price = max(prices)
        min_price = min(prices)

        statistics_data = {
            "average_price": average_price,
            "max_price": max_price,
            "min_price": min_price,
        }
        write_to_json(statistics_data, "price_statistics.json")

        # Статистика по брендам
        brands = [book["brand"] for book in catalog_data]
        brand_frequency = Counter(brands)
        write_to_json(brand_frequency, "brand_frequency.json")

# URL каталога
catalog_url = "https://www.chitai-gorod.ru/bestsell?page=1&filters%5Bcategories%5D=110001"

go_operations(catalog_url)

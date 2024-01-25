import os
import requests
from bs4 import BeautifulSoup
import json


def get_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text


# Парсинг характеристик конкретной книги
def parse_book_details(book_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(book_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    characteristics_container = soup.find("div", class_="product-detail-characteristics")

    if not characteristics_container:
        print("Characteristics container not found.")
        return None

    characteristics_items = characteristics_container.find_all("div", class_="product-detail-characteristics__item")

    book_details = {}

    # Добавим название книги
    title_elem = soup.find("h1", itemprop="name")
    title = title_elem.get_text(strip=True) if title_elem else ""
    book_details["title"] = title

    # Добавим информацию об авторах
    authors_elem = soup.find("div", class_="product-detail-title__authors")
    authors = [author.get_text(strip=True) for author in
               authors_elem.find_all("a", class_="product-detail-title__author")] if authors_elem else []
    book_details["authors"] = authors

    for item in characteristics_items:
        title = item.find("span", class_="product-detail-characteristics__item-title")
        value = item.find("span", class_="product-detail-characteristics__item-value")

        if title and value:
            # Приведение типов, где это необходимо
            key = title.get_text(strip=True)
            raw_value = value.get_text(strip=True)

            if key in ["ID товара", "Год издания", "Количество страниц", "Тираж", "Вес, г"]:
                book_details[key] = int(raw_value)
            else:
                book_details[key] = raw_value

    # Описание книги
    description_elem = soup.find("div", itemprop="description")
    description = description_elem.get_text(strip=True) if description_elem else ""
    book_details["description"] = description

    return book_details


# URL книги
book_url = "https://www.chitai-gorod.ru/product/feyri-profayler-3015728?productShelf=&shelfIndex=0&productIndex=15"

# Вызов функции для получения характеристик книги и записи в JSON файл
book_details = parse_book_details(book_url)

if book_details:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "book_characteristics.json")
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(book_details, json_file, ensure_ascii=False, indent=2)

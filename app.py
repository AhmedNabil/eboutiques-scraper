from itertools import product
from math import prod
from bs4 import BeautifulSoup
import requests
import csv
from pathlib import Path
from const import cats
import handler

isHaveNextPage = True
page = 1
id = 0
list = []
itemsPerPage = 12
FILE_PATH = Path("products.csv")
baseUrl = "https://www.ewg.org/skindeep/browse/category/"


if not FILE_PATH.exists():
    with open(FILE_PATH, "w", newline="") as products_csv:
        products_csv_write = csv.writer(products_csv)
        products_csv_write.writerow(["id", "name", "company"])


while isHaveNextPage:
    for idx, category in enumerate(cats):
        for index, sub_category in enumerate(category["sub_categories"]):
            url = baseUrl + sub_category["slug"]
            if page > 1:
                url = (
                    baseUrl
                    + sub_category["slug"]
                    + "/"
                    + "?category="
                    + sub_category["pagination_slug"]
                    + "&page="
                    + str(page)
                )
            session = requests.Session()
            session.cookies.update({"__hs_opt_out": "yes"})
            session.get(url)
            response = requests.get(url)
            if response.status_code == 403:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                response = requests.get(url, headers=headers).text
                soup = BeautifulSoup(response, "lxml")
                products = soup.find_all("div", class_="product-tile")
                for index, product in enumerate(products):
                    product_info = handler.product_handler(product)
                    # print(product_info)
                print("page---", page, "---page")
                print(url)
                if soup.find("div", class_="product-tile") is None:
                    isHaveNextPage = False
                page += 1

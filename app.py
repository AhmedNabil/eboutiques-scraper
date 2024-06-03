from itertools import product
from math import prod
from time import sleep
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
FILE_PATH = Path("products.csv")
baseUrl = "https://www.ewg.org/skindeep/browse/category/"


if not FILE_PATH.exists():
    with open(FILE_PATH, "w", newline="") as products_csv:
        products_csv_write = csv.writer(products_csv)
        products_csv_write.writerow(
            [
                "ID",
                "Name",
                "Company",
                "Main Category",
                "Parent Category",
                "Sub Category",
            ]
        )


for idx, category in enumerate(cats):
    for index, sub_category in enumerate(category["sub_categories"]):
        main_cat = category["main_category"]
        parent_cat = sub_category["parent_category"]
        sub_cat = sub_category["name"]
        print("##################################################################")
        print(f"Main-Category : {main_cat}")
        print(f"Parent-Category : {parent_cat}")
        print(f"Sub-Category : {sub_cat}")
        print("##################################################################")
        isHaveNextPage = True
        page = 1
        sleep(2)
        while isHaveNextPage:
            url = handler.url_handler(
                baseUrl=baseUrl,
                slug=sub_category["slug"],
                pagination_slug=sub_category["pagination_slug"],
                page=page,
            )
            product_list = handler.product_list_handler(url)
            print(url)
            print("page---", page, "---page")
            for product in product_list:  # noqa: F402
                id += 1
                product_name = handler.product_handler(product)["product_name"]
                product_company = handler.product_handler(product)["product_company"]
                print(f"ID : {id}")
                print(f"Product Name : {product_name}")
                print(f"Product Company : {product_company}")
                print(
                    f"Product Image : {handler.product_handler(product)['product_img']}"
                )
                print(
                    f"Product URL : {handler.product_handler(product)['product_url']}"
                )
                print(f"Main Category : {main_cat}")
                print(f"Parent Category : {parent_cat}")
                print(f"Sub Category : {sub_cat}")
                print(
                    "##################################################################"
                )

                with open(FILE_PATH, "a", newline="") as products_csv:
                    products_csv_write = csv.writer(products_csv)
                    products_csv_write.writerow(
                        [
                            id,
                            product_name,
                            product_company,
                            main_cat,
                            parent_cat,
                            sub_cat,
                        ]
                    )
            isHaveNextPage = handler.next_page_checker(url)
            sleep(3)
            page += 1

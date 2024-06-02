from itertools import product
from math import prod
from bs4 import BeautifulSoup
import requests
import csv
from pathlib import Path
from const import cats
import handler


def product_handler(product):
    text_wrapper = product.find("div", class_="text-wrapper")
    product_name = text_wrapper.find("div", class_="product-name").text
    product_company = text_wrapper.find("div", class_="product-company").text
    product_img = product.find("img")["src"]
    product_url = product.find("a")["href"]
    product_details_handler(product_url)
    return {
        "product_name": product_name,
        "product_company": product_company,
        "product_img": product_img,
        "product_url": product_url,
    }


def product_details_handler(url):
    session = requests.Session()
    session.cookies.update({"__hs_opt_out": "yes"})
    session.get(url)
    response = requests.get(url)
    if response.status_code == 403:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, "lxml")
        ingredient_overviews = soup.find_all("tr", class_="ingredient-overview-tr")
        ingredient_more_info_wrappers = soup.find_all(
            "tr", class_="ingredient-more-info-wrapper"
        )
        for index, ingredient_overview in enumerate(ingredient_overviews):
            ingredient_title = ingredient_overview.find(
                "div", class_="td-ingredient-interior"
            ).text
            functions_concerns = ingredient_more_info_wrappers[index].find_all("td")
            print(functions_concerns)

        # print(ingredient_more_info_wrappers)

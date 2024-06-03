from itertools import product
from math import prod
from bs4 import BeautifulSoup
import requests
import csv
from pathlib import Path
from const import cats
import handler


def url_handler(baseUrl, slug, pagination_slug, page):
    url = baseUrl + slug
    if page > 1:
        url = (
            baseUrl + slug + "/" + "?category=" + pagination_slug + "&page=" + str(page)
        )
    return url


def soup_response(url):
    try:
        session = requests.Session()
        session.cookies.update({"__hs_opt_out": "yes"})
        session.get(url)
        response = requests.get(url)
        if response.status_code == 403:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(url, headers=headers).text
            soup = BeautifulSoup(response, "lxml")
            return soup
        else:
            soup = BeautifulSoup(response.text, "lxml")
            return soup
    except Exception as e:
        print(e)


def next_page_checker(url):
    soup = soup_response(url)
    if soup.find("a", class_="next_page") is None:
        return False
    else:
        return True


def product_list_handler(url):
    soup = soup_response(url)
    products = soup.find_all("div", class_="product-tile")
    return products


def product_handler(product):
    text_wrapper = product.find("div", class_="text-wrapper")
    product_name = text_wrapper.find("div", class_="product-name").text
    product_company = text_wrapper.find("div", class_="product-company").text
    product_img = product.find("img")["src"]
    product_url = product.find("a")["href"]
    return {
        "product_name": product_name,
        "product_company": product_company,
        "product_img": product_img,
        "product_url": product_url,
    }


def product_details_handler(url):
    soup = soup_response(url)
    ingredient_overviews = soup.find_all("tr", class_="ingredient-overview-tr")
    ingredient_more_info_wrappers = soup.find_all(
        "tr", class_="ingredient-more-info-wrapper"
    )
    for index, ingredient_overview in enumerate(ingredient_overviews):
        ingredient_title = ingredient_overview.find(
            "div", class_="td-ingredient-interior"
        ).text
        functions_concerns = ingredient_more_info_wrappers[index].find_all("td")
        for function_concern in functions_concerns:
            print(function_concern.text)

    print(ingredient_more_info_wrappers)

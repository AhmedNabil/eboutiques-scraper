from itertools import product
from logging import info, warn
from math import e, inf, prod
import re
from tkinter import XView
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
    label_information = fetch_label_information(soup)
    product_ingredient_concern = fetch_product_ingredient_concerns(soup)
    print(product_ingredient_concern)
    print("================================================================")

def fetch_product_ingredient_concerns(soup):
    ingredient_list = []
    if soup.find("section", class_="product-concerns-and-info") is None:
        return None

    ingredient_list = (
        soup.find("section", class_="product-concerns-and-info")
        .find("table", class_="table-ingredient-concerns")
        .find("tbody")
        .find_all("tr", class_="ingredient-overview-tr")
    )

    ingredient_more_info_list = (
         soup.find("section", class_="product-concerns-and-info")
        .find("table", class_="table-ingredient-concerns")
        .find("tbody")
        .find_all("tr", class_="ingredient-more-info-wrapper")
    )
    
    product_ingredient_concern = []
    for idx, ingredient in enumerate(ingredient_list):
        ingredient_concern = {}
        ingredient_concern["ingredient_name"] = ingredient.find(
            "td", class_="td-ingredient"
        ).find('div' , class_="td-ingredient-interior").text.strip()
        for heading in ingredient_more_info_list[idx].find_all(["td"]):
            if "CONCERNS" in heading.text:
                ingredient_concern["ingredient_concerns"] = heading.find_next("td").text
            if "FUNCTION(S)" in heading.text:
                ingredient_concern["ingredient_function"] = heading.find_next("td").text
        product_ingredient_concern.append(ingredient_concern)
    return product_ingredient_concern 
  
    

        

def fetch_label_information(soup):
    info_list = []
    if soup.find("section", attrs={"id": "label-information"}) is None:
        return None
    info_list = soup.find("section", attrs={"id": "label-information"}).find_all(
        ["h2", "p"]
    )
    for heading in info_list:
        label_information = {}
        if (
            heading.name == "h2"
            and "Ingredients from packaging" in heading.text.strip()
        ):
            for p in heading.find_next_siblings("p"):
                label_information["ingredients_from_packaging"] = p.text.strip()

        if heading.name == "h2" and "Warnings from packaging" in heading.text.strip():
            for p in heading.find_next_siblings("p"):
                label_information["warnings_from_packaging"] = p.text.strip()

        return label_information

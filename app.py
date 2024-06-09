from itertools import product
from pathlib import Path
from time import sleep
import handler
from const import cats


isHaveNextPage = True
page = 1
id = 0
list = []
FILE_PATH = Path("products.xlsx")
baseUrl = "https://www.ewg.org/skindeep/browse/category/"


handler.xlsx_file(FILE_PATH)

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
        sleep(1)
        while isHaveNextPage:
            url = handler.url_handler(
                baseUrl=baseUrl,
                slug=sub_category["slug"],
                pagination_slug=sub_category["pagination_slug"],
                page=page,
            )
            product_list = handler.product_list_handler(url)
            print("page------", page, "------page")
            for product in product_list:  # noqa: F402
                sleep(3)
                id += 1
                product_url = handler.product_handler(product)["product_url"]
                product_details = handler.product_details_handler(product_url)
                product_name = product_details["product_name"]
                product_company = handler.product_handler(product)["product_company"]
                product_img = handler.product_handler(product)["product_img"]
                product_label_information = product_details["label_information"]
                ingredient_from_packaging = product_label_information[
                    "ingredients_from_packaging"
                ]
                directions_from_packaging = (
                    product_label_information["directions_from_packaging"]
                    if "directions_from_packaging" in product_label_information
                    else "N/A"
                )
                warnings_from_packaging = (
                    product_label_information["warnings_from_packaging"]
                    if "warnings_from_packaging" in product_label_information
                    else "N/A"
                )
                product_ingredient_concerns = product_details[
                    "product_ingredient_concerns"
                ]
                print(
                    "===================================================================================================="
                )
                print(f"ID : {id}")
                print(f"Product Name : {product_name}")
                print(f"Product Company : {product_company}")
                print(f"Product Image : {product_img}")
                print(f"Ingredients From Packaging : {ingredient_from_packaging}")
                print(f"Directions From Packaging : {directions_from_packaging}")
                print(f"Warnings From Packaging : {warnings_from_packaging}")
                # print(f"Product Ingredient Concerns : {product_ingredient_concerns}")
                print(
                    "===================================================================================================="
                )
                handler.write_product_to_xlsx(
                    FILE_PATH,
                    {
                        "id": id,
                        "product_name": product_name,
                        "product_img": product_img,
                        "product_company": product_company,
                        "product_url": product_url,
                        "main_category": main_cat,
                        "parent_category": parent_cat,
                        "sub_category": sub_cat,
                        "ingredient_from_packaging": ingredient_from_packaging,
                        "directions_from_packaging": directions_from_packaging,
                        "warnings_from_packaging": warnings_from_packaging,
                        "product_ingredient_concerns": product_ingredient_concerns,
                    },
                )
                for ingredient in product_details["product_ingredient_concerns"]:
                    handler.write_ingredient_to_xlsx(
                        FILE_PATH,
                        {
                            "ingredient_name": ingredient["ingredient_name"],
                            "product_id": id,
                            "ingredient_function": (
                                ingredient["ingredient_function"]
                                if "ingredient_function" in ingredient
                                else "N/A"
                            ),
                            "ingredient_concerns": (
                                ingredient["ingredient_concerns"]
                                if "ingredient_concerns" in ingredient
                                else "N/A"
                            ),
                        },
                    )
            isHaveNextPage = handler.next_page_checker(url)
            sleep(1)
            page += 1

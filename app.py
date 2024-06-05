from itertools import product
from math import prod
from time import sleep
from bs4 import BeautifulSoup
import requests
import csv
from pathlib import Path
from const import cats
import handler
import xlsxwriter



# # Create an new Excel file and add a worksheet.
# workbook = xlsxwriter.Workbook('products.xlsx')
# worksheet = workbook.add_worksheet('Products')
# worksheet2 = workbook.add_worksheet('Ingredients')

# # Widen the first column to make the text clearer.
# worksheet.set_column('A:A', 20)

# # Add a bold format to use to highlight cells.
# bold = workbook.add_format({'bold': True})

# # Write some simple text.
# worksheet.write('A1', 'Hello')

# # Text with formatting.
# worksheet.write('A2', 'World', bold)

# # Write some numbers, with row/column notation.
# worksheet.write(2, 0, 123)
# worksheet.write(3, 0, 123.456)

# img_download = handler.img_download("https://phorcys-static.ewg.org/cdn-cgi/image/width=300,height=300,quality=60/https://phorcys-static.ewg.org/image/contents/620584/medium.png?1655315800" , "1")

# # Insert an image.
# worksheet.insert_image('B5', 'imgs/1.png')

# workbook.close()













isHaveNextPage = True
page = 1
id = 0
list = []
FILE_PATH = Path("products.xlsx")
baseUrl = "https://www.ewg.org/skindeep/browse/category/"


if not FILE_PATH.exists():
    with open(FILE_PATH, "w", newline="") as products_csv:
        workbook = xlsxwriter.Workbook('products.xlsx')
        products_worksheet = workbook.add_worksheet('Products')
        ingredients_worksheet = workbook.add_worksheet('Ingredients')
        bold = workbook.add_format({'bold': True})

        products_worksheet.set_column('A:A', 20)
        products_worksheet.set_column('B:B', 40)
        products_worksheet.set_column('C:C', 40)
        products_worksheet.set_column('D:D', 40)
        products_worksheet.set_column('E:E', 20)
        products_worksheet.set_column('F:F', 20)
        products_worksheet.set_column('G:G', 20)
        products_worksheet.set_column('H:H', 100)
        products_worksheet.set_column('I:I', 100)
        products_worksheet.set_column('J:J', 100)

        products_worksheet.write('A1', 'ID', bold)
        products_worksheet.write('B1', 'Name', bold)
        products_worksheet.write('C1', 'Image', bold)
        products_worksheet.write('D1', 'Product URL', bold)
        products_worksheet.write('E1', 'Main Category', bold)
        products_worksheet.write('F1', 'Parent Category', bold)
        products_worksheet.write('G1', 'Sub Category', bold)
        products_worksheet.write('H1', 'Ingredients From Packaging', bold)
        products_worksheet.write('I1', 'Directions From Packaging', bold)
        products_worksheet.write('J1', 'Warnings From Packaging', bold)

        ingredients_worksheet.set_column('A:A', 20)
        ingredients_worksheet.set_column('B:B', 80)
        ingredients_worksheet.set_column('C:C', 20)
        ingredients_worksheet.set_column('D:D', 150)
        ingredients_worksheet.set_column('E:E', 150)
        
        ingredients_worksheet.write('A1', 'ID', bold)
        ingredients_worksheet.write('B1', 'Ingredient Name', bold)
        ingredients_worksheet.write('C1', 'Product ID', bold)
        ingredients_worksheet.write('D1', 'FUNCTION(S)', bold)
        ingredients_worksheet.write('E1', 'CONCERNS', bold)

        workbook.close()














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
                ingredient_from_packaging =  product_label_information["ingredients_from_packaging"]
                directions_from_packaging = product_label_information["directions_from_packaging"] if "directions_from_packaging" in product_label_information  else "N/A"
                warnings_from_packaging = product_label_information["warnings_from_packaging"] if "warnings_from_packaging" in product_label_information  else "N/A"
                product_ingredient_concerns = product_details["product_ingredient_concerns"]
                print ("====================================================================================================")
                print(f"ID : {id}")
                print(f"Product Name : {product_name}")
                print(f"Product Company : {product_company}")
                print (f"Product Image : {product_img}")
                print(f"Ingredients From Packaging : {ingredient_from_packaging}")
                print(f"Directions From Packaging : {directions_from_packaging}")
                print(f"Warnings From Packaging : {warnings_from_packaging}")
                print(f"Product Ingredient Concerns : {product_ingredient_concerns}")
                print ("====================================================================================================")
                # with open(FILE_PATH, "a", newline="") as products_csv:
                #     products_csv_write = csv.writer(products_csv)
                #     products_csv_write.writerow(
                #         [
                #             id,
                #             product_name,
                #             product_img,
                #             product_company,
                #             product_url,
                #             main_cat,
                #             parent_cat,
                #             sub_cat,
                #             ingredient_from_packaging,
                #             directions_from_packaging, 
                #             warnings_from_packaging,
                #             product_details["product_ingredient_concerns"],

                #         ]
                #     )
            isHaveNextPage = handler.next_page_checker(url)
            sleep(1)
            page += 1

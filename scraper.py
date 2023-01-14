#import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json
import os


class RetryException(Exception):
  pass

def calc_product_quantity(product_price_label, product_price_unit_label):
  if product_price_unit_label:
    return (product_price_unit_label[0][1:], float(product_price_label[1].replace('.', '').replace(',', '.')), float(product_price_unit_label[1][2:-1].replace('.', '').replace(',', '.')))
  else:
    return(None, 0, 0)
    
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

page_number = 1

df_index = 1
sections = ['despensa', 'lacteos-huevos-y-refrigerados', 'pollo-carne-y-pescado', 'frutas-y-verduras', 'despensa/enlatados-y-conservas', 'delicatessen', 'vinos-y-licores', 'snacks', 'panaderia-y-reposteria', 'aseo-del-hogar', 'despensa/bebidas']
sections_idx = 0
saved = False
fcsv = open("exito__.csv", "a")
fcsv.write("marca,nombre_producto,precio,cantidad,precio_unidad,unidad,seccion\n")
fcontent = []

retry_counts = 0

while True:
  break
  current_section = sections[sections_idx]
  try:

    driver.get(f"https://www.exito.com/mercado/{current_section}/?layout=one&page={page_number}")

    time.sleep(8)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".vtex-search-result-3-x-totalProductsMessage"))
    )

    print("Page {} from section {} loaded".format(page_number, current_section))

    product_list = None
    try:
        for i in range(1,13):
          driver.execute_script("window.scrollTo(0, document.body.scrollHeight*{});".format(i/12))
          time.sleep(0.4)

        time.sleep(3)

        product_list = WebDriverWait(driver, 5).until(
          EC.presence_of_element_located((By.ID, "gallery-layout-container"))
        )
    except TimeoutException:
      print(f"Could not find the layout of products for page {page_number} from section {current_section}")
      print("Checking if there are no elements...")
      retry_counts += 1
      if retry_counts == 3:
        if sections_idx == len(sections)-1:
          break
          print('breaking scraper, no more pages. reached page number {}'.format(page_number))
        print('finished section {}'.format(current_section))
        sections_idx+=1
        page_number = 1
        retry_counts = 0
        continue
      else:
        raise RetryException()
    except:
      raise RetryException()

    if not product_list:
      raise RetryException()

    print("Scraping page {} from section {}".format(page_number, current_section))

    parsed_product_list = BeautifulSoup(product_list.get_attribute('innerHTML'), 'html.parser')
    parsed_product_list = parsed_product_list.find_all('div', class_='vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--one pa4')

    print(f"Numbers of elements found {len(parsed_product_list)}")
    for product_section in parsed_product_list:

      product_section_content = product_section.select_one("section a article div.vtex-flex-layout-0-x-flexRowContent--product-info-down-mobile")

      if not product_section_content:
        raise RetryException()

      product_brand = product_section_content.select_one("span.vtex-product-summary-2-x-productBrandName").get_text() if product_section_content.select_one("span.vtex-product-summary-2-x-productBrandName") else None
      product_name = product_section_content.select_one("span.vtex-store-components-3-x-productBrand").get_text() if product_section_content.select_one("span.vtex-store-components-3-x-productBrand") else None
      product_price = product_section_content.select_one("div.exito-vtex-components-4-x-selling-price div.exito-vtex-components-4-x-PricePDP span.exito-vtex-components-4-x-currencyContainer").get_text().split() if product_section_content.select_one("span.exito-vtex-components-4-x-currencyContainer") else None
      product_price_unit = product_section_content.select_one("div.exito-vtex-components-4-x-validatePumValue").get_text().split(' a ') if product_section_content.select_one("div.exito-vtex-components-4-x-validatePumValue") else None

      product_unit_label, product_price_total, product_unit_price = calc_product_quantity(product_price, product_price_unit)

      product_quantity = round(product_price_total/product_unit_price) if product_price_total and product_unit_price else None

      fcontent.append(f"{product_brand},{product_name},{product_price_total},{product_quantity},{product_unit_price},{product_unit_label},{current_section}\n")
      print(f"Scraped {product_name}")
      df_index += 1

      #checkpoint every 100 items
      if df_index % 100 == 0:
        print("Checkpoint reached")
        fcsv.write(''.join(fcontent))
        fcontent = []

    page_number += 1
  except RetryException:
    print(f"Refreshing page {page_number} from section {current_section}")
    continue
  except Exception as e:
    print(e)
    print('error but still saving file...')
    fcsv.write(''.join(fcontent))
    continue

if not saved:
  driver.quit()
  fcsv.write(''.join(fcontent))
  fcsv.close()
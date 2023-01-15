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
import argparse
from utils import create_file, calc_product_quantity
from config import config

class RetryException(Exception):
  pass

def scraper(tienda, output_file):
  options = Options()
  options.headless = True
  driver = webdriver.Chrome(options=options)

  page_number = config['start_in_page']
  tienda_selectors = tienda['selectors']
  df_index = 1
  sections = tienda['sections']
  sections_idx = config['start_in_section_index']
  fcsv = open(output_file, "a")
  fcsv.write(config['file_headers'])
  fcontent = []

  retry_counts = 0
  
  while True:
    current_section = sections[sections_idx]
    try:

      driver.get(tienda['url'](current_section, page_number))

      time.sleep(config['explicit_waits']['initial_load'])

      product_list = None
      try:
          WebDriverWait(driver, config['explicit_waits']['webdriver_wait']).until(
              EC.presence_of_element_located((By.CSS_SELECTOR, tienda_selectors['first_element']))
          )
          print("Page {} from section {} loaded".format(page_number, current_section))

          for i in range(1,config['number_of_scrolls']+1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*{});".format(i/config['number_of_scrolls']))
            time.sleep(config['explicit_waits']['scroll'])

          time.sleep(config['explicit_waits']['items_list_load'])

          product_list = WebDriverWait(driver, config['explicit_waits']['webdriver_wait']).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, tienda_selectors['items_list_container']))
          )
      except TimeoutException:
        print(f"Could not find the layout of products for page {page_number} from section {current_section}")
        print("Checking if there are no elements...")
        retry_counts += 1
        if retry_counts == config['max_retries']:
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
      #print(parsed_product_list)
      parsed_product_list = parsed_product_list.find_all('div', class_=tienda_selectors['items_list_class'])

      print(f"Numbers of elements found {len(parsed_product_list)}")
      for product_section in parsed_product_list:

        product_section_content = product_section.select_one(tienda_selectors['product_section_content'])
        if not product_section_content:
          raise RetryException()
  
        product_brand = product_section_content.select_one(tienda_selectors['product_brand']).get_text() if product_section_content.select_one(tienda_selectors['product_brand']) else None
        product_name = product_section_content.select_one(tienda_selectors['product_name']).get_text() if product_section_content.select_one(tienda_selectors['product_name']) else None
        product_price = product_section_content.select_one(tienda_selectors['product_price']).get_text().split() if product_section_content.select_one(tienda_selectors['product_price']) else None
        product_price_unit = product_section_content.select_one(tienda_selectors['product_price_unit']).get_text().split(' a ') if product_section_content.select_one(tienda_selectors['product_price_unit']) else None

        product_unit_label, product_price_total, product_unit_price = calc_product_quantity(product_price, product_price_unit)

        product_quantity = round(product_price_total/product_unit_price) if product_price_total and product_unit_price else None

        fcontent.append(f"{product_brand},{product_name},{product_price_total},{product_quantity},{product_unit_price},{product_unit_label},{current_section}\n")
        print(f"Scraped {product_name}")
        df_index += 1

        #checkpoint to save elements to file
        if df_index % config['items_checkpoint'] == 0:
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

  driver.quit()
  fcsv.write(''.join(fcontent))
  fcsv.close()

if __name__ == "__main__":

  parser = argparse.ArgumentParser(
    prog = 'Mercado Parser',
    description = 'Parser de algunas páginas de mercado en Colombia! (Por ahora Éxito y Jumbo)')

  parser.add_argument('-t', '--tienda', type=str,
                    choices=['exito', 'jumbo', 'carulla'],
                    default='exito', required=True,
                    help='la tienda a la cual le quieres hacer scraping')

  parser.add_argument('-f', '--file', type=str, dest='file', default=None,
                    help='el nombre del archivo donde quieres guardar tu output')
  
  parser.add_argument('-fp', '--file_prefix', type=str, dest='file_prefix',
                    help='el nombre del prefijo del archivo donde quieres guardar tu output')

  args = parser.parse_args()

  scraper_config = config['tiendas'][args.tienda]
  if not scraper_config:
    raise Exception(f'La configuración para la tienda {args.tienda} no existe')

  default_output_path = os.path.join(os.getcwd(), "output", args.tienda)

  if not os.path.exists(default_output_path):
    print(f"Creating dir {default_output_path}")
    os.mkdir(default_output_path, 0o777)

  file_name = create_file(default_output_path, args.file, args.file_prefix)
  
  scraper(scraper_config, file_name)
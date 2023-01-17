from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from config import config as sconfig

class RetryException(Exception):
  pass

class MercadoScraper:
  def __init__(self, tienda, file_name, config=sconfig):
    self.tienda = tienda
    self.config = config
    self.file_name = file_name
    self.driver = None
    self._init_driver()
    self.page_number = config['start_in_page']
    self.tienda_selectors = tienda['selectors']
    self.df_index = 1
    self.sections = tienda['sections']
    self.sections_idx = config['start_in_section_index']
    self.fcontent = []
    self.retry_counts = 0
  
  def _init_driver(self):
    options = Options()
    options.headless = True
    self.driver = webdriver.Chrome(options=options)

  def calc_product_quantity(self, product_price_label, product_price_unit_label):
    if product_price_unit_label:
      return (product_price_unit_label[0][1:], float(product_price_label[1].replace('.', '').replace(',', '.')), float(product_price_unit_label[1][2:-1].replace('.', '').replace(',', '.')))
    else:
      return(None, 0, 0)

  def scrape(self):
    fcsv = open(self.file_name, "a")
    fcsv.write(self.config['file_headers'])
  
    while True:
      current_section = self.sections[self.sections_idx]
      try:

        self.driver.get(self.tienda['url'](current_section, self.page_number))

        time.sleep(self.config['explicit_waits']['initial_load'])

        product_list = None
        try:
            WebDriverWait(self.driver, self.config['explicit_waits']['webdriver_wait']).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.tienda_selectors['first_element']))
            )
            print("Page {} from section {} loaded".format(self.page_number, current_section))

            for i in range(1,self.config['number_of_scrolls']+1):
              self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight*{});".format(i/self.config['number_of_scrolls']))
              time.sleep(self.config['explicit_waits']['scroll'])

            time.sleep(self.config['explicit_waits']['items_list_load'])

            product_list = WebDriverWait(self.driver, self.config['explicit_waits']['webdriver_wait']).until(
              EC.presence_of_element_located((By.CSS_SELECTOR, self.tienda_selectors['items_list_container']))
            )
        except TimeoutException:
          print(f"Could not find the layout of products for page {self.page_number} from section {current_section}")
          print("Checking if there are no elements...")
          self.retry_counts += 1
          if self.retry_counts == self.config['max_retries']:
            if self.sections_idx == len(sections)-1:
              break
              print('breaking scraper, no more pages. reached page number {}'.format(self.page_number))
            print('finished section {}'.format(current_section))
            self.sections_idx+=1
            self.page_number = 1
            self.retry_counts = 0
            continue
          else:
            raise RetryException()
        except:
          raise RetryException()

        if not product_list:
          raise RetryException()

        print("Scraping page {} from section {}".format(self.page_number, current_section))

        parsed_product_list = BeautifulSoup(product_list.get_attribute('innerHTML'), 'html.parser')

        parsed_product_list = parsed_product_list.find_all('div', class_=self.tienda_selectors['items_list_class'])

        print(f"Numbers of elements found {len(parsed_product_list)}")
        for product_section in parsed_product_list:

          product_section_content = product_section.select_one(self.tienda_selectors['product_section_content'])
          if not product_section_content:
            raise RetryException()
    
          product_brand = product_section_content.select_one(self.tienda_selectors['product_brand']).get_text() if product_section_content.select_one(self.tienda_selectors['product_brand']) else None
          product_name = product_section_content.select_one(self.tienda_selectors['product_name']).get_text() if product_section_content.select_one(self.tienda_selectors['product_name']) else None
          product_price = product_section_content.select_one(self.tienda_selectors['product_price']).get_text().split() if product_section_content.select_one(self.tienda_selectors['product_price']) else None
          product_price_unit = product_section_content.select_one(self.tienda_selectors['product_price_unit']).get_text().split(' a ') if product_section_content.select_one(self.tienda_selectors['product_price_unit']) else None

          product_unit_label, product_price_total, product_unit_price = self.calc_product_quantity(product_price, product_price_unit)

          product_quantity = round(product_price_total/product_unit_price) if product_price_total and product_unit_price else None

          self.fcontent.append(f"{product_brand},{product_name},{product_price_total},{product_quantity},{product_unit_price},{product_unit_label},{current_section}\n")
          print(f"Scraped {product_name}")
          self.df_index += 1

          #checkpoint to save elements to file
          if self.df_index % self.config['items_checkpoint'] == 0:
            print("Checkpoint reached")
            fcsv.write(''.join(self.fcontent))
            self.fcontent = []

        self.page_number += 1
      except RetryException:
        print(f"Refreshing page {self.page_number} from section {current_section}")
        continue
      except KeyboardInterrupt as e:
        print('quitted app but saving file...')
        break
      except Exception as e:
        print(e)
        print('error but still saving file...')
        fcsv.write(''.join(self.fcontent))
        continue

    self.driver.quit()
    fcsv.write(''.join(self.fcontent))
    fcsv.close()
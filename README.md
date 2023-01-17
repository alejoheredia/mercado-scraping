#Mercado Scraping

It is a super simple CLI which aims to execute a web scraper to pull data from some of the web catalogs from big super markets in Colombia (Currently it supports Éxito, Jumbo and Carulla web catalogs). It will grab the products found and save it to a csv file.

## Requirements

- Python 3.X
- [Selenium (4.5.0)] (https://selenium-python.readthedocs.io/installation.html) 
- Webdriver for Selenium (For this project I used [Chrome]'s(https://sites.google.com/chromium.org/driver/?pli=1))

## Execute the scraper

```
$ python3 app.py -t exito
```

```
$python3 app.py -h

usage: Mercado Scraper [-h] -t {exito,jumbo,carulla} [-f FILE] [-fp FILE_PREFIX]

Scraper de algunas páginas de mercado en Colombia! (Por ahora Éxito, Jumbo y Carulla)

optional arguments:
  -h, --help            show this help message and exit
  -t {exito,jumbo,carulla}, --tienda {exito,jumbo,carulla}
                        la tienda a la cual le quieres hacer scraping
  -f FILE, --file FILE  el nombre del archivo donde quieres guardar tu output
  -fp FILE_PREFIX, --file_prefix FILE_PREFIX
                        el nombre del prefijo del archivo donde quieres guardar tu output
```

## Settings

In `config.py` file you'll find the configuration for the scraper and for each one of the supported market's web catalog.

Configuration for the web catalog looks like the following:

```python
"start_in_page": 1, # Catalog's page number where the web scraper starts
"start_in_section_index": 0,
"file_headers": "marca,nombre_producto,precio,cantidad,precio_unidad,unidad,seccion\n", #Generate CSV file headers
"max_retries": 3, #Maximum number of retries. A retry occurs when the page does not load correctly or no elements are found. Once the maximum number of retries has been reach, the scraper saves and quits
"items_checkpoint": 100, #The scraper will save to the CSV file each n parsed items
"number_of_scrolls": 12, #Number of times the scraper will scroll inside the catalog. On each scroll it will wait few seconds for it to load completely (As the catalogs are dynamically loaded)
"explicit_waits": { #In this objects the user can define some parameters regarding the wait times for some processes made by the scraper (integers represent seconds)
  "webdriver_wait": 5, #Initial wait
  "initial_load": 8, #First relevant element to load
  "scroll": 0.4, #Delay on each scroll
  "items_list_load": 3 #Explicit wait for all elements to load
}

```

For each store (tienda), there's the following structure (Will use exito's config as an example):

```python
"exito": {
    "url": lambda current_section, page_number: f"https://www.exito.com/mercado/{current_section}/?layout=one&page={page_number}", #Builds a string with the right url for the scraper
    "sections": ['despensa', 'lacteos-huevos-y-refrigerados', 'pollo-carne-y-pescado', 'frutas-y-verduras', 'despensa/enlatados-y-conservas', 'delicatessen', 'vinos-y-licores', 'snacks', 'panaderia-y-reposteria', 'aseo-del-hogar', 'despensa/bebidas'], #Array with the most common "sections" (aisles ?) found in the web catalog
    "selectors": { #CSS selectors for relevant information regarding the products in the catalog
      "first_element": ".vtex-search-result-3-x-totalProductsMessage",
      "items_list_container": "#gallery-layout-container",
      "items_list_class": "vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--one pa4",
      "product_section_content": "section a article div.vtex-flex-layout-0-x-flexRowContent--product-info-down-mobile",
      "product_brand": "span.vtex-product-summary-2-x-productBrandName",
      "product_name": "span.vtex-store-components-3-x-productBrand",
      "product_price": "div.exito-vtex-components-4-x-selling-price div.exito-vtex-components-4-x-PricePDP span.exito-vtex-components-4-x-currencyContainer",
      "product_price_unit": "div.exito-vtex-components-4-x-validatePumValue"
    }
  }
```

## Contributing

If you wish to contribute, please feel free to open a PR or create a new issue :D
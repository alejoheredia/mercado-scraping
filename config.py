tiendas = {
  "exito": {
    "url": lambda current_section, page_number: f"https://www.exito.com/mercado/{current_section}/?layout=one&page={page_number}",
    "sections": ['despensa', 'lacteos-huevos-y-refrigerados', 'pollo-carne-y-pescado', 'frutas-y-verduras', 'despensa/enlatados-y-conservas', 'delicatessen', 'vinos-y-licores', 'snacks', 'panaderia-y-reposteria', 'aseo-del-hogar', 'despensa/bebidas'],
    "selectors": {
      "first_element": ".vtex-search-result-3-x-totalProductsMessage",
      "items_list_container": "#gallery-layout-container",
      "items_list_class": "vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--one pa4",
      "product_section_content": "section a article div.vtex-flex-layout-0-x-flexRowContent--product-info-down-mobile",
      "product_brand": "span.vtex-product-summary-2-x-productBrandName",
      "product_name": "span.vtex-store-components-3-x-productBrand",
      "product_price": "div.exito-vtex-components-4-x-selling-price div.exito-vtex-components-4-x-PricePDP span.exito-vtex-components-4-x-currencyContainer",
      "product_price_unit": "div.exito-vtex-components-4-x-validatePumValue"
    }
  },
  "carulla": {
    "url": lambda current_section, page_number: f"https://www.carulla.com/{current_section}/?layout=one&page={page_number}",
    "sections": ['despensa', 'lacteos-huevos-y-refrigerados', 'pollo-carnes-y-pescado', 'frutas-y-verduras', 'despensa/enlatados-y-conservas', 'delicatessen', 'vinos-y-licores', 'snacks', 'limpieza-del-hogar', ],
    "selectors": {
      "first_element": ".vtex-search-result-3-x-totalProductsMessage",
      "items_list_container": "#gallery-layout-container",
      "items_list_class": "vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--one pa4",
      "product_section_content": "section a article div.vtex-flex-layout-0-x-flexRowContent--product-info-down-mobile",
      "product_brand": "span.vtex-product-summary-2-x-productBrandName",
      "product_name": "span.vtex-store-components-3-x-productBrand",
      "product_price": "div.exito-vtex-components-4-x-selling-price div.exito-vtex-components-4-x-PricePDP span.exito-vtex-components-4-x-currencyContainer",
      "product_price_unit": "div.exito-vtex-components-4-x-validatePumValue"
    }
  },
  "jumbo": {
    "url": lambda current_section, page_number: f"https://www.tiendasjumbo.co/supermercado/{current_section}/?layout=grid&page={page_number}",
    "sections": ['despensa', 'lacteos-huevos-y-refrigerados', 'carne-y-pollo', 'frutas-y-verduras', 'despensa/enlatados-y-conservas', 'charcuteria', 'vinos-y-licores', 'pasabocas', 'aseo-del-hogar', ],
    "selectors": {
      "first_element": ".vtex-search-result-3-x-totalProductsMessage",
      "items_list_container": "#gallery-layout-container",
      "items_list_class": "vtex-search-result-3-x-galleryItem",
      "product_section_content": "section a article > div",
      "product_brand": "span.vtex-product-summary-2-x-productBrandName",
      "product_name": "span.vtex-product-summary-2-x-productBrand",
      "product_price": "div.tiendasjumboqaio-jumbo-minicart-2-x-price",
      "product_price_unit": ".tiendasjumboqaio-calculate-pum-2-x-PUMInfo"
    }
  }
}

config = {
  "start_in_page": 1,
  "start_in_section_index": 0,
  "file_headers": "marca,nombre_producto,precio,cantidad,precio_unidad,unidad,seccion\n",
  "max_retries": 3,
  "items_checkpoint": 100,
  "number_of_scrolls": 12,
  "explicit_waits": {
    "webdriver_wait": 5,
    "initial_load": 8,
    "scroll": 0.4,
    "items_list_load": 3
  },
  "tiendas": tiendas
}
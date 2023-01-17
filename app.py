import os
import argparse
from utils import create_file
from config import config
from scraper import MercadoScraper

if __name__ == "__main__":

  parser = argparse.ArgumentParser(
    prog = 'Mercado Scraper',
    description = 'Scraper de algunas páginas de mercado en Colombia! (Por ahora Éxito, Jumbo y Carulla)')

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

  new_scraper = MercadoScraper(scraper_config, file_name)
  new_scraper.scrape()
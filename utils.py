from datetime import datetime
import os

def create_file(path, filename=None, prefix='output'):
  fname = filename if filename and filename.endswith('.csv') else f"{filename}.csv"

  if os.path.exists(fname):
    raise Exception('File already exists')

  if not filename:
    if not prefix:
      prefix = 'output'

    fname = f'{prefix}_{datetime.now().strftime("%m-%d-%YT%H_%M_%S")}.csv'

  fpath = os.path.join(path, fname)
  open(fpath, 'a')
  return fpath

def calc_product_quantity(product_price_label, product_price_unit_label):
  if product_price_unit_label:
    return (product_price_unit_label[0][1:], float(product_price_label[1].replace('.', '').replace(',', '.')), float(product_price_unit_label[1][2:-1].replace('.', '').replace(',', '.')))
  else:
    return(None, 0, 0)
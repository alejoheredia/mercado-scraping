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
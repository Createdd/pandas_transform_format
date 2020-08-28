# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3.7.6 64-bit
#     language: python
#     name: python37664bitcec5513a60ce49909c4b87b3ad0ec34d
# ---

# +
import sys  # module for python interpreter
sys.path.append('../')  # necessary for relative import of utils file e.g.

import os
import requests

import pandas as pd


from IPython.core.interactiveshell import InteractiveShell
# # %load_ext autoreload
# # %autoreload 2
# # # %matplotlib inline
# # %config IPCompleter.greedy=True

# pd.options.display.max_columns = None
# pd.options.display.max_rows = 200
# sns.set_palette("bright")
# sns.set(style="darkgrid")

InteractiveShell.ast_node_interactivity = "all"


# -

# # Load dataset

# +
def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


download('https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv', './data')

# -

# # Transform data

# +
df = pd.read_csv('./data/titanic.csv')
# df = pd.read_json('./data/titanic.json')

df.to_json(r'./data/titanic.json')

df.columns
df
# -



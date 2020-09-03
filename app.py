import json
import os

import pandas as pd
from flask import Flask, request, send_from_directory, abort


app = Flask(__name__)
UPLOAD_DIRECTORY = "."

conversions = ['h5', 'pkl', 'feather', 'parquet' ]

@app.route('/', methods=['GET'])
def home():
    return 'This app provides data format transformation!'


@app.route('/download', methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        provided_data = request.files.get('file')
        if provided_data is None:
            return 'Please enter valid excel format ', 400
        provided_format = request.form.get('format')
        if provided_format is None:
            return f'Please enter valid format to convert.', 400
        if provided_format not in conversions:
            return f'Please enter valid format to convert. Can be {list(conversions)}', 400

        df = pd.read_csv(provided_data)
        file_name = f'converted.{provided_format}'
        path = f'./{file_name}'

        if provided_format == 'h5':
            df.to_hdf(
                path,
                file_name,
                mode='w')
        elif provided_format == 'pkl':
            df.to_pickle(path)
        elif provided_format == 'parquet':
            df.to_pickle(path)
        elif provided_format == 'feather':
            df.to_pickle(path)

        try:
            return send_from_directory(UPLOAD_DIRECTORY, filename=file_name, as_attachment=True)
        except FileNotFoundError:
            abort(404)
        finally:
            remove_file(path)

def remove_file(new_file):
    path = os.path.join(UPLOAD_DIRECTORY, new_file)
    os.remove(path)


@app.route('/get_json', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        provided_data = request.files.get('file')
        if provided_data is None:
            return 'Please enter valid excel format ', 400

        data = provided_data
        df = pd.read_csv(data)
        transformed = df.to_json()

        result = {
            'result': transformed,
        }

        json.dumps(result)

        return result

if __name__ == '__main__':
    app.run()
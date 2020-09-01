import json
import os
import pandas as pd

from flask import Flask, request, jsonify, send_file, send_from_directory, abort
import flask_excel as excel

import io

app = Flask(__name__)
UPLOAD_DIRECTORY = "."

@app.route('/', methods=['GET'])
def home():
    return 'This app provides data format transformation!'


@app.route('/download', methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        provided_data = request.files.get('file')
        if provided_data is None:
            return 'Please enter valid excel format ', 400

        data = provided_data
        df = pd.read_csv(data)

        file_name = 'titanic_data.h5'
        path = f'./{file_name}'

        df.to_hdf(
            path,
            file_name,
            mode='w')

        try:
            return send_from_directory(UPLOAD_DIRECTORY, filename=file_name, as_attachment=True)
        except FileNotFoundError:
            abort(404)
        finally:
            remove_file(path)

def remove_file(new_file):
    path = os.path.join(UPLOAD_DIRECTORY, new_file)
    os.remove(path)


@app.route('/upload', methods=['GET', 'POST'])
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
    # app.run(debug=True)
    excel.init_excel(app)
    app.run()
import json
import pandas as pd

from flask import Flask, request, jsonify
import flask_excel as excel


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'This app provides data format transformation!'


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
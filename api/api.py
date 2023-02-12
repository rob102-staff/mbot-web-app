from flask import Flask
from flask_cors import CORS, cross_origin

from package_scanner import load_packages

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/packages/list')
def list_packages():
    packages = load_packages()
    return {"packages": [package.as_dict() for package in packages]}

from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request

from package_scanner import load_packages

import subprocess
import os

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/packages/list', methods=['GET'])
def list_packages():
    packages = load_packages()
    return {"packages": [package.as_dict() for package in packages]}

@app.route('/packages/uninstall', methods=['POST'])
def uninstall_package():
    """Uninstall a package"""

    # get the package name from the request body
    package_name = request.json.get("name")

    if not package_name:
        return {"success": False, "error": "Package name not provided"}
    
    # uninstall the package
    print(f"mbotter uninstall \"{package_name}\"")
    output = subprocess.check_output(f"mbotter uninstall \"{package_name}\"", shell=True)

    if("not" in output.decode("utf-8")):
        return {"success": False, "error": "Package not found"}

    return {"success": True}
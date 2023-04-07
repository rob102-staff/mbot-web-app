from flask import Flask
from flask_cors import CORS
from flask import request

from waitress import serve

import storage_api
import package_utils

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/ping', methods=['GET'])
def ping():
    return {"success": True}

@app.route('/packages/list', methods=['GET'])
def list_packages():
    packages = package_utils.load_packages()
    return {"packages": [package.as_dict() for package in packages]}

@app.route('/packages/uninstall', methods=['POST'])
def uninstall_package():
    """Uninstall a package"""

    # get the package name from the request body
    package_name = request.json.get("name")

    if not package_name:
        return {"success": False, "error": "Package name not provided"}
    
    success = package_utils.remove_package(package_name)

    if not success:
        return {"success": False, "error": "Package install failed."}

    return {"success": True}

@app.route('/packages/install', methods=['POST'])
def install_package():
    """Install a package"""

    # get the package name from the request body
    package_url = request.json.get("url")
    
    # get the branch, if it exists
    branch = request.json.get("branch", "deploy")

    if not package_url:
        return {"success": False, "error": "Package url not provided"}

    success, msg = package_utils.install_git_package(package_url, branch=branch, overwrite=True)

    print(success, msg)

    if not success:
        return {"success": False, "error": "msg"}
    
    return {"success": True}

@app.route('/storage/keyvalue/<store>/', methods=['GET','POST'])
def keyvalue(store: str):
    """Get key value on GET and set key value on POST"""

    # get the key from the request body
    key = request.json.get("key")

    if not key:
        return {"success": False, "error": "Key not provided"}

    # check if the key value store exists
    if not storage_api.check_keyvalue_store_exists(store):
        return {"success": False, "error": "Key value store does not exist"}

    if request.method == 'GET':
        # get the key value, if it exists.
        # otherwise return None
        value = storage_api.get_keyvalue(store, key) 
        return {"success": True, "value": value}

    elif request.method == 'POST':

        # get the value from the request body
        value = request.json.get("value")

        if not value:
            return {"success": False, "error": "Value not provided"}

        # set the key value
        storage_api.set_keyvalue(store, key, value)

        return {"success": True}

@app.route('/storage/keyvalue/<store>/all/', methods=['GET'])
def keyvalue_all(store: str):
    """Get all key values"""

    # check if the key value store exists
    if not storage_api.check_keyvalue_store_exists(store):
        return {"success": False, "error": "Key value store does not exist"}

    # get all key values
    keyvalues = storage_api.get_all_keyvalues(store)

    return {"success": True, "keyvalues": keyvalues}

@app.route('/storage/create/', methods=['POST'])
def create_store():
    """Create a key value store"""

    # get the store name from the request body
    store = request.json.get("store")

    if not store:
        return {"success": False, "error": "Store name not provided"}

    if storage_api.check_keyvalue_store_exists(store):
        return {"success": False, "error": "Store already exists"}

    # create the key value store
    success = storage_api.create_keyvalue_store(store)

    if not success:
        return {"success": False, "error": "An error occured while creating the store"}
    
    return {"success": True}

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
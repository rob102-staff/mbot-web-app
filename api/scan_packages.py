import os
import json

## current file location
loc = os.path.dirname(os.path.realpath(__file__))
## location of the packages folder
package_location = os.path.join(loc, 'packages')

if os.environ.get('DEVELOPMENT_INSTALL') is not None:
    print('DEVELOPMENT_INSTALL is set')

def scan_packages():
    # return all folders in the packages folder
    return [name for name in os.listdir(package_location) if os.path.isdir(os.path.join(package_location, name))]

def package_metadata(package_name):
    # return the metadata.json file in the package folder, if it exists
    metadata_file = os.path.join(package_location, package_name, 'metadata.json')
    if os.path.isfile(metadata_file):
        with open(metadata_file) as f:
            return json.load(f)
    else:
        return {}

def package_uri(package_name):
    # return the file location of the package folder
    path = os.path.join(package_location, package_name)

    # check for the metadata.json file
    metadata_file = os.path.join(path, 'metadata.json')

    # read the metadata file
    if os.path.isfile(metadata_file):
        with open(metadata_file) as f:
            metadata = json.load(f)
    else:
        return ""
    
    # get the entry variable from the json
    entry = metadata['entry']

    # return the path to the entry file
    return os.path.join(path, entry)
import os
import json

DEFAULT_PACKAGE_PATH = "/data/www/mbot/packages"

class Package:

    def __init__(self, path: str):
        self.path = path
        self.name = self.path.split("/")[-1]
        
        self._read_metadata()

        self.author = self.metadata["author"]
        self.description = self.metadata["description"]
        self.version = self.metadata["version"]
        self.name = self.metadata["name"]
        self.html_file = self.metadata["html_file"]
        self.h = self._hash()
        self.hidden = self.metadata["hidden"]

    def as_dict(self):
        return {
            "name": self.name,
            "author": self.author,
            "description": self.description,
            "version": self.version,
            "html_file": self.html_file,
            "uuid": self.h,
            "URI": "/packages/" + self.h + "/" + self.html_file,
            "hidden": self.hidden
        }

    def full_path(self):
        return self.path + "/" + self.html_file

    def get_uuid(self):
        return self.h

    def get_metadata(self):
        return self._metadata
    
    def get_name(self):
        return self._name
    
    def get_path(self):
        return self._path

    def get_author(self):
        return self._author

    def get_description(self):
        return self._description
    
    def get_version(self):
        return self._version
    
    def get_html_file(self):
        return self.html_file
    
    def is_valid(self):
        return self.html_file != ""

    def _hash(self):
        # the hash is equal to the name of the folder containing the package
        return self.path.split("/")[-1]

    def _read_metadata(self):
        
        #check that the package has a metadata file
        if not os.path.exists(self.path + "/metadata.json"):
            self.metadata = {}
        
        else:
            #read the metadata file
            with open(self.path + "/metadata.json", "r") as f:
                self.metadata = json.load(f)
            
        self._validate_metadata() 
    
    def _validate_metadata(self):

        # check that the metadata file has the required fields
        
        if "name" not in self.metadata:
            self.metadata["name"] = self.name # if not, use the package name

        if "description" not in self.metadata:
            self.metadata["description"] = ""

        if "author" not in self.metadata:
            self.metadata["author"] = ""

        if "version" not in self.metadata:
            self.metadata["version"] = ""
        
        if "html_file" not in self.metadata and "entry" not in self.metadata:
            self.metadata["html_file"] = ""

        elif "entry" in self.metadata and "html_file" not in self.metadata:
            self.metadata["html_file"] = self.metadata["entry"]
    
        if "hidden" not in self.metadata:
            self.metadata["hidden"] = False

def load_packages(path: str = DEFAULT_PACKAGE_PATH):
    return _load_packages(path)

def _load_packages(path: str):

    packages = []

    # load all folders in the path
    # if the folder has a metadata file and is valid, add it to the list

    for folder in os.listdir(path):

        # skip if not a folder
        if not os.path.isdir(path + "/" + folder):
            continue

        package = Package(path + "/" + folder)
        if package.is_valid():
            packages.append(package)

    return packages 


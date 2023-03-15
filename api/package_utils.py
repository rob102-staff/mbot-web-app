from typing import Tuple
import hashlib
import json
import os
import shutil
import git

DEFAULT_PACKAGE_PATH = "/data/www/mbot/packages"
DEFAULT_INSTALL_PATH = "/data/www/mbot/packages"
GIT_CLONE_PATH = "/data/www/mbot/git/tmp"

def load_packages(path: str = DEFAULT_PACKAGE_PATH):
    return _load_packages(path)

def _load_packages(path: str):

    packages = []

    # load all folders in the path
    # if the folder has a metadata file and is valid, add it to the list

    for folder in os.listdir(path):

        # skip if not a folder
        if not os.path.isdir(path + "/" + folder):
            print("skipping " + folder + " because it is not a folder")
            continue

        package = Package(path + "/" + folder)
        if package.is_valid():
            packages.append(package)
        else:
            print("skipping " + folder + " because it is not valid")

    return packages 

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
        self.uuid = self.h
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

def generate_uuid(name, author, version, description, html_file):
    # generate a UUID
    # the UUID is a hash of the package name, author, version, description, and entry html file
    # created with the hashlib library with a sha256 hash

    # create a string with all the data
    data = name + author + version + description + html_file

    # create a sha256 hash object
    h = hashlib.sha256()

    # update the hash with the data
    h.update(data.encode("utf-8"))

    # return the hex digest of the hash
    return h.hexdigest()

def validate_metadata(metadata):
    # validate the metadata
    # make sure it has all the required keys
    # return True if the metadata is valid, False if not

    required_keys = ["name", "author", "version", "description", "html_file", "uuid"]

    for key in required_keys:
        if not key in metadata:
            return False

    return True

def check_for_metadata(path: str):
    # check if the current directory has a metadata.json file
    # return True if it does, False if not

    return os.path.exists(path + "/metadata.json")

def check_for_file(filename: str, path: str):
    # check if the current directory has a metadata.json file
    # return True if it does, False if not

    return os.path.exists(f"{path}/{filename}")

def clone_package(url: str, branch: str, location: str = GIT_CLONE_PATH, overwrite: bool = True) -> bool:
    """clone a package from a git repository"""

    # Remove the location if it exists and overwrite is True
    if overwrite:
        if os.path.exists(location):
            shutil.rmtree(location)

    # Create the install location
    os.makedirs(location, exist_ok=True)

    # Clone the repository
    try:
        git.Repo.clone_from(url, location, branch=branch)
    except Exception as e:
        return False
    
    return True

def remove_package(package_name: str) -> bool:
    """Remove a package by name."""

    packages = load_packages() 
    package_names = [package.name for package in packages]

    if not package_name in package_names:
        return False

    uuid = packages[package_names.index(package_name)].uuid
    shutil.rmtree(os.path.join(DEFAULT_PACKAGE_PATH, uuid))
    return True

def install_package(path: str, overwrite: bool = True) -> Tuple[bool, str]:
    """Install a package located in folder path"""

    if not check_for_metadata(path):
        return False, "No metadata.json file found"

    with open(path + "/metadata.json", "r") as f:
        metadata = json.load(f)
    
    if not validate_metadata(metadata):
        return False, "Invalid metadata.json file."
    
    if os.path.exists(DEFAULT_PACKAGE_PATH + "/" + metadata["uuid"]):
        if overwrite:
            shutil.rmtree(DEFAULT_PACKAGE_PATH + "/" + metadata["uuid"])
        else:
            return False, "Package already installed."
    
    shutil.copytree(path, DEFAULT_PACKAGE_PATH + "/" + metadata["uuid"])
    return True, "Package installed successfully."

def generate_metadata(name: str, author: str, version: str, description: str, html_file: str, uuid: str, hidden: bool = False):
    # create a metadata.json file in the current directory
    # the metadata file contains the name, author, version, description, and entry html file of the package
    # the metadata file is used to validate the package and to display information about the package

    # create a dictionary with the metadata
    metadata = {
        "name": name,
        "author": author,
        "version": version,
        "description": description,
        "html_file": html_file,
        "uuid": uuid,
        "hidden": hidden
    }

    return metadata

def install_git_package(url: str, branch: str, overwrite: bool = True) -> Tuple[bool, str]:
    """Install a package from a git repository"""

    # Clone the repository
    if not clone_package(url, branch, overwrite=overwrite):
        return False, "Failed to clone repository."
    
    # Install the package
    status, message = install_package(GIT_CLONE_PATH, overwrite=overwrite)
    return status, message
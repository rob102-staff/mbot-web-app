#!/usr/bin/env python3

import typer
import colorama
import hashlib
import json
import os
import shutil

app = typer.Typer()

DEFAULT_PACKAGE_PATH = "/data/www/mbot/packages"
DEFAULT_INSTALL_PATH = "/data/www/mbot/packages"

class Package:

    def __init__(self, path: str):
        self.path = path
        self.name = self.path.split("/")[-1]
        
        self._read_metadata()

        self.author = self.metadata["author"]
        self.description = self.metadata["description"]
        self.version = self.metadata["version"]
        self.html_file = self.metadata["html_file"]
        self.name = self.metadata["name"]
        self.h = self._hash()
        self.uuid = self.h

    def as_dict(self):
        return {
            "name": self.name,
            "author": self.author,
            "description": self.description,
            "version": self.version,
            "html_file": self.html_file,
            "uuid": self.h,
            "URI": "/packages/" + self.h + "/" + self.html_file,
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



# list packages, install package, uninstall package, fix packages, generate metadata

# list packages command. Named "list" for brevity
@app.command()
def listall():
    """List all installed packages."""
    packages = load_packages()

    typer.echo(f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}Found {len(packages)} mbot package{'s' if len(packages) - 1 else ''}!\n\
                    {colorama.Style.RESET_ALL}")

    for package in packages:
        # print the package name in bold and green
        typer.echo(f"Package: {colorama.Style.BRIGHT}{package.name}{colorama.Style.RESET_ALL}")
        typer.echo(f"\tname: {package.name}")
        typer.echo(f"\tDescription: {package.description}")
        typer.echo(f"\tAuthor: {package.author}")
        typer.echo(f"\tVersion: {package.version}")
        typer.echo(f"\tEntry HTML File: {package.html_file}")
        typer.echo(f"\tPath: {package.path}")
        typer.echo(f"\tUUID: {package.uuid}")
        typer.echo("\n")

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

def check_for_metadata():
    # check if the current directory has a metadata.json file
    # return True if it does, False if not

    return os.path.exists("metadata.json")

@app.command()
def generate_metadata():
    """Generate a metadata file for your package."""
    # package name, author, version, description, entry html file
    # ask for each of these, then write to metadata.json
    
    typer.echo(f"{colorama.Style.BRIGHT}Welcome to the metadata generator!{colorama.Style.RESET_ALL}")
    typer.echo("Let's get started by generating a metadata file for your package.")
    typer.echo("You can always edit this file later, but it's best to get it right the first time.")
    typer.echo("Let's get started!\n")
    
    name = typer.prompt("Package name")
    author = typer.prompt("Author")
    version = typer.prompt("Version")
    description = typer.prompt("Description")
    html_file = typer.prompt("Entry HTML file (default index.html)", default="index.html")

    metadata = {
        "name": name,
        "author": author,
        "version": version,
        "description": description,
        "html_file": html_file,
        "uuid": generate_uuid(name, author, version, description, html_file)
    }

    typer.echo(f"{colorama.Fore.GREEN}\nMetadata generated! Here it is:{colorama.Style.RESET_ALL}")
    typer.echo(metadata)

    typer.echo(f"\n{colorama.Fore.GREEN}Writing metadata to metadata.json...{colorama.Style.RESET_ALL}")
    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    
    typer.echo(f"{colorama.Fore.GREEN}Done!{colorama.Style.RESET_ALL}")

@app.command()
def update_uuid():
    """check for metadata.json, then update the UUID"""
    if not check_for_metadata():
        typer.echo(f"{colorama.Fore.RED}metadata.json not found!{colorama.Style.RESET_ALL}")
        typer.echo("Please run 'generate-metadata' in your package directory first.")
        return

    typer.echo(f"{colorama.Fore.GREEN}Updating UUID...{colorama.Style.RESET_ALL}")
    with open("metadata.json", "r") as f:
        metadata = json.load(f)
    
    if not validate_metadata(metadata):
        typer.echo(f"{colorama.Fore.RED}Invalid metadata!{colorama.Style.RESET_ALL}")
        typer.echo("Please run 'generate-metadata' in your package directory first.")
        return

    metadata["uuid"] = generate_uuid(metadata["name"], metadata["author"], metadata["version"], metadata["description"], metadata["html_file"])

    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    
    typer.echo(f"{colorama.Fore.GREEN}Done!{colorama.Style.RESET_ALL}")

@app.command()
def install():
    """check for metadata.json, then copy to packages directory"""
    if not check_for_metadata():
        typer.echo(f"{colorama.Fore.RED}metadata.json not found!{colorama.Style.RESET_ALL}")
        typer.echo("Please run 'generate-metadata' in your package directory first.")
        return
    
    metadata = None
    with open("metadata.json", "r") as f:
        metadata = json.load(f)
    
    if not validate_metadata(metadata):
        typer.echo(f"{colorama.Fore.RED}Invalid metadata!{colorama.Style.RESET_ALL}")
        typer.echo("Please run 'generate-metadata' in your package directory first.")
        return
    
    typer.echo(f"{colorama.Fore.GREEN}Installing package...{colorama.Style.RESET_ALL}")

    # check if the package is already installed
    if os.path.exists(os.path.join(DEFAULT_INSTALL_PATH, metadata["uuid"])):
        typer.echo(f"{colorama.Fore.RED}Package already installed! Overwrite?{colorama.Style.RESET_ALL}")
        
        if not typer.confirm("Overwrite?"):
            typer.echo(f"{colorama.Fore.RED}Aborting...{colorama.Style.RESET_ALL}")
            return
        
        typer.echo(f"{colorama.Fore.GREEN}Overwriting...{colorama.Style.RESET_ALL}")
        shutil.rmtree(os.path.join(DEFAULT_INSTALL_PATH, metadata["uuid"]))

    # First make a folder in the packages directory with the UUID as the name
    os.mkdir(os.path.join(DEFAULT_INSTALL_PATH, metadata["uuid"]))

    # Copy all the files in the current directory to the new folder
    for file in os.listdir("."):
        # copy all files and folders
        if os.path.isdir(file):
            shutil.copytree(file, os.path.join(DEFAULT_INSTALL_PATH, metadata["uuid"], file))
        else:
            shutil.copy(file, os.path.join(DEFAULT_INSTALL_PATH, metadata["uuid"], file))

    typer.echo(f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}Done!{colorama.Style.RESET_ALL}")

@app.command()
def uninstall(package_name: str):
    """uninstall a package by name"""
    # check if the package exists
    # if it does, delete the folder
    # if not, print an error message

    # get a list of all the packages
    packages = load_packages()

    package_names = [package.name for package in packages]

    if not package_name in package_names:
        typer.echo(f"{colorama.Fore.RED}Package not found!{colorama.Style.RESET_ALL}")
        return
    
    uuid = packages[package_names.index(package_name)].uuid

    typer.echo(f"{colorama.Fore.GREEN}Uninstalling package...{colorama.Style.RESET_ALL}")

    shutil.rmtree(os.path.join(DEFAULT_INSTALL_PATH, uuid))

    typer.echo(f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}Done!{colorama.Style.RESET_ALL}")
    
@app.command()
def shake_unusable():
    """Shake the unusable packages from the packages directory"""
    typer.echo(f"{colorama.Fore.GREEN}Shaking packages directory...{colorama.Style.RESET_ALL}")
    
    # get a list of all the packages
    packages = load_packages()

    # get a list of all the folders in the packages directory
    folders = os.listdir(DEFAULT_INSTALL_PATH)

    # loop through the folders
    for folder in folders:
        if folder == "default":
            continue
    
        # if the folder does not contain a metadata.json file, ask the user if they want to delete it
        if not os.path.exists(os.path.join(DEFAULT_INSTALL_PATH, folder, "metadata.json")):
            typer.echo(f"{colorama.Fore.RED}Found unusable package!{colorama.Style.RESET_ALL}")
            typer.echo(f"{colorama.Fore.RED}Folder: {colorama.Style.RESET_ALL}{folder}")
            typer.echo(f"{colorama.Fore.RED}Path: {colorama.Style.RESET_ALL}{os.path.join(DEFAULT_INSTALL_PATH, folder)}")

            if not typer.confirm("Delete?"):
                typer.echo(f"{colorama.Fore.RED}Skipping...{colorama.Style.RESET_ALL}")
                continue

            typer.echo(f"{colorama.Fore.GREEN}Deleting...{colorama.Style.RESET_ALL}")
            shutil.rmtree(os.path.join(DEFAULT_INSTALL_PATH, folder))

    typer.echo(f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}Done!{colorama.Style.RESET_ALL}")

@app.command()
def add_remote_package(url, from_git=False):
    """
    Add a remote package to the packages directory.
    If the package is from git, it will be cloned. Otherwise, a remote package will be created.
    """

    if from_git:
        install_package_from_git(url)
    else:
        install_package_from_url(url)

def install_package_from_git(url):
    """Clone the git repo into /data/mbot/tmp/ and then run the install command"""

    # clone the repo
    
    pass



def install_package_from_url(url):
    pass

if __name__ == "__main__":
    app()
#!/usr/bin/env python3

import typer
import colorama
import hashlib
import json
import os
import shutil
import git

import utils
from utils import load_packages, Package, generate_uuid, validate_metadata, check_for_file, check_for_metadata, clone_package, remove_package, install_package
from utils import DEFAULT_INSTALL_PATH, DEFAULT_PACKAGE_PATH, GIT_CLONE_PATH

app = typer.Typer()

CURRENT_EXECUTION_PATH = os.getcwd()

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
        typer.echo(f"\tHidden: {package.hidden}")
        typer.echo("\n")

def generate_metadata_at(path: str = CURRENT_EXECUTION_PATH):
    """Generate a metadata file for your package."""
    typer.echo(f"{colorama.Style.BRIGHT}Welcome to the metadata generator!{colorama.Style.RESET_ALL}")
    typer.echo("Let's get started by generating a metadata file for your package.")
    typer.echo("You can always edit this file later, but it's best to get it right the first time.")
    typer.echo("Let's get started!\n")
    
    name = typer.prompt("Package name")
    author = typer.prompt("Author")
    version = typer.prompt("Version")
    description = typer.prompt("Description")
    hidden = typer.confirm("Hidden?", default=False)
    html_file = typer.prompt("Entry HTML file (default index.html)", default="index.html")
    remote_package = typer.confirm("Remote package?", default=False)
    remote_url = "" 
    if remote_package:
        remote_url = typer.prompt("Remote URL")

    metadata = utils.generate_metadata(
        name=name,
        author=author,
        version=version,
        description=description,
        html_file=html_file,
        uuid=generate_uuid(name, author, version, description, html_file),
        hidden=hidden,
        remote_package=remote_package,
        remote_url=remote_url)

    typer.echo(f"{colorama.Fore.GREEN}\nMetadata generated! Here it is:{colorama.Style.RESET_ALL}")
    typer.echo(metadata)

    typer.echo(f"\n{colorama.Fore.GREEN}Writing metadata to metadata.json...{colorama.Style.RESET_ALL}")
    with open(path + "/metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    
    typer.echo(f"{colorama.Fore.GREEN}Done!{colorama.Style.RESET_ALL}")

@app.command()
def generate_metadata(path: str = CURRENT_EXECUTION_PATH):
    """Generate a metadata file for your package."""
    # package name, author, version, description, entry html file
    # ask for each of these, then write to metadata.json
    generate_metadata_at(path)
    

@app.command()
def update_uuid(path: str = CURRENT_EXECUTION_PATH):
    """check for metadata.json, then update the UUID"""
    if not check_for_metadata(path):
        typer.echo(f"{colorama.Fore.RED}metadata.json not found!{colorama.Style.RESET_ALL}")
        typer.echo("Please run 'generate-metadata' in your package directory first.")
        return

    typer.echo(f"{colorama.Fore.GREEN}Updating UUID...{colorama.Style.RESET_ALL}")
    with open(path + "/metadata.json", "r") as f:
        metadata = json.load(f)
    
    if not validate_metadata(metadata):
        typer.echo(f"{colorama.Fore.RED}Invalid metadata!{colorama.Style.RESET_ALL}")
        typer.echo("Please run 'generate-metadata' in your package directory first.")
        return

    metadata["uuid"] = generate_uuid(metadata["name"], metadata["author"], metadata["version"], metadata["description"], metadata["html_file"])

    with open(path + "/metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    
    typer.echo(f"{colorama.Fore.GREEN}Done!{colorama.Style.RESET_ALL}")

@app.command()
def install():
    """check for metadata.json, then copy to packages directory"""

    typer.echo(f"{colorama.Fore.GREEN}Installing package...{colorama.Style.RESET_ALL}")

    install_result, msg = install_package(CURRENT_EXECUTION_PATH, overwrite=False) # install to the default install path

    if msg == "Package already installed.":
        # ask if they want to overwrite
        overwrite = typer.confirm("Package already installed. Overwrite?")
        if overwrite:
            install_result, msg = install_package(CURRENT_EXECUTION_PATH, overwrite=True)
    
    if install_result:
        typer.echo(f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}Install Complete!{colorama.Style.RESET_ALL}")

    else:
        typer.echo(f"{colorama.Fore.RED}{colorama.Style.BRIGHT}Install Failed!\nReason: {msg}{colorama.Style.RESET_ALL}")

@app.command()
def uninstall(package_name: str):
    """uninstall a package by name"""
    typer.echo(f"{colorama.Fore.GREEN}Uninstalling package...{colorama.Style.RESET_ALL}")
    removed = remove_package(package_name)
    if not removed:
        typer.echo(f"{colorama.Fore.RED}Error while removing package!{colorama.Style.RESET_ALL}")
        return
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
def install_remote_package(url, from_git=True, branch="deploy"):
    """
    Add a remote package to the packages directory.
    If the package is from git, it will be cloned. Otherwise, a remote package will be created.
    """

    if from_git:
        install_package_from_git(url, branch=branch)
    else:
        install_package_from_url(url)

def install_package_from_git(url, branch="deploy"):
    """Clone the git repo into /data/mbot/tmp/ and then run the install command"""

    # attempt to clone the repo
    success, _ = clone_package(url, branch)

    if not success:
        typer.echo(f"{colorama.Fore.RED}Failed to install git package!{colorama.Style.RESET_ALL}")
        return

    has_metadata = check_for_metadata(GIT_CLONE_PATH)
    has_index = check_for_file("index.html", GIT_CLONE_PATH)

    if not has_metadata:
        typer.echo(f"{colorama.Fore.RED}")
        typer.echo("The repo does not contain a metadata.json file!")
        typer.echo("This may indicate that the repo is not a valid package, or that you specified the wrong branch.")
        
        if has_index:
            typer.echo() # newline
            typer.echo("The repo does contain an index.html file, so it may be a useable package.")
        if not has_index:
            typer.echo()
            typer.echo("The repo does not contain an index.html file, so it's unlikely to be a useable package.")
        
        generate = typer.confirm(f"{colorama.Style.BRIGHT}Would you like to attempt to generate a metadata to install the package?")   

        if generate:
            typer.echo(f"{colorama.Style.RESET_ALL}")
            generate_metadata_at(GIT_CLONE_PATH)
        else:
            typer.echo(f"Exiting package installation{colorama.Style.RESET_ALL}")
            shutil.rmtree(GIT_CLONE_PATH)
            return

    # remove the .git folder
    shutil.rmtree(os.path.join(GIT_CLONE_PATH, ".git"))

    # install the package
    install_package(GIT_CLONE_PATH)

    # delete the tmp folder
    shutil.rmtree(GIT_CLONE_PATH)
    typer.echo(f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}Package installed from git!{colorama.Style.RESET_ALL}")

@app.command()
def add_remote_package():
    """Add a remote package to the packages directory"""
    
    remote_package_name = typer.prompt("Enter the name of the remote package")
    remote_url = typer.prompt("Enter the URL of the remote package")

    metadata = utils.generate_metadata(
        name=remote_package_name, 
        author="Unknown",
        description="",
        remote_url=remote_url,
        html_file="",
        remote_package=True,
        version="1.0.0",
        hidden=False,
        uuid=utils.generate_uuid(remote_url, "", "", "", ""))

    # remove tmp folder if it exists
    # if os.path.exists(DEFAULT_INSTALL_PATH + "/tmp/remote-package"):
    #     shutil.rmtree(DEFAULT_INSTALL_PATH + "/tmp/remote-package")

    # create a tmp folder
    os.makedirs(GIT_CLONE_PATH + "/tmp/remote-package", exist_ok=True)

    # save the metadata to the tmp folder
    with open(GIT_CLONE_PATH + "/tmp/remote-package/metadata.json", "w") as f:
        f.write(json.dumps(metadata, indent=4))
    
    # install the package
    success, _ = install_package(GIT_CLONE_PATH + "/tmp/remote-package", overwrite=True)

    if not success:
        typer.echo(f"{colorama.Fore.RED}Failed to install remote package!{colorama.Style.RESET_ALL}")
        return

    # remove tmp folder
    #shutil.rmtree(GIT_CLONE_PATH + "/tmp/remote-package")

    typer.echo(f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}Remote package installed!{colorama.Style.RESET_ALL}")


def install_package_from_url(url):
    pass

if __name__ == "__main__":
    app()
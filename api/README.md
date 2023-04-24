# The M-Bot Web Application API

## Overview

The M-Bot web application frontend uses the API to get the necessary data from the robot to display to the user. The API is written using Flask and is served using Waitress, which is a pure python WSGI server. This allows the API to operate purely as a python application, and requires no extra system dependencies aside from Python3 and Python3-pip. 

## Getting Started

Run the API (in production mode) by running the following in your terminal

```bash
python3 api.py
```

If you would like to launch a development instance of the api, run

```bash
./run.sh
```

This will launch the API in development mode, which includes hot reloads for file changes. 

This will start the API on port 5000 of localhost. If you installed the M-Bot web framework via the easy install script, you will need to stop the API which is running as a system service. To do so, run

```bash
sudo systemctl stop mbotapi.service
```

This will allow you to run the development API.

### Additional node

The API is hosted at `localhost:5000`. When the mbot-web application is installed via the install script, Nginx is used to serve all content to the user, allowing you to also access the api via `localhost/api/`. 

To test that the API is running, you may run

```bash
curl localhost:5000/ping
```
which should output `{"success": true}`

And if installed through the install script,

```bash
curl localhost/api/ping
```

should return the same.

## API endpoints

The API has a number of endpoints which perform different operations. The endpoints are listed below.

1. `/ping` - GET <br>
The `\ping` is used only to validate that the API is running.

2. `/packages/list` - GET<br>
This endpoint returns all currently installed packages, along with their metadata.

3. `/packages/uninstall` - POST<br>
This endpoint is used to request that a package is uninstalled. To use the endpoint, a json string containing the name of the package you wish to uninstall is required. Ex. `{"name": <package-name>}`

4. `/package/install` - POST<br>
This endpoint is used to install a git-package. To use, specify the package in the body. Ex. `{"url":<git url>}`

5. `/storage/keyvalue/<store>/` - GET, POST<br>
This endpoint is used for both getting and setting values in the keyvalue store. For example, a get request containing the body `{"key": <key>}` will return the value associated with the value stored in the keyvalue store <store>. The post endpoint is used to set the value of a specified key.

6. `/storage/keyvalue/<store>/all/` - GET<br>
Return all the key value pairs in the keyvalue store <store>.

7. `/storage/create/` - POST<br> 
Create a new key-value store. The body should specify the
name of the store. Ex. `{"store": <name>}`

## File Structure

`api.py` - The file containing endpoint definitions. If you want to add an endpoint, add it in this file.

`package_utils.py` - The file containing the functions that are used to manage system packages (e.g. settings package or drive control package). 

`storage_api.py` - The file containing functions for managing the persistent storage provided by the API. 
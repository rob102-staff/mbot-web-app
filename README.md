# MBot Web Application
<p align="center">
 <img src="https://user-images.githubusercontent.com/59806465/232891073-7a051d5c-3e9a-4af7-a9cc-f17ffdaa3d41.png">
</p>


## This page contains the current mbot web application

## Quick Install

To quickly install the mbot web application, copy the following onto your
linux command line. It will automatically install 

-> <b>Nginx</b> - For serving the web app<br>
-> <b>Python3</b> - for api and cli <br>
-> <b>python3-pip</b> - For api and cli setup <br>
-> <b>mbot-cli</b> - To manage the web application from the command line. Use with `mbot-cli`. Ex `mbot-cli --help` <br>
-> <b>mbot flask api</b> - To help serve the web application<br>
-> <b>Default mbot packages</b> - Home Page, Drive Control, Settings<br>

```sh
bash <(curl -s https://raw.githubusercontent.com/rob102-staff/mbot-web-app/main/setup/scripts/install.sh)
```

## Quick Uninstall

Uninstalls the web app and nginx from your machine

```sh
bash <(curl -s https://raw.githubusercontent.com/rob102-staff/mbot-web-app/main/setup/scripts/uninstall.sh)
```

## Creating a new mbot package

Creating packages for the mbot is rather simple. To start, run 

```bash
npx mbot-package-template-engine <package-name>
cd <package-name>
mbot-cli generate-metadata
```

This will create a new application template for you. The app is setup using React. To preview the app, 
run
```bash
npm run start
```

To build and install the application for the mbot web app, run
```bash
npm run build
cp metadata.json build
cd build
mbot-cli install
```

### Deploy a package to github

If you would like to share a package, simply build your package, and then push the
build folder to a branch named deploy, and thats it. 

## Using the Mbot CLI

Included with the web app is the mbot web CLI. The cli is accessible through the command `mbot-cli`.

The CLI is a management tool for mbot packages. It allows for easy installation of
mbot packages, along with simple removal, and metadata generation and updates.

To see available commands, run

```bash
mbot-cli --help
```


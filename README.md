# MBot Web Application

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
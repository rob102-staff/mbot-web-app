# System outline

## Introduction

This is the outline for the new MBOT web app. The mbot web app will connect to the robot and provides a modular system to serve different web pages.

## System overview

This system is build on top of "packages." A package is just a folder that contains the necessary files. A package will have a UUID that is used to reference the material in it. If you want to reach a webpage, then locate to the endpoint /packages/<UUID>/index.html. This will load the specified webpage.

## The API 

There is an API that can be used to get certain data for rendering the website. 

The available endpoints are

-> /packages/list - Return a json containing all the current packages

-> /package/UUID/metadata - Get the meta data for a package

## The package system

In `/data/www/mbot`, you can create packages. You create a package in the folder named `UUID`. This folder needs to have a `metadata.json` file. The folder will also need to contain an `index.html` which is the entry of the package.

### metadata.json

`metadata.json` has the following format:

```json
{
    "author":"package author",
    "name":"package name",
    "version":"package version"
}
```
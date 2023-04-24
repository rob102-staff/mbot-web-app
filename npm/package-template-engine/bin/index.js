#! /usr/bin/env node
const args = process.argv.slice(2);

if (args.length < 1) {
    console.log("Please provide a package name");
    process.exit(1);
}

const [packageName, ..._] = args;

// get the current execution path
const currentPath = process.cwd();

// clone the template
const clone = require('git-clone');
const path = require('path');

console.log("Creating template at " + path.join(currentPath, packageName));

clone("https://github.com/rob102-staff/mbot-package-template.git", path.join(currentPath, packageName), null, (error) => {
    console.log(error ? error : "Success!");

    if (!error) {
        // remove the .git folder
        const fs = require('fs');
        fs.rmSync(path.join(currentPath, packageName, ".git"), { recursive: true, force: true });
    }
});


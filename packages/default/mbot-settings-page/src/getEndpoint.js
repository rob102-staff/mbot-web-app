function getPageUrl() {
    // return the current page url.
    let url = window.location.href;
    
    let http_location = url.indexOf('http://');
    let https_location = url.indexOf('https://');

    if (http_location === -1 && https_location === -1) {
        return url.split('/')[0];
    }

    if (http_location !== -1) {
        return url.split('/')[2].split(":")[0];
    }

    if (https_location !== -1) {
        return url.split('/')[2].split(":")[0];
    }
}

function createEndpoint(endpoint, useHttps) {
    let url = "http://" + getPageUrl() + endpoint;
    if (useHttps) {
        url = "https://" + getPageUrl() + endpoint;
    }
    return url;
}

export {createEndpoint, getPageUrl};
/*
This file defines the API for the key-value store.
*/

const api_base = "http://localhost/api"

/**
 * Create a new key-value store that we can use to store data.
 * 
 * @param {string} store_name 
 * @returns {boolean} success
 */
async function create_key_value_store(store_name) {

    let success = false;

    fetch(api_base + "/storage/create/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "store": store_name
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                success = true;
            }
            else {
                success = false;
            }
        }).catch(error => {
            console.log(error);
        });

    return success;
}

/**
 * Get a key-value store.
 * 
 * @param {string} store_name
 * @param {string} key 
 * @returns {boolean} success
 * 
 */
async function get_key_value(store, key) {
    let data = null;
    let success = false;
    await fetch(api_base + "/storage/keyvalue/store/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "key": key
        })
    })
        .then(response => response.json())
        .then(json => {
            if (json.success) {
                data = json.value;
                success = true;
            }
        }).catch(error => {
            console.log(error);
        });
    return data;
}

/**
 * 
 * Set the value of a key in a key-value store.
 * 
 * @param {string} store 
 * @param {string} key 
 * @param {string} value 
 * @returns {boolean} success
 */
async function set_key_value(store, key, value) {
    let success = false;
    await fetch(api_base + "/storage/keyvalue/"+ store + "/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "key": key,
            "value": value
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                success = true;
            }
        }).catch(error => {
            console.log(error);
        });
    return success;
}

/**
 * Get all key-value pairs in a key-value store.
 * 
 * @param {string} store 
 */
async function get_all_key_values(store) {

    let all_values = null;

    await fetch(api_base + "/storage/keyvalue/"+store+"/all/",
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); 
            if (data.success) {
                all_values = data.keyvalues;
            }
        })
        .catch(error => {
            console.log(error);
        });

    return all_values;
}

/**
 * Delete a key-value store.
 * 
 * @param {string} store
 * @returns {boolean} success
 * 
 */
async function delete_key_value(store, key) {
    let success = false;
    await fetch(api_base + "/storage/keyvalue/store/", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "key": key
        })
    })
        .then(response => response.json())
        .then(json => {
            if (json.success) {
                success = true;
            }
        }).catch(error => {
            console.log(error);
        });
    return success;
}

export { create_key_value_store, get_key_value, set_key_value, delete_key_value, get_all_key_values };
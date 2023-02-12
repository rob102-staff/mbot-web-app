
// Gets the packages json from localhost:5000/packages
async function getPackages(callback) {
    return fetch("http://localhost:8080/api/packages/list")
        .then(response => response.json())
        .then(data => {
            console.log(data); 
            callback(data.packages);
        })
        .catch(error => {
            
            console.log(error);
        });
}

export default getPackages;

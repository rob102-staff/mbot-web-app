import {create_key_value_store, get_key_value, set_key_value, delete_key_value, get_all_key_values} from "./keyvalueapi";
import {useEffect, useState} from "react";

// a react component that displays a key-value store.
// it also provides a form to add new key-value pairs to the store.
function StoreInterface(props){

    // the name of the key-value store.
    const store = "test_store";

    const [store_values, set_store_values] = useState({}); // the key-value pairs in the store.
    
    useEffect(() => {
        // create the key-value store if it doesn't exist.
        create_key_value_store(store).then(_ => {
            // get all key-value pairs in the store.
            get_all_key_values(store).then((values) => {
                console.log(values); 
                set_store_values(values);
            });
        }
        );
        
    }, []);

    return (
        <div style={{display: "flex", alignContent: "center", alignItems: "center", flexDirection: "column"}}>
            <h1>Key-Value Store</h1>
            <h2>{store}</h2>

            <div style={{display: "flex", alignContent: "center", alignItems: "center", flexDirection: "column"}}>
                <h3>Key-Value Pairs</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Key</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Object.keys(store_values).map((key) => {
                            return (
                                <tr>
                                    <td>{key}</td>
                                    <td>{store_values[key]}</td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>

            <input type="text" placeholder="key" id="key" />
            <input type="text" placeholder="value" id="value" />
            <button onClick={() => {
                let key = document.getElementById("key").value;
                let value = document.getElementById("value").value;

                set_key_value(store, key, value).then(
                    get_all_key_values(store).then((values) => {
                        console.log(values); 
                        set_store_values(values);
                    })
                );
            }}>Add Key-Value Pair</button>
        </div>
    )
}

export default StoreInterface;
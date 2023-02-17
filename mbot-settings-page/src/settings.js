
import './settings.css';
import { useState, useEffect } from 'react';
import {NotificationContainer, NotificationManager} from 'react-notifications';
import 'react-notifications/lib/notifications.css';

// A settings react component

function uninstallPackage(name, onSuccess, onError) {
    fetch('http://localhost:8080/api/packages/uninstall', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name
        })
    }).then(res => res.json())
        .then(data => {
            
            if(data.success){
                console.log('Package uninstalled successfully');
                NotificationManager.success('Package uninstalled successfully', 'Success');
                onSuccess(); 
            } else {
                console.log('Package uninstallation failed');
                NotificationManager.error('Package uninstallation failed', 'Error');
                onError();
            }
            
        }).catch(err => {
            console.log(err);
            onError();
        });
}

function fetchPackages(setPackages) { 
    fetch('http://localhost:8080/api/packages/list')
    .then(res => res.json())
    .then(data => {
        console.log(data.packages);
        setPackages(data.packages);
    }).catch(err => {
        console.log(err);
    });
}

function Settings() {
    const [packages, setPackages] = useState([]);

    // use the effect hook to get data from the /api/packages/list endpoint
    useEffect(() => {
        fetchPackages(setPackages);
    }, []);

    return (
        <div className='settings'>
            <NotificationContainer />
            <h1>Settings</h1>

            <div className="packages-settings">
                <h2>Installed Packages</h2>
                <div className="packages-list">
                    {packages.map((pkg, index) => {
                        return (<div key={index} className="package-list-item">
                            <h3 className="pkg-title">{pkg.name}</h3>
                            <div className="pkg-meta-section">
                                <p className="pkg-meta-text"><strong>Description: </strong>{pkg.description}</p>
                                <p className="pkg-meta-text"><strong>Author: </strong>{pkg.author}</p>
                                <p className="pkg-meta-text"><strong>Version: </strong>{pkg.version}</p>
                                <p className="pkg-meta-text"><strong>UUID: </strong>{pkg.uuid}</p>
                            </div>
                            <div className="pkg-actions">
                                <button className="pkg-action-btn" onClick={() => uninstallPackage(pkg.name, () => {fetchPackages(setPackages)}, ()=>{})}>Uninstall</button>
                            </div>
                        </div>);
                    })}
                </div>
            </div>
        </div>
    );
}

export default Settings; 
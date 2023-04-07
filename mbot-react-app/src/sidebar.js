import React from 'react';
import { slide as Menu } from 'react-burger-menu';
import { useEffect, useState } from 'react';
import './sidebar.css';
import { createEndpoint } from './getEndpoint';

function getPackages(setPackages) {

    fetch(createEndpoint("/api/packages/list", false))
        .then(res => res.json())
        .then(data => {
            setPackages(data.packages);
        }).catch(err => {
            console.log(err);
        });
}

export default props => {

    const [packages, setPackages] = useState([]);

    // use the effect hook to get data from the /api/packages/list endpoint
    useEffect(() => {
        getPackages(setPackages);
    }, []);

    if (packages === undefined) {
        return <Menu></Menu>
    }

    return (
        <Menu onStateChange={() => { getPackages(setPackages); }}>
            <h2 className="menu-item" style={{ cursor: 'pointer' }}
                onMouseOver={e => e.target.style.color = 'brown'}
                onMouseOut={e => e.target.style.color = 'white'}
                onClick={() => {
                    props.setPackageURL(createEndpoint("/packages/default/index.html"));
                    document.getElementById("react-burger-menu-btn").click();
                }}
            >
                MBot home
            </h2>
            {packages.map((pkg, index) => {
                if (pkg.uuid === "default") {
                    return null;
                }
                return <h2 className="menu-item"
                    key={index}
                    onClick={() => {
                        console.log(pkg.name);
                        if (pkg.remote_package === true)
                            props.setPackageURL(pkg.remote_url);
                        else
                            props.setPackageURL(createEndpoint("") + pkg.URI);
                        console.log(createEndpoint("") + pkg.URI);
                        document.getElementById("react-burger-menu-btn").click();
                    }}
                    style={{ cursor: 'pointer' }}
                    onMouseOver={e => e.target.style.color = 'brown'}
                    onMouseOut={e => e.target.style.color = 'white'}>
                    {pkg.name}
                </h2>
            })}
        </Menu>
    );
};
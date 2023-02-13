import React from 'react';
import { slide as Menu } from 'react-burger-menu';
import { useEffect, useState } from 'react';
import './sidebar.css';

export default props => {

    const [packages, setPackages] = useState([]);

    // use the effect hook to get data from the /api/packages/list endpoint
    useEffect(() => {
        fetch('http://localhost:8080/api/packages/list')
            .then(res => res.json())
            .then(data => {
                console.log(data.packages);
                setPackages(data.packages);
            }).catch(err => {
                console.log(err);
            });
    }, []);

    if (packages === undefined) {
        return <Menu></Menu>
    }

    return (
        <Menu>
            <h2 className="menu-item" style={{cursor: 'pointer'}}
                onMouseOver={e => e.target.style.color = 'brown'}
                onMouseOut={e => e.target.style.color = 'white'}
                onClick={() => {
                    props.setPackageURL("http://localhost:8080/packages/default/index.html");
                    document.getElementById("react-burger-menu-btn").click();
                }}
                >
                MBot home
            </h2>
            {packages.map((pkg, index) => {
                return <h2 className="menu-item" 
                key={index}
                onClick={() => {
                    console.log(pkg.name);
                    props.setPackageURL("http://localhost:8080" + pkg.URI);
                    console.log("http://localhost:8080" + pkg.URI);
                    document.getElementById("react-burger-menu-btn").click();
                }}
                style={{cursor: 'pointer'}}
                onMouseOver={e => e.target.style.color = 'brown'}
                onMouseOut={e => e.target.style.color = 'white'}>
                    {pkg.name}
                </h2>
            })}
        </Menu>
    );
};
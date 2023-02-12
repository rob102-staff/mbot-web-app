import logo from './logo.svg';
import './App.css';
import { Sidebar, Menu, MenuItem, useProSidebar } from "react-pro-sidebar";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import PeopleOutlinedIcon from "@mui/icons-material/PeopleOutlined";
import ContactsOutlinedIcon from "@mui/icons-material/ContactsOutlined";
import ReceiptOutlinedIcon from "@mui/icons-material/ReceiptOutlined";
import CalendarTodayOutlinedIcon from "@mui/icons-material/CalendarTodayOutlined";
import HelpOutlineOutlinedIcon from "@mui/icons-material/HelpOutlineOutlined";
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";
import React, { useState, useEffect } from 'react';


import getPackages from './get_packages';


function App() {
  const { collapseSidebar } = useProSidebar();

  const [packages, setPackages] = useState([]);
  const [package_uri, setPackageURI] = useState([]);

  useEffect(() => {
    console.log("useEffect running");
    getPackages((data) => { console.log(data); setPackages(data); })}, []);


  return (
    <div id="app" style={({ height: "100vh" }, { display: "flex" })}>
      <Sidebar style={{ height: "100vh" }}>
        <Menu>
          <MenuItem
            icon={<MenuOutlinedIcon />}
            onClick={() => {
              collapseSidebar();
            }}
            style={{ textAlign: "center" }}
          >
            {" "}
            <h2>Admin</h2>
          </MenuItem>
          <MenuItem icon={<HomeOutlinedIcon />}>Home</MenuItem>
          
          {packages.map((p) => (
            <MenuItem icon={<PeopleOutlinedIcon key={p.name} onClick={() => { 
              setPackageURI("http://localhost:8080" + p.URI);
              console.log("http://localhost:8080" + p.URI + p.URI);
            }}/>}>{p.name}</MenuItem>
          ))}

        </Menu>
      </Sidebar>
      <iframe src={package_uri} style={{ width: "100%", height: "100%" }}></iframe>
    </div>
  );
}


export default App;

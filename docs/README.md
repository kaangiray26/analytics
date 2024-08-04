<div align="center">
    <a href="https://github.com/kaangiray26/analytics">
        <img src="https://kaangiray26.github.io/analytics/screenshot.png" alt="Analytics Logo">
    </a>
    <h1 align="center">analytics</h1>
    <p align="center">
        Simple, open-source web analytics alternative
        <br />
        <div align="center">
            <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/kaangiray26/analytics?style=flat-square">
            <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/kaangiray26/analytics?style=flat-square">
            <img alt="GitHub issues" src="https://img.shields.io/github/issues/kaangiray26/analytics?style=flat-square">
            <img alt="License" src="https://img.shields.io/github/license/kaangiray26/analytics.svg?style=flat-square">
        </div>
        <a href="https://github.com/kaangiray26/analytics/issues">Report Bug</a>
        ·
        <a href="https://github.com/kaangiray26/analytics/issues">Request Feature</a>
    </p>
</div>

## About
This project is a simple, open-source web analytics alternative. It uses a beacon to send data to the server. The server stores the data in a DuckDB database. The data is then visualized using a simple web interface.

You can view the script [here](https://kaangiray26.github.io/analytics/beacon.js).

## Setup
To add analytics to your website, add the following script to your website, and change the `data-addr` attribute to your server address.
```
<script defer data-addr="http://127.0.0.1:5000/beacon" src="https://kaangiray26.github.io/analytics/beacon.min.js"></script>
```

Or you can use the following script to add analytics to your website:
```
<script defer data-addr="http://127.0.0.1:5000/beacon">
(function(addr){window.addEventListener("DOMContentLoaded",()=>{fetch(addr,{method:"POST",headers:{"Content-Type":"application/json",},body:JSON.stringify({origin:window.location.origin,path:window.location.pathname,}),})})})(document.currentScript.getAttribute("data-addr"))
</script>
```

To run the server, we have created a Docker image. You can run the server using the `docker-compose.yml` file. The `docker-compose.yml` file comes with two environment variables:
- SITES: A comma-separated list of sites to track
- ADDRESS: The local ip address of the server

To run the server, run the following command:
```
docker compose up
```

## Usage
To view the analytics, go to `http://<local-ip>:5000/`. You can view the analytics for each site by clicking on the site name.

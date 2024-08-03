#!env/bin/python
#-*- coding: utf-8 -*-

import os
import time
import json
import hashlib
import duckdb
from datetime import datetime
from flask import Flask, request, send_from_directory, Response
from flask_cors import CORS

app = Flask(__name__)
app.config.from_prefixed_env()
CORS(app)

# Configuration
sites = os.environ.get("SITES", "null").split(", ")
address = os.environ.get("ADDRESS", None)
if not address:
    raise ValueError("ADDRESS environment variable not set")
    exit(1)

# DuckDB connection
con = duckdb.connect("sites.db")

# Check for the tables and
# create them if they don't exist
con.execute("CREATE TABLE IF NOT EXISTS sites (site STRING PRIMARY KEY, UNIQUE(site))")
con.execute("CREATE TABLE IF NOT EXISTS visitors (hash STRING, timestamp TIMESTAMP_S, user_agent STRING, origin STRING , path STRING, FOREIGN KEY(origin) REFERENCES sites(site))")

# Add sites to the database
# if they don't exist
res = con.sql("SELECT site FROM sites").fetchall()
if not res:
    # Prepare the statement
    statement = "INSERT INTO sites VALUES " + "(?), " * (len(sites)-1) + "(?)"
    res = con.execute(statement, sites)

async def log_request(req):
    # Hash the ip
    h = hashlib.sha256(req.remote_addr.encode()).hexdigest()

    # Construct visitor data
    data = [h, datetime.now(), req.user_agent.string, req.json["origin"], req.json["path"]]

    # Insert the data into the database
    try:
        con.execute("INSERT INTO visitors VALUES (?, ?, ?, ?, ?)", data)
    except Exception as e:
        print(e)

@app.before_request
def before_request():
    if request.path == "/beacon":
        return
    # Only allow requests from the local network
    if request.host != address:
        return Response("Forbidden", status=403)

@app.route("/", methods=["GET"])
async def index():
    return send_from_directory("static", "index.html")

@app.route("/site", methods=["POST"])
async def get_site():
    # Get site data
    data = {
        "unique":0,         # Unique visitors
        "total":0,          # Total number of visitors
        "traffic": [0 for x in range(12)], # Monthly traffic
        "paths": []         # Top 10 visited paths
    }

    # Get data from the database
    data["unique"] = con.execute("SELECT COUNT(DISTINCT hash) FROM visitors WHERE origin = ?", (request.json["site"],)).fetchone()[0]
    data["total"] = con.execute("SELECT COUNT(*) FROM visitors WHERE origin = ?", (request.json["site"],)).fetchone()[0]
    data["traffic"] = con.execute("SELECT strftime('%m', timestamp) as month, COUNT(*) as count FROM visitors WHERE origin = ? GROUP BY month", (request.json["site"],)).fetchall()
    data["paths"] = con.execute("SELECT path, COUNT(*) as count FROM visitors WHERE origin = ? GROUP BY path ORDER BY count DESC LIMIT 10", (request.json["site"],)).fetchall()

    return data

@app.route("/sites", methods=["GET"])
async def get_sites():
    res = con.sql("SELECT site FROM sites").fetchall()
    return {
        "sites": res
    }

@app.route("/beacon", methods=["POST"])
async def beacon():
    # Log the request
    await log_request(request)
    return {
        "message":"Beacon received"
    }

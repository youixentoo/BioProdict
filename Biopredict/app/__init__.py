# -*- coding: utf-8 -*-
"""
Created on Sun May 10 16:53:05 2020

@author: Thijs Weenink

Main script for the API.
There were plans for a web based interface, this is not implemented and it's currently too late to remove the plans for it. (11-jun-2020, 23:33)
"""
from flask import Flask, render_template, request
from .scripts.mongodb_connection import connector_backup, connector

app = Flask(__name__)

# Route for the 'home' page.
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


# Route for the API.
@app.route("/api",  methods=['GET', 'POST'])
def pureAPI():
    data = request.args

    # if statement to extract the correct API request, show an information page if false.
    if len(data) == 0 or list(data.keys()) != ['chr', 'loc', 'var']:
        return render_template("api.html")
    else:
        results = connector(data)
        return results
    
# Another page
@app.route("/results")
def results():
    return render_template("results.html")


# Function that apiapp.py calls
def launch():
    return app

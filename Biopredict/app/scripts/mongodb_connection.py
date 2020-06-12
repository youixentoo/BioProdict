# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 18:32:12 2020

@author: Thijs Weenink

Script to connect to and retrieve information from the MongoDB
"""
import requests
import pymongo
from bson.json_util import dumps
import json


# Connects and retrieves data based on the dictionary from the API
def connector(api_args):
    # MongoDB settings
    mongo_adress = "192.168.178.81"
    port = 27017
    mongodb_name = "bioprodict"
    collections_name = "vcf"
    
    # Setting up connection to DB
    client = pymongo.MongoClient(f'mongodb://{mongo_adress}/', port)
    db = client[f"{mongodb_name}"]
    data = db[f"{collections_name}"]

    # Arguments from API
    chrom = api_args.get("chr")
    try:
        location = int(api_args.get("loc"))
    except ValueError:
        return "loc is not an integer"
    variance = api_args.get("var")
    
    # Check if all needed information is there
    if not chrom or not variance:
        return "chr of var is empty"
    
    # Mongo shell query (example):
    # db.vcf.aggregate( { $unwind: "$7" }, {$match: { "7.Pos": 550404, "7.Ref": "AGGAGG"}})
    
    # MongoDB query. Matches on both the position as the reference.
    query = [{ "$unwind": f"${chrom}" }, {"$match": { f"{chrom}.Pos": location, f"{chrom}.Ref": f"{variance}"}}]
    
    # Test query for when there are issues.
    # query = [
    #     { "$unwind": "$7" }, 
    #     { "$match": { "7.Pos": 550404, "7.Ref": "A"}}
    #     ]
    # print(query)

    cursor = list(data.aggregate(query))

    if len(cursor) == 0:
        result = "No entries found"
    else:
        # To transfrom the returned data into a .json for nice visualisation in the browser and easy use ofcourse.
        result = json.loads(dumps(cursor[0]))

    return result


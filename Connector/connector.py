# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 14:57:59 2020

@author: Thijs Weenink

Simple script to read a .json file and calling the web based api.
"""
import requests
import json
import bson.json_util as bju

# Example of a main function to get information from the api
def main():
    api_adress = "192.168.178.81:5050"
    
    filename = "sample.json"

    sample_data = get_sample_data(filename)
    
    chroms = sample_data.keys()
    
    # No time for a pretty solution
    new_filename = filename.split(".")[0]+"_APIoutput"
    
    results = {}
    
    for chrom in chroms:
        result = retrieve_api_calls(sample_data, chrom, api_adress)
        results[chrom] = result
        
    # Stores it in a json file, key = chromosome, value = list of results from api.
    # list of results: 1st index: loc, 2nd index: var, 3rd index: api result.
    with open(f"{new_filename}.json", "w") as file_out:
        json.dump(results, file_out)
        
            
        
    
# Calls the api and returns the results   
def retrieve_api_calls(sample_data, chrom, api_adress):    

    data = sample_data[chrom]
    
    recieved_data = []
    
    for loc, var in data.items():
        
        api_call = "http://{}/api?chr={}&loc={}&var={}".format(api_adress, chrom, loc, var)
        api_return = requests.get(api_call).text
        json_conversion = bju.dumps(api_return)
        recieved_data.append((loc, var, json_conversion))
        
    return recieved_data
    

# Opens and loads the search data from the .json file as a dictionary
def get_sample_data(filename):
    with open(filename) as file:
        data = json.load(file)
    return data
    
    
if __name__ == "__main__":
    main()
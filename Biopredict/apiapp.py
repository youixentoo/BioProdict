# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 14:24:31 2020

@author: Thijs Weenink

Launches the web API. This is what docker-compose calls.
"""

from app import launch

app = launch()

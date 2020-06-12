# -*- coding: utf-8 -*-
"""
Created on Sun May 10 16:27:07 2020

@author: Thijs Weenink

er gaat een chromossom in, een locatie op het chromosoom en een variatie op die locatie.
"""
from vcf import Reader
import vcf.parser
import json
import vcf_parser

# Only calls a function a the vcf_parser script
def main():  
    # Output file - Input file
    vcf_parser.parse("Output/mongosetup_test.json", "D:/School/Jaar3/Biopredict/Data/gnomad.exomes.r2.1.1.sites.7.vcf")


if __name__ == "__main__":
    main()
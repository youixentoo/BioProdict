# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 11:42:12 2019

@author: Thijs Weenink

Reused mess from last year, removed most of the messy bits.
Reads the vcf file and extracts the needed data.
Also makes the file for MongoDB.

Doesn't do any filtering on cancer as I kinda forgot until writing this.
"""

from vcf import Reader
import vcf.parser
import json

# Main function to parse the vcf file and making the .json file for the MongoDB.
def parse(json_filename, vcf_file):
    amount = 0
    with open("errors.txt", "w"):
        pass
    
    vcf_reader = Reader(open(vcf_file))

    json_chr = {}
    
    for index, record in enumerate(vcf_reader):
        try:
            if record.INFO["AF"][0] > 0.01:# and record.INFO["non_cancer_AF_popmax"] == 0: #  or not "e" in str(x.INFO[keys[0]][0])

                amount += 1

                if json_chr.get(str(record.CHROM)):
                    json_chr[str(record.CHROM)].append(to_json(record, index))
                else:
                    json_chr[str(record.CHROM)] = [to_json(record, index)]
        
        # Just skip errors. 
        except KeyError:
            pass

        
        # Testing only
        # if amount > 6:
            # break
    
    total_data = index+1    
    
    # Write the file used for MongoDB
    with open(json_filename, "w") as outjson:
        json.dump(json_chr, outjson)
        
    # Extra information about how much data is stored.
    with open("Output/data_split_{}.txt".format(json_filename.split("/")[1]), "w") as dp:
        dp.write("Amount of data: {}\nTotal data in file: {}".format(amount, total_data))
            
    
# Gets all the information for the records and saves it in the needed format.
def to_json(record, count):
    chrom = record.CHROM
    pos = record.POS
    ref = record.REF
    alt = record.ALT[0]
    ac = record.INFO["AC"][0]
    an = record.INFO["AN"]
    freq = record.INFO["AF"][0]
    nc_ac = record.INFO["non_cancer_AC"][0]
    nc_an = record.INFO["non_cancer_AN"]
    nc_af = record.INFO["non_cancer_AF"][0]
    
    c_ac = ac - nc_ac
    c_an = an - nc_an
    
    
    json_dict = {
        "Chrom": chrom,
        "Pos": pos,
        "Ref": f"{ref}",
        "Alt": f"{alt}",
        "Frequency": freq,
        "Total_counts": {"AC":ac, "AN":an},
        "Non_cancer": {"nc_AC":nc_ac, "nc_AN":nc_an, "nc_AF":nc_af},  
        "Cancer": {"c_AC": c_ac, "c_AN": c_an},
        "Type": {"Var_type": record.var_type, "Var_subtype": record.var_subtype}
        }
    
    
    return json_dict


# vcf file format
def get_fileformat():
    file_format = """
    Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|
    cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|
    ALLELE_NUM|DISTANCE|STRAND|FLAGS|VARIANT_CLASS|MINIMISED|SYMBOL_SOURCE|HGNC_ID|CANONICAL|
    TSL|APPRIS|CCDS|ENSP|SWISSPROT|TREMBL|UNIPARC|GENE_PHENO|SIFT|PolyPhen|DOMAINS|HGVS_OFFSET|
    GMAF|AFR_MAF|AMR_MAF|EAS_MAF|EUR_MAF|SAS_MAF|AA_MAF|EA_MAF|ExAC_MAF|ExAC_Adj_MAF|ExAC_AFR_MAF|
    ExAC_AMR_MAF|ExAC_EAS_MAF|ExAC_FIN_MAF|ExAC_NFE_MAF|ExAC_OTH_MAF|ExAC_SAS_MAF|CLIN_SIG|SOMATIC|PHENO|
    PUBMED|MOTIF_NAME|MOTIF_POS|HIGH_INF_POS|MOTIF_SCORE_CHANGE|LoF|LoF_filter|LoF_flags|LoF_info"""
    return file_format

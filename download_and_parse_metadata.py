# -*- coding: utf-8 -*-
"""
Created on Fri Aug 05 16:23:30 2016

@author: Claire
"""
from lxml import etree
import pandas as pd
import os
import argparse


def download_metadata_xmls(df):
    ## Download all the metadata
    for i in df.index:
        xml = df.loc[i, 'secondary_sample_accession']
        sid = df.loc[i, 'sampleID']
        wgetstr = 'wget -O {}.xml http://www.ebi.ac.uk/ena/data/view/{}%26display%3Dxml'.format(sid,xml)
        os.system(wgetstr)
    return None

def parse_one_xml(xml_file, fields=None):
    """
    Returns age, bmi, and description metadata in dict form from one xml file
    """
    tree = etree.iterparse(xml_file)
    
    d = dict.fromkeys(fields)
    for event, elem in tree:
        if elem.tag == 'SAMPLE_ATTRIBUTE':
            for f in fields:
                if elem.getchildren()[0].text == f:
                    d[f] = elem.getchildren()[1].text 
    return d

def parse_metadata_xmls(fields):

    files = os.listdir(os.getcwd())
    files = [i for i in files if i.endswith('.xml')]
    
    allmeta = {}
    for f in files:
        sid = f.split('.')[0]
        allmeta[sid] = parse_one_xml(f, fields)

    return allmeta
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', help='EBI metadata file')
    parser.add_argument('-f', help='fields to parse from metadata xml files', nargs='+')
    parser.add_argument('-s', help='EBI column to use to label samples', default='fastq_ftp')
    parser.add_argument('-o', help='output metadata file', default='metadata.txt')
    parser.add_argument('-d', help='Download metadata xml files?', action='store_true')

    args = parser.parse_args()


    df = pd.read_csv(args.e, sep='\t')
    ## Add in a sampleID column
    df['sampleID'] = [s.split('/')[-1].split('.')[0] for s in df[args.s]]
    
    if args.d:
        download_metadata_xmls(df)
        
    ## Parse the metadata 
    meta = parse_metadata_xmls(args.f)
    
    meta = pd.DataFrame(meta).T
    meta.to_csv(args.o, sep='\t')

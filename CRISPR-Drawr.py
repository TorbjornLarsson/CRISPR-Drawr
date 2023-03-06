"""CRISPR-Drawr docstring."""
# -*- coding: UTF-8 -*-

# Summary: TBD

import sys
import logging
import requests
import click
#import numpy as np
from Bio import SeqIO

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0')

def greet():
    """CRISPR experimental design\n
    Author: Torbjörn Larsson"""

@greet.command()
@click.argument('file')  # add the name argument
def read_fna(**kwargs):
    filename = '{0}'.format(kwargs['file'])
    getFASTA_record = SeqIO.read(filename, "fasta")
    print(getFASTA_record.description)
    print("n=[1:20]: ", getFASTA_record.seq[1:20])

@greet.command()
@click.argument('file')  # add the name argument
def read_gbk(**kwargs):
    filename = '{0}'.format(kwargs['file'])
    getGenBank_record = SeqIO.read(filename, "genbank")
    print(getGenBank_record.description)
    print("n=[1:20]: ", getGenBank_record.seq[1:20])

@greet.command()
@click.option('--strand', default=1, help='strand orientation 1/-1', show_default=True)
@click.argument('chr')
@click.argument('start')
@click.argument('stop')
def get_sORF(**kwargs):
    chr = '{0}'.format(kwargs['chr'])
    start = '{0}'.format(kwargs['start'])
    stop = '{0}'.format(kwargs['stop'])
    strand = '{0}'.format(kwargs['strand'])

    server = "https://rest.ensembl.org"
     ext = "/sequence/region/human/"+chr+":"+start+".."+stop+":"+str(strand)+"?mask=hard"
    r = requests.get(server+ext, headers={ "Content-Type" : "text/x-fasta"})
 
    if not r.ok:
        r.raise_for_status()
        sys.exit()
 
    print(r.text)

if __name__ == '__main__':
    greet()

# We want to catch and log all exceptions to begin with
try:
    print()
    # Main code
 
except:  # catch *all* exceptions
    e = sys.exc_info()[0]
    print("Error: %s" % e)
    logging.exception("message")

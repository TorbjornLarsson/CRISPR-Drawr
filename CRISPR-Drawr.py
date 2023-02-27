"""CRISPR-Drawr docstring."""
# -*- coding: UTF-8 -*-

# Summary: TBD

import sys
import logging
import click
import numpy as np
from Bio import SeqIO

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0')

def greet():
    """CRISPR experimental design\n
    Author: Torbjörn Larsson"""
    pass

@greet.command()
@click.argument('name')  # add the name argument
def read_fna(**kwargs):
    filename = '{0}'.format(kwargs['name'])
    getFASTA_record = SeqIO.read(filename, "fasta")
    print(getFASTA_record.description)
    print("n=[1:20]: ", getFASTA_record.seq[1:20])

@greet.command()
@click.argument('name')  # add the name argument
def read_gbk(**kwargs):
    filename = '{0}'.format(kwargs['name'])
    getGenBank_record = SeqIO.read(filename, "genbank")
    print(getGenBank_record.description)
    print("n=[1:20]: ", getGenBank_record.seq[1:20])

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

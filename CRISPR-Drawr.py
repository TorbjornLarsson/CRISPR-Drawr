"""CRISPR-Drawr docstring."""
# -*- coding: UTF-8 -*-

# Summary: TBD
# 
 
import sys
import logging
import numpy as np

# We want to catch and log all exceptions to begin with
try:
    # Main code 
    print("-------------------------------------\n")
    print("CRISPR-Drawr v1 [Februrary, 2023]\n")
    print("SciLifeLab\n")
    print("Torbjörn Larsson\n")
    print("-------------------------------------\n")

except: # catch *all* exceptions
    e = sys.exc_info()[0]
    write_to_page( "<p>Error: %s</p>" % e )
    logging.exception("message")

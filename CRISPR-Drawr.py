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
    print("CRISPR-Drawr v1 [February, 2023]\n")
    print("SciLifeLab\n")
    print("Torbjörn Larsson\n")
    print("-------------------------------------\n")

except: # catch *all* exceptions
    e = sys.exc_info()[0]
    print("Error: %s" % e )
    logging.exception("message")

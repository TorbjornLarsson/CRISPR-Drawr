"""CRISPR-Drawr docstring."""
# -*- coding: UTF-8 -*-

# Summary: TBD

import sys
import logging
import click
import numpy as np

@click.group()
def greet():
    pass

@greet.command()
@click.argument('name')  # add the name argument
def hello(**kwargs):
    print('Hello, {0}!'.format(kwargs['name']))

@greet.command()
@click.argument('name')
def goodbye(**kwargs):
    print('Goodbye, {0}!'.format(kwargs['name']))

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

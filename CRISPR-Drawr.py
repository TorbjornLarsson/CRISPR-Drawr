"""CRISPR-Drawr docstring."""
# -*- coding: UTF-8 -*-

# Summary: TBD

import sys
import datetime
import logging
import requests
import click
#import numpy as np
from Bio import SeqIO
from pynat import get_ip_info
import paramiko
import scp

now = datetime.datetime.now()
tnow = now.strftime("%y%m%d_%H_%M_%S")

ip_info = get_ip_info()

logging.basicConfig(filename='example.log', level=logging.INFO)

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
    r = requests.get(server+ext, headers={ "Content-Type" : "text/plain"})
 
    if not r.ok:
        r.raise_for_status()
        sys.exit()
 
    print(r.text)
    filename = '_'.join([tnow,'chr',chr,start,stop,'strand',str(strand)])
    filename = filename+'.fa'
    print(filename)
    f = open(filename, 'x')
    f.write(r.text)
    f.close()


@greet.command()
@click.option('--strand', default=1, help='strand orientation 1/-1', show_default=True)
@click.option('--pad', default=2000, help='padding length [nt]', show_default=True)
@click.argument('chr')
@click.argument('start')
@click.argument('stop')
def get_arms(**kwargs):
    logging.info(tnow)
    logging.info('get_arms')
    logging.info(kwargs)
    chr = '{0}'.format(kwargs['chr'])
    start = '{0}'.format(kwargs['start'])
    stop = '{0}'.format(kwargs['stop'])
    strand = '{0}'.format(kwargs['strand'])
    pad = '{0}'.format(kwargs['pad'])
    server = "https://rest.ensembl.org"
    ext = "/sequence/region/human/"+chr+":"+start+".."+stop+":"+str(strand)\
        +"?expand_5prime="+str(pad)+";expand_3prime="+str(pad)+";mask=hard"
    
    r = requests.get(server+ext, headers={ "Content-Type" : "text/x-fasta"})
 
    if not r.ok:
        r.raise_for_status()
        sys.exit()
 
    print(r.text[1:100])
    filename = '_'.join([tnow,'chr',chr,start,stop,'strand',str(strand),'pad',str(pad)])
    filename = filename+'.fna'
    print(filename)
    f = open(filename, 'x')
    f.write(r.text)
    f.write('\n')
    f.close()

@greet.command()
@click.option('--outdirectory', default='', help='path', show_default=True)
@click.argument('infile')

def get_guides_primers(**kwargs):
    logging.info(tnow)
    logging.info('get_guides_primers')
    logging.info(kwargs)
    infile = '{0}'.format(kwargs['infile'])
    out_path = '{0}'.format(kwargs['outdirectory'])
    base_path = '/var/www/html/temp'

    # Connect
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip_info[1], port=2222, username='crispor', password='crispor')
    scp_client = scp.SCPClient(ssh_client.get_transport())

    # Execute the commands in series, each will finish before the next starts
    # 1. Move the infile to remote temp and close the scp client
    scp_client.put(infile, remote_path=base_path)
    scp_client.close()

    # 2. Run command
    # For tests we run sacCer3    
    _stdin, _stdout, _stderr = ssh_client.exec_command('python /var/www/html/crispor.py sacCer3 '+base_path+'/'+infile+' '+base_path+'/out.tsv')
    # cmd_text = 'python /var/www/html/crispor.py hg38 '\
    #     +base_path+'/'+infile+' '\
    #     +base_path+'/out.tsv '\
    #     +'-o '+base_path+'/offtargets.tsv '\
    #     +'--satMutDir='+base_path+'/SATMUTDIR'
    # _stdin, _stdout, _stderr = ssh_client.exec_command(cmd_text)

    # Print output of command. Will wait for command to finish.
    print(f'STDOUT: {_stdout.read().decode("utf8")}')
    print(f'STDERR: {_stderr.read().decode("utf8")}')

    # Get return code from command (0 is default for success)
    print(f'Return code: {_stdout.channel.recv_exit_status()}')

    # Because they are file objects, they need to be closed
    _stdin.close()
    _stdout.close()
    _stderr.close()

    #3. Fetch outfile with a new scp client
    scp_client = scp.SCPClient(ssh_client.get_transport())
    scp_client.get(base_path+'/out.tsv', local_path=out_path)
    scp_client.get(base_path+'/offtargets.tsv', local_path=out_path)
    scp_client.get(base_path+'/SATMUTDIR', recursive=True, local_path=out_path)

    # Close the clients
    scp_client.close()
    ssh_client.close()

    # chr = '{0}'.format(kwargs['chr'])
    # start = '{0}'.format(kwargs['start'])
    # stop = '{0}'.format(kwargs['stop'])
    # strand = '{0}'.format(kwargs['strand'])
    # pad = '{0}'.format(kwargs['pad'])
    # server = "https://rest.ensembl.org"
    # ext = "/sequence/region/human/"+chr+":"+start+".."+stop+":"+str(strand)\
    #     +"?expand_5prime="+str(pad)+";expand_3prime="+str(pad)+";mask=hard"
    
    # r = requests.get(server+ext, headers={ "Content-Type" : "text/x-fasta"})
 
    # if not r.ok:
    #     r.raise_for_status()
    #     sys.exit()
 
    # print(r.text[1:100])
    # filename = '_'.join([tnow,'chr',chr,start,stop,'strand',str(strand),'pad',str(pad)])
    # filename = filename+'.fna'
    # print(filename)
    # f = open(filename, 'x')
    # f.write(r.text)
    # f.write('\n')
    # f.close()
# ----------- MAIN --------------
if __name__ == '__main__':
    greet()

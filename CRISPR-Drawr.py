"""CRISPR-Drawr docstring."""
# -*- coding: UTF-8 -*-

# Summary: A tool to design mutagenic primer.

import sys
import datetime
import logging
import requests
import click
from Bio import SeqIO
from pynat import get_ip_info
import paramiko
import scp
import os
from shutil import copyfile
import pandas as pd
import numpy as np

now = datetime.datetime.now()
tnow = now.strftime("%y%m%d_%H_%M_%S")

ip_info = get_ip_info()[1]

logging.basicConfig(filename='crispr_drawr.log', level=logging.INFO)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0')

def greet():
    """CRISPR experimental design\n
    Author: Torbjörn Larsson"""

@greet.command()
@click.argument('file')  # add the name argument
def read_fna(**kwargs):
    logging.info(tnow)
    logging.info('read_fna')
    logging.info(kwargs)
    filename = '{0}'.format(kwargs['file'])
    getFASTA_record = SeqIO.read(filename, "fasta")
    print(getFASTA_record.description)
    print("n=[1:20]: ", getFASTA_record.seq[1:20])

@greet.command()
@click.argument('file')  # add the name argument
def read_gbk(**kwargs):
    logging.info(tnow)
    logging.info('read_gbk')
    logging.info(kwargs)
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
    logging.info(tnow)
    logging.info('get_sORF')
    logging.info(kwargs)
    chr = '{0}'.format(kwargs['chr'])
    start = '{0}'.format(kwargs['start'])
    stop = '{0}'.format(kwargs['stop'])
    strand = '{0}'.format(kwargs['strand'])

    server = "https://rest.ensembl.org"
    ext = "/sequence/region/human/"+chr+":"+start+".."+stop+":"+str(strand)+"?mask=hard"
    r = requests.get(server+ext, headers={ "Content-Type" : "text/plain"})
 
    if not r.ok:
        logging.info('request failed')
        r.raise_for_status()
        sys.exit()
 
    print(r.text)
    filename = '_'.join([tnow,'chr',chr,start,stop,'strand',str(strand)])
    filename = filename+'.fa'
    print(filename)
    logging.info(filename)
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
        logging.info('request failed')
        r.raise_for_status()
        sys.exit()
 
    print(r.text[1:100])
    filename = '_'.join([tnow,'chr',chr,start,stop,'strand',str(strand),'pad',str(pad)])
    filename = filename+'.fna'
    print(filename)
    logging.info(filename)
    f = open(filename, 'x')
    f.write(r.text)
    f.write('\n')
    f.close()

@greet.command()
@click.option('--o', '--output_path', default='', help='output directory path', show_default=True)
@click.argument('infile')

def get_guides_primers(**kwargs):
    logging.info(tnow)
    logging.info('get_guides_primers')
    logging.info(kwargs)
    fpath = '{0}'.format(kwargs['infile'])
    fname = os.path.basename(fpath)
    tempflag = 0
    if fname is not fpath:
        tempflag = 1
        copyfile(fpath,fname)

    out_path = '{0}'.format(kwargs['o'])
    base_path = '/var/www/html/temp'

    # Connect
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip_info, port=2222, username='crispor', password='crispor')
    scp_client = scp.SCPClient(ssh_client.get_transport())

    # Execute the commands in series, each will finish before the next starts
    # 1. Move the infile to remote temp and close the scp client
    scp_client.put(fname, remote_path=base_path)
    scp_client.close()
    if tempflag == 1:
        os.remove(fname)

    # 2. Run command
    # For tests we run sacCer3    
    # _stdin, _stdout, _stderr = ssh_client.exec_command('python /var/www/html/crispor.py sacCer3 '+base_path+'/'+fname+' '+base_path+'/'+tnow+'_out.tsv')
    cmd_text = 'python /var/www/html/crispor.py hg38 '\
        +base_path+'/'+fname+' '\
        +base_path+'/'+tnow+'_out.tsv '\
        +'-o '+base_path+'/'+tnow+'_offtargets.tsv '\
        +'--satMutDir='+base_path+'/'+tnow+'_SATMUTDIR'
    _stdin, _stdout, _stderr = ssh_client.exec_command(cmd_text)

    # Print output of command. Will wait for command to finish.
    logging.info(_stdout.read().decode("utf8"))
    logging.info(_stderr.read().decode("utf8"))
 
    # Get return code from command (0 is default for success)
    print(f'Return code: {_stdout.channel.recv_exit_status()}')

    # Because they are file objects, they need to be closed
    _stdin.close()
    _stdout.close()
    _stderr.close()

    #3. Fetch outfile with a new scp client
    scp_client = scp.SCPClient(ssh_client.get_transport())
    scp_client.get(base_path+'/'+tnow+'_out.tsv', local_path=out_path)
    scp_client.get(base_path+'/'+tnow+'_offtargets.tsv', local_path=out_path)
    scp_client.get(base_path+'/'+tnow+'_SATMUTDIR', recursive=True, local_path=out_path)

    # Close the clients
    scp_client.close()
    ssh_client.close()

    # Parse and add snr score to outfile
    ontargets_df=pd.read_csv(out_path+'/'+tnow+'_out.tsv', sep="\t")
    labels=ontargets_df.columns.tolist()
    labels.append('')
    ontargets_df=pd.read_table(out_path+'/'+tnow+'_out.tsv', header=None,names=labels,skiprows=1)
    guides = np.unique(ontargets_df['guideId'])
    
    # First get signal as specificity scores
    signalscore=[]
    for guide in guides:
         signalscore.append(np.float64(ontargets_df.loc[offtargets_df['guideId'] == guide]['mitSpecScore']))
    
    # Then get sum of squares of off target specificity noise scores 
    offtargets_df=pd.read_table(out_path+'/'+tnow+'_offtargets.tsv')
    noisescore=[]
    for guide in guides:
        noisescore.append(np.square(offtargets_df.loc[offtargets_df['guideId'] == guide]['cfdOfftargetScore']).sum())
    
    # Now get snr score with specificity scores as amplitudes
    snrscore=[]
    i = 0
    for score in signalscore[0]:
        snrscore.append(score**2/noisescore[i])
        i += 1
    
    # Add column and replace guidefile
    ontargets_df['snrScore'] = snrscore
    ontargets_df.to_csv(out_path+'/'+tnow+'_out.tsv', sep = '\t', index=False)

    # Make design matrix over guides and primers
    # First sort the two dataframes on guides and make the design matrix.
    # Then sort priority according to snr score.
    header_list = ['#seqId', 'guideId', 'targetSeq', 'snrScore']
    design_df = ontargets_df[header_list].copy()
    primers_df = pd.read_table(out_path+'/'+tnow+'_SATMUTDIR/'+tnow+'_ontargetPrimers.tsv')
 
    design_df.sort_values(by='guideId', inplace=True)
    primers_df.sort_values(by='#guideId', inplace=True)

    header_list = header_list + ['forwardPrimer', 'leftPrimerTm', 'revPrimer', 'revPrimerTm']
    design_df = design_df.reindex(columns = header_list) 
    design_df['forwardPrimer'] = primers_df['forwardPrimer']
    design_df['leftPrimerTm'] = primers_df['leftPrimerTm']
    design_df['revPrimer'] = primers_df['revPrimer']
    design_df['revPrimerTm'] = primers_df['revPrimerTm']
    
    design_df.sort_values(by='snr', ascending=False, inplace=True)
    design_df.to_csv(out_path+'/'+tnow+'_designtable.tsv', sep = '\t', index=False)

# ----------- MAIN --------------
if __name__ == '__main__':
    greet()

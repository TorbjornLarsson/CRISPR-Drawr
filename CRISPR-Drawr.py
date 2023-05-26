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

#ip_info = get_ip_info()[1]
# For non-eduroam usres we need to pull the ipv4 adress
# In windows it is easy, do ipconfig /all in a terninal.
ip_info = '192.168.1.69'

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

    host_out_path = '{0}'.format(kwargs['o'])
    guest_base_path = '/var/www/html/temp'

    def run_file():
        # Connect, clear the cashes and create the SATMUTDIR out directory
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ip_info, port=2222, username='crispor', password='crispor')
        scp_client = scp.SCPClient(ssh_client.get_transport())
        _stdin, _stdout, _stderr = ssh_client.exec_command('sudo -S <<< "crispor" sh -c $"echo 1 > /proc/sys/vm/drop_caches"')
        guest_in_path = guest_base_path+'/'+fname
        guest_out_path = guest_base_path+'/'+tnow+'_'+fname+'_out.tsv'
        guest_offtargets_path = guest_base_path+'/'+tnow+'_'+fname+'_offtargets.tsv'
        satmut_dir = guest_base_path+'/'+tnow+'_'+fname+'_SATMUTDIR'
        _stdin, _stdout, _stderr = ssh_client.exec_command('mkdir '+satmut_dir)

        # Execute the commands in series, each will finish before the next starts
        # 1. Create the SATMUTDIR and close the scp client
        
        scp_client.put(fname, remote_path=guest_base_path)
        scp_client.close()
        if tempflag == 1:
            os.remove(fname)

        # 2. Run command
        # For tests we run sacCer3    
        # _stdin, _stdout, _stderr = ssh_client.exec_command('python /var/www/html/crispor.py sacCer3 ' +base_path+'/'+fname+' '+out_file)
        cmd_text = 'python /var/www/html/crispor.py hg38 '\
            +guest_in_path+' '\
            +guest_out_path+' '\
            +'-o '+guest_offtargets_path+' '\
            +'--satMutDir='+satmut_dir
        logging.info(cmd_text)
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

        #3. Fetch outfiles with a new scp client
        scp_client = scp.SCPClient(ssh_client.get_transport())
        scp_client.get(guest_out_path, local_path=host_out_path)
        scp_client.get(guest_offtargets_path, local_path=host_out_path)
        scp_client.get(satmut_dir, recursive=True, local_path=host_out_path+'/'+os.path.basename(satmut_dir))
        scp_client.close()
        logging.info('In target data: '+host_out_path+os.path.basename(guest_out_path))
        logging.info('Off target data: '+host_out_path+os.path.basename(guest_offtargets_path))
        logging.info('Saturation data: '+host_out_path+os.path.basename(satmut_dir))
        
        # and erase all files after
        _stdin, _stdout, _stderr = ssh_client.exec_command('rm '+guest_in_path)
        _stdin, _stdout, _stderr = ssh_client.exec_command('rm '+guest_out_path)
        _stdin, _stdout, _stderr = ssh_client.exec_command('rm '+guest_offtargets_path)
        _stdin, _stdout, _stderr = ssh_client.exec_command('rm -rf '+satmut_dir)

        # Close the client
        ssh_client.close()

        # Parse and add snr score to outfile
        out_name = os.path.basename(guest_out_path)
        ontargets_df=pd.read_csv(host_out_path+'/'+out_name, sep="\t")
        labels=ontargets_df.columns.tolist()
        labels.append('')
        ontargets_df=pd.read_table(host_out_path+'/'+out_name, header=None, names=labels, skiprows=1)
        guides = np.unique(ontargets_df['guideId'])

        # Get sum of squares of off target specificity noise scores
        offtargets_name = os.path.basename(guest_offtargets_path)
        offtargets_df=pd.read_table(host_out_path+'/'+offtargets_name)
        noisescore=[]
        for guide in guides:
            noisescore.append(np.square(offtargets_df.loc[offtargets_df['guideId'] == guide]['cfdOfftargetScore']).sum())

        # Get signal as in target specificity scores
        signalscore=[]
        for guide in guides:
                signalscore.append(np.float64(ontargets_df.loc[offtargets_df['guideId'] == guide]['mitSpecScore']))

        # Now get snr score with specificity scores as amplitudes
        snrscore=[]
        i = 0
        for score in signalscore[0]:
            snrscore.append(score**2/noisescore[i])
            i += 1

        # Add column and replace guidefile
        ontargets_df['snrScore'] = snrscore
        ontargets_df.to_csv(host_out_path+'/'+out_name, sep = '\t', index=False)
        logging.info('Added snrScore to: '+host_out_path+os.path.basename(guest_out_path))
       
        # Make design matrix over guides and primers
        # First sort the two dataframes on guides and make the design matrix.
        # Then sort priority according to snr score.
        header_list = ['#seqId', 'guideId', 'targetSeq', 'snrScore']
        design_df = ontargets_df[header_list].copy()
        primers_df = pd.read_table(host_out_path+os.path.basename(satmut_dir)+'/'+tnow+'_'+fname+'_ontargetPrimers.tsv')

        design_df.sort_values(by='guideId', inplace=True)
        primers_df.sort_values(by='#guideId', inplace=True)

        header_list = header_list + ['forwardPrimer', 'leftPrimerTm', 'revPrimer', 'revPrimerTm']
        design_df = design_df.reindex(columns = header_list) 
        design_df['forwardPrimer'] = primers_df['forwardPrimer']
        design_df['leftPrimerTm'] = primers_df['leftPrimerTm']
        design_df['revPrimer'] = primers_df['revPrimer']
        design_df['revPrimerTm'] = primers_df['revPrimerTm']

        design_df.sort_values(by='snrScore', ascending=False, inplace=True)
        design_table_path = host_out_path+'/'+tnow+'_'+fname+'_designtable.tsv'
        design_df.to_csv(design_table_path, sep = '\t', index=False)
        logging.info('Added designtable: '+design_table_path)

    if str.split(fname, sep='.')[1] == 'bed':
        fr = open(fname, 'r')
        Lines = fr.readlines()
        fr.close()
        for line in Lines:
            fname = line.split(sep='\t')[3]+'.bed'
            fline = open(fname, 'w')
            fline.writelines(line)
            fline.close()
            run_file()
            os.remove(fname)
    else:
        run_file()
    
    logging.info('Done!')

# ----------- MAIN --------------
if __name__ == '__main__':
    greet()

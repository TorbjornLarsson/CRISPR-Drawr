# CRISPR-Drawr - a CRISPR design tool

## User instructions
CRISPR-Drawr suggests guides and primers, and conveniently output design tables with ranks using specificity scores for on- and offtarget effects.

CRISPR-Drawr uses the CRISPOR package for Virtualbox, see http://crispor.tefor.net/downloads/. To download and run hg38 analyses at least 8 GB RAM is recommended.
You run CRISPR-Drawr from the command line.

## Software licenses
Note that CRISPOR usage is free only for academic or non-profit organisations.
  
## Setup instructions
Make sure you have Python>=3.8 installed. 

Then install dependencies with:
`pip install -r requirements.txt`

Next clone and add the base directory of the repository to your PYTHONPATH.

Finally run python.py with something like:
`python3 CRISPR-Drawr.py`
  
Follow the CRISPOR download and installation instructions. Open the machine settings, go to the System tabs and set the base memory to no less than 6200 MB and the number of CPUs to 2. G to the Network tab, then to Advanced/Port Forwarding and put a space in the ssh Host IP to free that setting. Finally open port 2222 in your firewall.

When you start your virtual machine in Virtualbox, CRISPR-Drawr will manage to work against that machine if you are using eduroam wifi. If you have other LAN settings you may have to find out your IPv4 address by opening a terminal and do ifconfig (on linux) or ipconfig /all (on windows).

There is a crispor.py bug in the current download version that needs to be fixed. SSH to port 2222 on your IPv4 address:  
`ssh crispor@{IPv4 address} -p 2222, password \"crispor\"`  
Then navigate to the crispor.py directory:  
`cd /var/www/html`  
The installation has a nano editor that can be used for the bug fix.  
`sudo nano crispor.py, password "crispor"`  
Navigate to line number 6903 by a corntrol-key sequence:  
`CTRL + -, line number "6903"`  
Add two lines after 6903, minding the same start position as that line as in Python conventiok:  
`score = "0"`  
`strand = "+"`  
Save the file with a control-key sequences:  
`CTRL + X, Save modified buffer? "Yes"`  

CRISPR-Drawr default is the human hg38 genome. You can perform the ~ 1 h download by navigating to the download tool and ask for the hg38 genome to be put in the /var/www/html/genomes/ directory:  
`cd /var/www/html/tools`  
`crisprDownloadGenome hg38`  

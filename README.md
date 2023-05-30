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
  
Follow the CRISPOR download and installation instructions. Open the machine settings, go to the System tabs and set the base memeory to no less than 6200 MB and the number of CPUs to 2. If you run CRISPR-Drawr on a WSL2 virtual machine linux installation on windows you then go to the Network tab, then to Advanced/Port Forwarding and put a space in the ssh Host IP to free that setting. Finally open port 2222 in your firewall.

When you start your virtual machine in Virtualbox, CRISPR-Drawr will manage to work against that machine if you are using eduroam wifi. If you have other LAN settings you may have to find out your ipv4 adress by opening a terminal and do ipconfig /all (on windows) or ifconfig (on linux).

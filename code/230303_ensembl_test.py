import requests, sys
 
server = "https://rest.ensembl.org"
ext = "/lookup/id/ENSG00000165029?"
 
r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
 
if not r.ok:
  r.raise_for_status()
  sys.exit()
 
decoded = r.json()
print(repr(decoded))

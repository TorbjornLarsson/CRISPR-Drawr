import requests, sys
 
server = "https://rest.ensembl.org"
#ext = "/sequence/region/human/X:1000000..1000100:1?expand_3prime=60;expand_5prime=60"
#ext = "/sequence/region/human/X:1000000..1000100:-1?expand_3prime=60;expand_5prime=60" 
#ext = "/sequence/region/human/X:1000000..1000100:1?mask=hard"
ext = "/sequence/region/human/16:67846953..67846986:1?mask=hard"

r = requests.get(server+ext, headers={ "Content-Type" : "text/x-fasta"})
 
if not r.ok:
  r.raise_for_status()
  sys.exit()
 
 
print(r.text)

# Test script for bed file handling

import pandas as pd

# If infile is a bed file, iterate on each row: 
fname = 'test.bed'
#print(str.split(fname, sep='.')[1])
i=1

def test_function():
  fw.write(line)
  print('0')
    
if str.split(fname, sep='.')[1] == 'bed':
  fr = open(fname, 'r')
  Lines = fr.readlines()
  fr.close()
  
  for line in Lines:
    fw = open('in.bed', 'w')
    #fw.write(line)
    print(i)
    i=i+1
    test_function()
    fw.close


        

# Test script for result handling

import pandas as pd
import numpy as np

# Read out correctly
tsv_df=pd.read_csv('test.tsv', sep="\t")
#print(tsv_df)
#print(tsv_df.columns.tolist())
labels=tsv_df.columns.tolist()
#print(labels)
labels.append('')
#print(labels)
tsv_df=pd.read_table('test.tsv', header=None,names=labels,skiprows=1)
#print(tsv_df)
ontargets_df = tsv_df
guides = np.unique(tsv_df['guideId'])
#print(guides)

offtargets_df=pd.read_table('analyses/offtargets.tsv')
#print(offtargets_df)
#print(offtargets_df.loc[offtargets_df['guideId'] == guides[0]])
#print(offtargets_df.loc[offtargets_df['guideId'] == guides[0]]['cfdOfftargetScore'])
#print(type(offtargets_df.loc[offtargets_df['guideId'] == guides[0]]['cfdOfftargetScore']))
#print(np.square(offtargets_df.loc[offtargets_df['guideId'] == guides[0]]['cfdOfftargetScore']).sum())
noisescore=[]
for guide in guides:
    noisescore.append(np.square(offtargets_df.loc[offtargets_df['guideId'] == guide]['cfdOfftargetScore']).sum())
print(noisescore)

onscore=[]
for guide in guides:
    #print(ontargets_df.loc[offtargets_df['guideId'] == guide]['mitSpecScore'])
    onscore.append(np.float64(ontargets_df.loc[offtargets_df['guideId'] == guide]['mitSpecScore']))
print(onscore[0])

snrscore=[]
i = 0
for score in onscore[0]:
    snrscore.append(score**2/noisescore[i])
    i += 1
print(snrscore)

ontargets_df['snr'] = snrscore
print(ontargets_df)
for col in ontargets_df:
   print(ontargets_df[col])

ontargets_df.to_csv('testout.tsv', sep = '\t', index=False)

# Make design matrix over guides and primers
# colkeys=ontargets_df.columns.tolist()
# print(colkeys)

header_list = ['#seqId', 'guideId', 'targetSeq', 'snr']
#design_df = ontargets_df[['#seqId', 'guideId', 'targetSeq', 'snr']].copy()
design_df = ontargets_df[header_list].copy()
#print(design_df)
primers_df = pd.read_table('ontargetPrimers.tsv')
print(primers_df)

#First sort the two dataframes on guides and make the design matrix.
#Then sort priority according to snr score.
design_df.sort_values(by='guideId', inplace=True)
#print(design_df)
primers_df.sort_values(by='#guideId', inplace=True)
#print(primers_df)

#primers_df.index = design_df.index
#design_df[['forwardPrimer', 'leftPrimerTm', 'revPrimer', 'revPrimerTm']] = design_df[['forwardPrimer', 'leftPrimerTm', 'revPrimer', 'revPrimerTm']]
#print(design_df)

#print(header_list)
header_list = header_list + ['forwardPrimer', 'leftPrimerTm', 'revPrimer', 'revPrimerTm']
#print(header_list)
design_df = design_df.reindex(columns = header_list) 
#print(design_df)
design_df['forwardPrimer'] = primers_df['forwardPrimer']
#print(design_df)
design_df['leftPrimerTm'] = primers_df['leftPrimerTm']
design_df['revPrimer'] = primers_df['revPrimer']
design_df['revPrimerTm'] = primers_df['revPrimerTm']
#print(design_df)
design_df.sort_values(by='snr', ascending=False, inplace=True)
#print(design_df)
for col in design_df:
   print(design_df[col])
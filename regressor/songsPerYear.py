import matplotlib
matplotlib.use('Agg')
import sys
import os
import matplotlib.pyplot as plt 
from functions import importMappedData, mbzMeta
import numpy as np

def printUsage():
	print("Usage: python songsPerYear.py {user_id}")
	
	
try:
	user = sys.argv[1]
except IndexError as err:
	printUsage()
	sys.exit(1)
	
user_folder = './'+user

# Set up data
allData = importMappedData(user_folder+'/mapped_data.tsv')
data = mbzMeta(user_folder+'/meta.tsv',allData)
data = data.merge(allData, on='track_id')

# Select the attribute we want to visualise
attribute = data['year'].value_counts()

labels = attribute.index.values
# Deal with unknown (empty string)
labels = ["Unknown" if x == '' else x for x in labels]

frequency = attribute.tolist() 
 
# Generate the y positions. Later, replace them with labels
y_pos = range(len(labels))

fig,ax = plt.subplots()

y_pos = np.arange(len(labels))
ax.barh(y_pos, frequency,align='center',color='purple')
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis()
# Set percentage labels
totals = []
for i in ax.patches:
	totals.append(i.get_width())
total = sum(totals)
for i in ax.patches:
	ax.text(i.get_width()+.3, i.get_y()+.38, \
		str(round((float(i.get_width())/float(total))*100,2))+'%',fontsize=8)
ax.set_xlabel('Number of songs')
ax.set_ylabel('Year')
ax.set_title("Songs Per Year")

ax.set_xlim(0, total)
plt.gcf().subplots_adjust(left=0.20)
plt.savefig(user+'/songsPerYear.png')
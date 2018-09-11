#!/usr/bin/env python3
# coding: utf-8

import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt
#import pandas as pd
import os
import csv
import sys

# common setup  BEGIN
cur_dir = os.path.dirname(os.path.realpath(__file__))
plt.figure(figsize=[3.6, 2.8])
sns.set_style("whitegrid")
sns.set_palette(sns.color_palette('colorblind'))
label_size = 9
matplotlib.rcParams['xtick.labelsize'] = label_size 
matplotlib.rcParams['ytick.labelsize'] = label_size 
matplotlib.rcParams.update({'font.size': label_size})
#plt.gcf().subplots_adjust(bottom=0.15)
#plt.gcf().subplots_adjust(left=0.4)
# common setup END

COLUMN = 1

print(" ".join(sys.argv))
for f in sys.argv[1:]:
    values = []
    csv_reader = csv.reader(open(f, "r"), delimiter=";")
    #_ = csv_reader.next() # ignore first value 
    i=0
    for row in csv_reader:
        i+=1
        if i <= 8:
            continue
        try:
            values.append(float(row[COLUMN]) / 1000) # ms
            #print(float(row[COLUMN]))
        except IndexError:
            pass

  
plt.figure(figsize=[10.0, 6.7])
#ax = sns.violinplot(data=all_data[(all_data["polling"] == "default")], y="device", x="latency (ms)", bw=0.2, linewidth=0.5, scale="count")
ax = sns.distplot(values, bins=30);
axes = plt.gca()
axes.set_xlim([0,60])
#plt.gcf().subplots_adjust(bottom=0.15)
#plt.gcf().subplots_adjust(left=0.25)
#sns.axlabel("latency (ms)", "")
if len(sys.argv[1:]) == 1: # only one file
    png_filename = os.path.splitext(os.path.basename(sys.argv[1]))[0] + ".png"
    plt.savefig(cur_dir + "/histograms_1ms/" + png_filename)
else:
    plt.show()

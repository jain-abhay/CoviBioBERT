import os
from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
import math
from nltk import tokenize
import re
from bs4 import BeautifulSoup
import sys

# data = pd.read_csv("all_sources_metadata_2020-03-13.csv",encoding="utf-8")
filename = "metadata.csv"
data = pd.read_csv(filename,encoding="utf-8")

def isNaN(string):
    return string!=string

index = data.index
rows = len(index)
print("total rows: ", rows)
count = 0
req = int(0.05*rows)

fileindex = 1
filerowcount = 0
maxabstcount = 100000

f = open('./shards/input'+str(fileindex)+'.txt', 'w', encoding="utf-8")

for abst in data['abstract']:
    count+=1
    filerowcount+=1
    if not isNaN(abst):
        soup = BeautifulSoup(abst,features="html.parser")
        clean_data = soup.get_text()
        try:
            p = tokenize.sent_tokenize(clean_data)
            for line in p:
                line += '\n'
                # print(line)
                f.write(line)
            f.write("\n")
        except:
            print("Oops!", sys.exc_info()[0], "occurred at count: ", count)
    if count == req:
        fileindex+=1
        count=0
        f.close()
        f = open('./shards/input'+str(fileindex)+'.txt', 'w', encoding="utf-8")

      




    
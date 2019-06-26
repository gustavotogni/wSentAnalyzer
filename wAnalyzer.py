import os
import sys
import pandas
import matplotlib.pyplot as plt
import pandas as pd
from wCrawler import wCrawler
from wProcessor import wProcessor
import wPlotter

import seaborn as sns

if (len(sys.argv) <= 1):
    print("ERROR: You must provide the path to the .csv file to be processed (or created) as the 1st parameter.")
    sys.exit(1)

# Number of API calls to make agaisn't wedy
# Don't go over 250 or you'll be termined by the server
# Each call retrieves 10 comments
numberOfRequests = 10
if (len(sys.argv) > 2):
    numberOfRequests = sys.argv[2]

outputFolderExists = os.path.isdir('./output')
if (not outputFolderExists):
    os.mkdir('./output')

sourceFileName = sys.argv[1]
sourceFileExists = os.path.isfile(sourceFileName)

if not sourceFileExists:
    print(sourceFileName + " doesn't exist. A WebCrawler will create one with live data.")
    wCrawler = wCrawler()    
    wCrawler.crawlToFile(numberOfRequests, sourceFileName)    

messagesToClassify = pandas.read_csv(
    sourceFileName,
    sep = ',',
    names = ["id", "content"],
    skiprows = 1
)

textProcessor = wProcessor('output/')
messagesToClassify['tokens'] = messagesToClassify['content'].apply(textProcessor.prepMsgList)
classifiedMessages = textProcessor.classifyMsgList(messagesToClassify)
pandas.DataFrame(classifiedMessages).to_csv('./output/classifiedSource.csv')
print('Classification results output to "output/classifiedSource.csv"')
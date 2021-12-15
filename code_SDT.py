# some parts of the code were taken from demos
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

from statistics import mean, StatisticsError
from os import listdir
from statsmodels.stats.anova import AnovaRM

#import data
dataPath = "data/"
fileList = listdir(dataPath)

sdtData = pd.DataFrame()
counter = 0

for dataFile in fileList:

    counter += 1
    pNum = "P-" + str(counter)
    rawData = pd.read_csv(dataPath + dataFile)
    expData = pd.DataFrame(rawData, columns = ["condition", "trial", "key_resp.keys", "key_resp.rt"])
    expData = expData.rename(columns = {"key_resp.keys" : "resp", "key_resp.rt" : "RT"})
    #print(expData)
    accuracy = pd.DataFrame({"condition" : ["short", "long"], "hits" : [0, 0], "misses" : [0,0], "CRs" : [0, 0], "FAs" : [0, 0]})
    for index, row in expData.iterrows():
        #short
        if row["condition"] == "short":
            rowInd = 0
            if row["trial"] == "go" and row["resp"] == "space":
                accuracy.loc[rowInd, "hits"] += 1
            elif row["trial"] == "go" and row["resp"] == "None":
                accuracy.loc[rowInd,"misses"] += 1
            elif row["trial"] == "no-go" and row["resp"] == "None":
                accuracy.loc[rowInd,"CRs"] += 1
            elif row["trial"] == "no-go" and row["resp"] =="space":
                accuracy.loc[rowInd,"FAs"] += 1
        elif row["condition"] == "long":
            rowInd = 1
            if row["trial"] == "go" and row["resp"] == "space":
                accuracy.loc[rowInd,"hits"] += 1
            elif row["trial"] == "go" and row["resp"] == "None":
                    accuracy.loc[rowInd,"misses"] += 1
            elif row["trial"] == "no-go" and row["resp"] == "None":
                    accuracy.loc[rowInd,"CRs"] += 1
            elif row["trial"] == "no-go" and row["resp"] == "space":
                    accuracy.loc[rowInd,"FAs"] += 1
    sdtData = pd.concat([sdtData, accuracy], ignore_index=True)
#print(sdtData)
shortCond = sdtData.query('condition == "short"')
longCond = sdtData.query('condition == "long"')
hitShortMean = shortCond['hits'].mean()
hitLongMean = longCond['hits'].mean()
FAshortMean = shortCond['FAs'].mean()
FAlongMean = longCond['FAs'].mean()
missShortMean = shortCond['misses'].mean()
missLongMean = longCond['misses'].mean()
crShortMean = shortCond['CRs'].mean()
crLongMean = longCond['CRs'].mean()
print(crLongMean)

 #d' function
def dPrime(hitRate, FArate):
     stat = norm.ppf(hitRate) - norm.ppf(FArate)
     return stat

#criterion function
def criterion(hitRate, FArate):
    stat = -.5 * (norm.ppf(hitRate) + norm.ppf(FArate ))
    return stat

hitRateShort = hitShortMean / 25
hitRateLong = hitLongMean / 25
FArateShort = FAshortMean / 25
FArateLong = FAlongMean / 25

print("d' (short):", dPrime(hitRateShort, FArateShort))
print("criterion (short):", criterion(hitRateShort, FArateShort))

print("d' (long):", dPrime(hitRateLong, FArateLong))
print("criterion (long):", criterion(hitRateLong, FArateLong))

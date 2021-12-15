# some parts of the code were taken from demos
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from statistics import mean, StatisticsError
from os import listdir
from statsmodels.stats.anova import AnovaRM


dataPath = "data/"
fileList = listdir(dataPath)
meanRTs = pd.DataFrame({"participant" : [], "condition" : [],  "mean RT" : []})
#print(meanRTs)

counter = 0
for dataFile in fileList:

    counter += 1
    pNum = "P-" + str(counter)
    rawData = pd.read_csv(dataPath + dataFile)

    expData = pd.DataFrame(rawData, columns = ["condition", "trial", "key_resp.keys", "key_resp.rt"])
    expData = expData.rename(columns = {"key_resp.keys" : "key", "key_resp.rt" : "RT"})
    #print(expData)

    expData = expData[expData.RT.notnull()] # filter answers with RT
    rtData = expData[(expData.trial == "go") & (expData.key == "space")]
    #print(rtData)

    # short and long RTs for each participant
    shortGoRTs = rtData[(rtData.condition == "short") & (rtData.trial == "go")].RT
    longGoRTs = rtData[(rtData.condition == "long") & (rtData.trial == "go")].RT
    print(shortGoRTs)

    if len(shortGoRTs) == 0:
        pNumList = [pNum]
        conditionList = ["long"]
        meanRTsList = [mean(longGoRTs)]
    elif len(longGoRTs) == 0:
        pNumList = [pNum]
        conditionList = ["short"]
        meanRTsList = [mean(shortGoRTs)]
    else:
        pNumList = [pNum, pNum]
        conditionList = ["short", "long"]
        meanRTsList = [mean(shortGoRTs), mean(longGoRTs)]
    newLines = pd.DataFrame({"participant" : pNumList, "condition" : conditionList,  "mean RT" : meanRTsList})
    meanRTs = meanRTs.append(newLines, ignore_index=True)

meanRTs = meanRTs.drop(meanRTs.index[[2]])
#print(meanRTs)

#Separate the long mean RTs from the short mean RTs
listOfshortMean = (meanRTs['mean RT'][meanRTs['condition']=='short'])
listOflongMean = (meanRTs['mean RT'][meanRTs['condition']=='long'])

meanShort = np.mean(meanRTs['mean RT'][meanRTs['condition']=='short'])
meanLong = np.mean(meanRTs['mean RT'][meanRTs['condition']=='long'])

#calculate SD
stdShort = np.std(meanRTs['mean RT'][meanRTs['condition']=='short'])/np.sqrt(6)
stdLong = np.std(meanRTs['mean RT'][meanRTs['condition']=='long'])/np.sqrt(6)

#wilcoxon t-test
t_test = stats.wilcoxon(listOfshortMean, listOflongMean)

print(f"{round(meanShort, 2)} +- {round(stdShort, 2)}")
print(f"{round(meanLong, 2)} +- {round(stdLong, 2)}")
print(t_test)

plt.errorbar(0, meanShort, 3*stdShort, fmt='.', c='r', capsize=2)
plt.errorbar(0, meanLong, 3*stdLong, fmt='.', c='k', capsize=2)
plt.show()

fig, ax = plt.subplots()
box = ax.boxplot([listOfshortMean, listOflongMean])
ax.set_ylabel("Mean RT (s)")
ax.set_title('Mean RT for the two conditions')
ax.set_xticklabels(['short condition', 'long condition'])
plt.show()


hist = plt.hist([listOfshortMean, listOflongMean])
plt.xlabel(['short condition', 'long condition'])
plt.ylabel("Mean RT (s)")
plt.show()

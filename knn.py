#KNN model

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import random as rdm

# number of neighbors
K = 5
# amount to change K by per iteration
KRate = 1
# training sample size
numTrainSamples = 2000


# calculate distance between 2 points
def distance(x1, x2):
    dist = 0.0
    for i in range(len(x1)-1):
        dist += (x1[i] - x2[i])**2
    dist = math.sqrt(dist)
    return dist


# finds mode of passed ndarray
# for KNN, this should be passed an ndarray of Y values
    # in order of ascending distance from target
def findMode(a):
    # get unique values and their counts
    (uniques, counts) = np.unique(a, return_counts=True)
    # check for only one mode, return it
    if len(np.argwhere(counts==np.max(counts))) < 2:
        return uniques.item(np.where(counts==np.max(counts))[0][0])
    # if tied, try again with farthest data point removed
    else:
        return findMode(a[:-1])

# takes a data point, a set of other data points, Y values
    # of the other data, and a K for
    # Nearest Neighbor calculation.
def getNNY(target, others, othersY, kn):
    # save Y values, and calculate distance from target
    sorted = np.zeros((len(others),2))
    for i in range(len(others)):
        sorted[i][0] = othersY[i]
        sorted[i][1] = distance(target,others[i])
    # sort data by distance from target
    sorted = sorted[sorted[:,1].argsort()]
    # collect Y values of exactly K nearest neighbors
    neighborsY = np.zeros(kn)
    for j in range(1,kn):
        neighborsY[j] = sorted[i][0]
    return findMode(neighborsY)


# Train
def TrainIteration(localK):
    YTrainPred = np.zeros(len(YTrain))
    for i in range(len(XTrain)):
        print("calculating XTrain[" + str(i) + "]")
        YTrainPred[i] = getNNY(XTrain[i],XTrain,YTrain,localK)
    correct = 0
    avgdif = 0.0
    for i in range(len(YTrainPred)):
        if YTrainPred[i] == YTrain[i]:
            correct += 1
        avgdif += abs(YTrain[i] - YTrainPred[i])
    avgdif /= len(YTrain)
    print("correct values: " + str(correct) + " out of " + str(len(YTrain)))
    print("average error: " + str(avgdif))
    print("K = " + str(localK))
    input("Press Enter to continue...")
    return correct,avgdif

def Train(localK):
    cor, avg = TrainIteration(localK)
    localK += KRate
    cor2, avg2 = TrainIteration(localK)
    while cor2 < cor and avg2 < avg:
        cor = cor2
        avg = avg2
        cor2, avg2 = Train(localK)

        if cor2 > cor or avg2 > avg:
            print("Done training!")
            return localK
        else:
            localK += KRate
    localK -= KRate * 2
    cor = cor2
    avg = avg2
    cor2, avg2 = TrainIteration(localK)
    while cor2 < cor and avg2 < avg:
        cor = cor2
        avg = avg2
        cor2, avg2 = TrainIteration(localK)
        if cor2 > cor or avg2 > avg:
            print("Done training!")
            return localK
        else:
            localK -= KRate
    localK += KRate
    print("Done training!")
    return localK


######## End of definitions


# read data from csv
data = pd.read_csv('.\\winequality-white.csv', sep = ';')
arr = pd.DataFrame(data).to_numpy()
# normalize
minVal = np.zeros(12)
maxDif = np.zeros(12)
    # get minimum and range for each factor & result
for i in range(0,12):
    minVal[i] = arr[:,i].min()
    maxDif[i] = arr[:,i].max() - minVal[i]
        # perform normalization on each factor in each datum
    for x in range(0,len(arr)):
        arr[x,i] = (arr[x,i] - minVal[i]) / maxDif[i]


# separate X and Y values for easier use
X = np.zeros((len(arr),11))
Y = np.zeros(len(arr))
X = arr[:,0:10]
Y = arr[:,11]


# pick random sample for training
trainPicks = rdm.sample(range(len(arr)),numTrainSamples)

# initialize arrays for training and test sets
XTrain = np.zeros((numTrainSamples,10))
YTrain = np.zeros(numTrainSamples)
XTest = np.zeros((len(arr) - numTrainSamples,10))
YTest = np.zeros(len(arr) - numTrainSamples)

# separate training and test samples
curTrainIndex = 0
curTestIndex = 0
for i in range(0,len(arr)):
    if i in trainPicks:
        j = 0
        for val in X[i]:
            XTrain[curTrainIndex][j] = val
            j += 1
        YTrain[curTrainIndex] = Y[i]
        curTrainIndex = curTrainIndex + 1
    else:
        for val in X[i]:
            np.append(XTest[curTestIndex],val)
        YTest[curTestIndex] = Y[i]
        curTestIndex = curTestIndex + 1

'''
# display training data
cols = data.columns.tolist()
fig, ax = plt.subplots(5,2)
for i in range(len(XTrain[0])):
    ax[i%5,math.floor(i/5)].scatter(XTrain[:,i],YTrain)
    ax[i%5,math.floor(i/5)].set_title(cols[i])
plt.ylabel('wine quality')
plt.show()
'''

K = Train(K)
print("final K: " + str(K))
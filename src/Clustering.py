import numpy as np
from collections import Counter

import stem

# https://www.youtube.com/watch?v=EvlzEkjVpO8

url = input("Enter your Youtube Link : ")

stem.preprocessing(url)

file = open("stem.txt", "r")
result = file.read()
file.close()

result = result.split('\n')

time = []
stemText = []
# 자막 파일에서 단어 수 세기.
for i in range(0, len(result), 2):
    time.append(result[i].split(" --> "))
    temp = result[i+1].split(' ')
    stemText.append(temp)

#print(time)
#print(stemText)
partition = [0, len(stemText)]

def getSortedVocab(stemTxt, start, end):
    voCab = {}
    for i in range(start, end):
        for w in stemTxt[i]:
            if w in voCab:
                voCab[w] += 1
            else:
                voCab[w] = 1

    #print("단어의 개수", len(voCab))
    #print("1 개 이상의 단어의 개수", sum(x > 1 for x in voCab.values()))
    #print(voCab)

    sortedvoCab = sorted(voCab.items(), key=(lambda x: x[1]), reverse=True) # value 순 정렬.

    #print(sortedvoCab)

    return sortedvoCab

#sortedVocab = getSortedVocab(stemText, 0, len(stemText))

def printsortedVocab(sortedVocab):
    #for printing the contents in sortedvocab
    preValue = sortedVocab[0][1]
    print(preValue, end=" ")
    for (key, value) in sortedVocab:
        if value != preValue:
            preValue = value
            print("\n", value, key, end=" ")
        else:
            print(key, end=" ")
    print("\n", end=" ")
    return

#printsortedVocab(sortedVocab)

def getfirst(word, linelist, start, end):
    for i in range (start, end):
        if word in linelist[i]:
            return i
    return -1

def getlast(word, linelist, start, end):
    for i in range (end - 1, start - 1, -1):
        if word in linelist[i]:
            return i
    return -1

def getwordVec(sortedVocabi, StTxt, start, end, lendur):
    WV = {}
    i = 0
    for (key, value) in sortedVocabi:
        # if len(wordVector) >= 5:
        #    break
        if value > 1:
            if (getlast(key, StTxt, start, end) - getfirst(key, StTxt, start, end)) > ((end - start) / lendur):
                continue
        if value < 2:  # 2 번 이상 쓰인 것만
            break
        WV[key] = i
        i = i + 1
    #print(WV)
    return WV

#wordVector = getwordVec(sortedVocab, stemText, 0, len(stemText), 100)

#print("dimension of vector", len(wordVector))
#print(wordVector)

def getFeature(stemTxt, wordVect, start, end):
    #print("end = ", end)
    ft = np.zeros((end - start, len(wordVect)))
    for i in range (end - start):
        count = Counter(stemTxt[start + i])
        for key in count:
            if key in wordVect:
                ft[i][wordVect[key]] = count[key]
    return ft

#feature = getFeature(stemText, wordVector, 0, len(stemText))

def getSumFeature(feat):
    SF = np.copy(feat)
    for i in range(len(SF)):
        if i == 0:
            continue
        SF[i] += SF[i - 1]
    return SF

#sumFeature = getSumFeature(feature)


def euc_similar(a, b):
    return np.sqrt(np.sum((a-b)**2))

def manhattan_similar(a, b):
    return np.sum(np.abs(a - b))

def cosine_similar(a, b):  # 1 - same,  0 - perpendicular , -1 - reverse
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 0.000001)



def divide_cent(SF, minsize): # feature의 s부터 e까지에서 반갈죽 잘하는 center를 구하자
    minhalf = minsize >> 1
    maxindex = minhalf

    max = 0
    for i in range(minhalf, len(SF) - minhalf + 1):
        feat_a = SF[i - 1]
        if np.sum(feat_a) == 0:
            continue
        feat_a = feat_a/np.sum(feat_a)
        feat_b = SF[-1] - SF[i - 1]
        if np.sum(feat_b) == 0:
            continue
        feat_b = feat_b/np.sum(feat_b)

        #similar = euc_similar(feat_a, feat_b)
        similar = manhattan_similar(feat_a, feat_b)

        if similar > max:
            max = similar
            maxindex = i
            #print("index i : " + str(i))
            #print(feat_a)
            #print(feat_b)

    return maxindex

def Recursion(StemTxt, start, end, minsize, iter):
    global k
    #print(start, " " , end)
    if end - start < minsize:
        return

    sortedVocab = getSortedVocab(StemTxt, start, end)

    #printsortedVocab(sortedVocab)

    wordVector = getwordVec(sortedVocab, StemTxt, start, end, k) # last num is the length
    print(wordVector)

    feature = getFeature(StemTxt, wordVector, start, end)

    sumFeature = getSumFeature(feature)

    centroid = divide_cent(sumFeature, minsize)
    #print (centroid)
    #do it for front
    Recursion(StemTxt, start, start + centroid, minsize, iter+1)

    #print the result
    #print(" " * iter, start + centroid, " ", time[start + centroid])
    partition.append(start + centroid)

    #do it for back
    Recursion(StemTxt, start + centroid, end, minsize, iter+1)

    return
# ===== Edit this =====
n = 7 # size of cluster
k = 6 # length of word Vec
# =====================

minsize = int(len(stemText) / n)

print("minsize = ", minsize)

Recursion(stemText, 0, len(stemText), minsize ,0)

partition.sort()
print(partition)

for i in range (len(partition) - 1):
    print(time[partition[i]][0][:8],", [ " ,end = "")
    sortvocab = getSortedVocab(stemText, partition[i], partition[i+1])
    for j in range (4):
        print(sortvocab[j][0].upper(), end=", ")
    print(sortvocab[4][0].upper(), end=" ")
    print("]")

#centroid = divide_cent(sumFeature)

#print("center", centroid, time[centroid])

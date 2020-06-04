import numpy as np
from collections import Counter

import stem_kor
import stem
import os

# https://www.youtube.com/watch?v=EvlzEkjVpO8

# url = input("Enter your Youtube Link : ")

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
    #print(start, " " , end)
    if end - start < minsize:
        return

    sortedVocab = getSortedVocab(StemTxt, start, end)

    #printsortedVocab(sortedVocab)

    wordVector = getwordVec(sortedVocab, StemTxt, start, end, k) # last num is the length

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

def main(url, lang, num_of_cluster):
    global k, partition
    print(url)
    err = 0
    try:
        video_name = url.split('v=')[1]
    except:
        err = 1    
    if err == 1:
        return err, "Not available youtube URL", "None"
    
    file_name = "stem_{}_{}.txt".format(video_name, lang)

    file_exist = False
    # stem.txt 파일 있는지 체크하는 거 추가해야함.
    if os.path.isfile(file_name):
        file_exist = True
        file = open("{} ({}).srt".format(video_name, lang), "r", encoding='UTF8')
        origin_subtitle = file.read()
        file.close()

    if not file_exist:
        if lang == "en":
            err, origin_subtitle = stem.preprocessing(url)
        else:
            err, origin_subtitle = stem_kor.preprocessing(url) # korean stemming. 변경해야함.
    
    if err == 2:
        return err, "Not supported URL", "None"
    elif err == 3:
        return err, "No lang subtitle", "None"
        

    file = open(file_name, "r", encoding='UTF8')
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

    # ===== Edit this =====
    n = num_of_cluster # desired number of cluster
    k = int(n * 6 / 7) # length of word Vec
    # =====================

    minsize = int(len(stemText) / n)

    result = list()

    # print("minsize = ", minsize)
    result.append("minsize = ")
    result.append(minsize)
    result.append("\n")

    #Recursion(stemText, 0, len(stemText), minsize ,0)
    queue = []
    queue.append([0,len(stemText)])
    count = 1
    while (count < n and len(queue) > 0):

        curmax = 0
        curindex = 0
        for i in range (len(queue)):
            if (queue[i][1] - queue[i][0]) > curmax:
                curindex = i
                curmax = queue[i][1] - queue[i][0]

        curstart = queue[curindex][0]
        curend = queue[curindex][1]

        if curend - curstart < minsize:
            del queue[curindex]
            continue

        sortedVocab = getSortedVocab(stemText, curstart, curend)

        # printsortedVocab(sortedVocab)

        wordVector = getwordVec(sortedVocab, stemText, curstart, curend, k)  # last num is the length

        feature = getFeature(stemText, wordVector, curstart, curend)

        sumFeature = getSumFeature(feature)

        centroid = divide_cent(sumFeature, minsize)
        # print (centroid)
        # do it for front
        #Recursion(StemTxt, start, start + centroid, minsize, iter + 1)
        queue.append([curstart, curstart + centroid])
        # print the result
        # print(" " * iter, start + centroid, " ", time[start + centroid])
        partition.append(curstart + centroid)
        count += 1

        # do it for back
        #Recursion(StemTxt, start + centroid, end, minsize, iter + 1)
        queue.append([curstart + centroid, curend])
        del queue[curindex]


    partition.sort()
    # print(partition)
    result.append(partition)
    result.append("\n")

    for i in range (len(partition) - 1):
        timestamp = list()
        # print(time[partition[i]][0][:8],", [ " ,end = "")
        result.append(time[partition[i]][0][:8])
        result.append(", [ ")
        sortvocab = getSortedVocab(stemText, partition[i], partition[i+1])
        for j in range (4):
            # print(sortvocab[j][0].upper(), end=", ")
            timestamp.append(sortvocab[j][0].upper())
        # print(sortvocab[4][0].upper(), end=" ")
        timestamp.append(sortvocab[4][0].upper())
        # print("]")
        timestamp = ", ".join(timestamp)
        result.append(timestamp)
        result.append(" ]\n")

    #centroid = divide_cent(sumFeature)

    #print("center", centroid, time[centroid])
    # print(result)

    result = "".join(str(value) for value in result)
    # print(result)
    return err, result, origin_subtitle

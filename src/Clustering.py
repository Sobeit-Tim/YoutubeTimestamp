import numpy as np
from collections import Counter
import queue

file = open("stem.txt", "r")
result = file.read()
file.close()

result = result.split('\n')

time = []
stemText = []
vocab = {}
# 자막 파일에서 단어 수 세기.
for i in range(0, len(result), 2):
    time.append(result[i].split(" --> "))
    temp = result[i+1].split(' ')
    stemText.append(temp)
    for j in temp:
        if j in vocab:
            vocab[j] += 1
        else:
            vocab[j] = 1

print(time)
print(stemText)

print("단어의 개수", len(vocab))
print("1 개 이상의 단어의 개수", sum(x > 1 for x in vocab.values()))
sortedVocab = sorted(vocab.items(), key=(lambda x: x[1]), reverse=True) # value 순 정렬.
preValue = sortedVocab[0][1]
print(" ", preValue, end=" ")
for (key, value) in sortedVocab:
    if value != preValue:
        preValue = value
        print("\n", value, key, end=" ")
    else:
        print(key, end=" ")

wordVector = {}
i = 0
for (key, value) in sortedVocab:
    #if len(wordVector) >= 5:
    #    break
    if value < 2: # 2 번 이상 쓰인 것만
        break
    wordVector[key] = i
    i = i + 1

print("dimension of vector", len(wordVector))
print(wordVector)

feature = np.zeros((len(stemText), len(wordVector)))

i = 0
for line in stemText:
    count = Counter(line)
    for key in count:
        if key in wordVector:
            feature[i, wordVector[key]] = count[key]
    i = i + 1

sumFeature = np.copy(feature)
for i in range(len(sumFeature)):
    if i == 0:
        continue
    sumFeature[i] += sumFeature[i-1]


norm = np.sum(feature, axis=1) # L1 norm
print(norm)


def euc_similar(a, b):
    return np.sqrt(np.sum((a-b)**2))


def man_similar(a, b):
    return np.sum(np.abs(a-b))


def cosine_similar(a, b):  # 1 - same,  0 - perpendicular , -1 - reverse
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 0.000001)


def divide_cent(_feat, _s, _e, _sum): # feature의 s부터 e까지에서 반갈죽 잘하는 center를 구하자
    if _e - _s < 3 or np.sum(_sum[_e-1] - _sum[_s]) == 0: # 구간이 일정 크기 이하 or 구간합이 0인 지점이면 그만
        return -1
    _index = -1
    if _s == 0:
        _featBase = np.zeros(np.shape(_feat[_s]))
    else:
        _featBase = _sum[_s - 1]
    _min = 987654321
    for i in range(_s, _e-1):
        feat_a = _sum[i] - _featBase
        if np.sum(feat_a) == 0: # 왼쪽 부분이 아직 0이면은 그냥 계속 skip
            continue
        feat_a = feat_a/np.sum(feat_a)

        feat_b = _sum[_e - 1] - _sum[i]
        if np.sum(feat_b) == 0: # 오른 쪽 부분이 0이면은 break
            break
        feat_b = feat_b/np.sum(feat_b)

        similar = man_similar(feat_a, feat_b)
        if similar < _min:
            _min = similar
            _index = i

    return _index


# clustering. get centers.
centers = []
s = 0
e = len(feature)

cluster_queue = queue.Queue()
cluster_queue.put((s, e))

while cluster_queue.qsize() > 0:
    s, e = cluster_queue.get()
    if e - s < 30:
        continue
    centroid = divide_cent(feature, s, e, sumFeature)
    if centroid == -1 or centroid == s or centroid == e:
        continue
    centers.append(centroid+1)

    cluster_queue.put((s, centroid+1))
    cluster_queue.put((centroid+1, e))

print(centers)
centers = sorted(centers)
for i in centers:
    print("maximize similar", i, time[i], stemText[i])



"""
0:23 : 10, The first manned, powered, heavier-than-air flight
1:05 : 9, The Attack on Pearl Harbour
1:45 : 8, Raising the flag on low Jima
2:26 : 7, The Hindenburg Disaster
3:09 : 6, V-J Day in Times Square
3:54 : 5, Migrant Mother
4:34 : 4, Hiroshima
5:23 : 3, Tank Man
6:06 : 2, The Fall of the Berlin Wall
7:07 : 1, Man on the Moon
"""



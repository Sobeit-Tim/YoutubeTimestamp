from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

file = open("subtitle.srt", "r")
result = file.read()
file.close()

result = result.split('\n\n')

time = []
text = []

for i in result:
    temp = i.split('\n')
    tempText = ""
    for j in range(len(temp)):
        if j == 1:
            time.append(temp[j])
        elif j > 1:
            tempText += temp[j]

    text.append(tempText)

documents = text
print(text)

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

true_k = 2
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print

print("\n")
print("Prediction")

for i in text:
    Y = vectorizer.transform([i])
    prediction = model.predict(Y)
    print(prediction)

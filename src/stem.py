from nltk.tokenize import word_tokenize, TreebankWordTokenizer, WordPunctTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


"""from pytube import YouTube
URL = input("Enter youtube url: ")
yt = YouTube(URL)
caption = yt.captions.all()[0]

caption.download("Captions") #기본 저장 형태가 srt인듯
"""

def preprocessing():
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

    #print(time)
    #print(text)

    tokenText = []
    lemmaText = []
    stemText = []

    # eliminateWord = ["were", "in", "a", "[", "]", "in"]
    eliminateWord = set(stopwords.words('english'))
    eliminateWord2 = ["'s", ".", ",", "'re", "?", "!", "'ll"]
    vocab = {}

    for i in text:
        temp = word_tokenize(i)
        # TreebankWordTokenizer().tokenize(i)
        # WordPunctTokenizer().tokenize(i)
        temp = list(filter(lambda x: x not in eliminateWord and x not in eliminateWord2, temp))
        #lemma = [WordNetLemmatizer().lemmatize(w).lower() for w in temp]
        stem = [PorterStemmer().stem(w).lower() for w in temp]
        if not temp:
            continue
        #tokenText.append(temp)
        #lemmaText.append(lemma)
        stemText.append(stem)

    #print(tokenText)
    #print(lemmaText)
    #print(stemText)

    file = open("stem.txt", "w")
    for i in range(len(time)):
        file.write(time[i] + "\n")
        for j in range(len(stemText[i])):
            file.write(stemText[i][j])
            if j != len(stemText[i]) - 1:
                file.write(" ")
        if i != len(time) - 1:
            file.write("\n")
    file.close()

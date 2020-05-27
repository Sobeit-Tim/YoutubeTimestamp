from nltk.tokenize import word_tokenize, TreebankWordTokenizer, WordPunctTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from pytube import YouTube

"""
import requests
L = "en"
LANG = "Korean"
#ID = "7068mw-6lmI"
ID = 'b3ZjhNG_BrM'
URL = "http://video.google.com/timedtext?lang={}&v={}".format(L, ID)
#URL = 'https://www.youtube.com/api/timedtext?lang={}&v={}&name={}'.format(L, ID, LANG)
#URL = "https://www.googleapis.com/youtube/v3/captions/{}".format(ID)
response = requests.get(URL)
print(response.status_code)
print(response.text)"""


def preprocessing(url):
    video_name = url.split('v=')[1]
    yt = YouTube(url)
    caption = yt.captions.get_by_language_code('en')

    caption.download(video_name) #기본 저장 형태가 srt인듯

    #file = open("subtitle.srt", "r")
    file = open("{} (en).srt".format(video_name), "r", encoding='UTF8')
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
    eliminateWord2 = set(["'s", ".", ",", "'re", "?", "!", "'ll", "'", "\"", "’", "”", "—", "“"])
    vocab = {}
    cnt = -1
    timeRemoveList = []
    for i in text:
        temp = word_tokenize(i)
        # TreebankWordTokenizer().tokenize(i)
        # WordPunctTokenizer().tokenize(i)
        temp = list(filter(lambda x: x not in eliminateWord and x not in eliminateWord2, temp))
        #lemma = [WordNetLemmatizer().lemmatize(w).lower() for w in temp]
        cnt += 1
        if not temp:
            timeRemoveList.append(cnt)
            continue

        stem = [PorterStemmer().stem(w).lower() for w in temp]
        #tokenText.append(temp)
        #lemmaText.append(lemma)
        stemText.append(stem)

    cnt = 0
    if len(timeRemoveList) != 0:
        for i in timeRemoveList:
            del(time[i-cnt])
            cnt += 1

    #print(tokenText)
    #print(lemmaText)
    #print(stemText)

    file = open("stem_{}_en.txt".format(video_name), "w", encoding='UTF8')
    for i in range(len(time)):
        file.write(time[i] + "\n")
        for j in range(len(stemText[i])):
            file.write(stemText[i][j])
            if j != len(stemText[i]) - 1:
                file.write(" ")
        if i != len(time) - 1:
            file.write("\n")
    file.close()

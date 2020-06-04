from nltk.tokenize import word_tokenize, TreebankWordTokenizer, WordPunctTokenizer
from khaiii import KhaiiiApi
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
def preprocessing(url, video_name):
    yt = YouTube(url)
    caption = yt.captions.get_by_language_code('ko')
    print(video_name)
    caption.download(video_name) #기본 저장 형태가 srt인듯

    #file = open("subtitle.srt", "r")
    file = open("{} (ko).srt".format(video_name), "r", encoding='UTF8')
    subtitle = file.read()
    file.close()

    result = subtitle.split('\n\n')

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

    """file = open("stopwords_kor.txt", "r", encoding='UTF8')
    eliminateWord = file.read()
    file.close()
    eliminateWord = set(eliminateWord.split("\n")[:-1])
    eliminateWord2 = set(["'s", ".", ",", "'re", "?", "!", "'ll", "'", "\"", "’", "”", "—", "“"])
    """
    api = KhaiiiApi()
    # https://github.com/kakao/khaiii/wiki/%EC%BD%94%ED%8D%BC%EC%8A%A4    tag.
    useTag = set(["NNG", "NNP", "VV", "VA"])
    cnt = -1
    timeRemoveList = []
    stemText =[]
    
    for i in text:
        res = api.analyze(i)
        temp = []
        cnt += 1
        for i in res:
            #print(i.lex)# tokenized word
            for m in i.morphs:
                if m.tag in useTag:
                    temp.append(m.lex)
                    #print([(m.lex + '/' + m.tag) for m in i.morphs])
        if len(temp) == 0:
            timeRemoveList.append(cnt)
            continue
        stemText.append(temp)

    cnt = 0
    if len(timeRemoveList) != 0:
        for i in timeRemoveList:
            del(time[i-cnt])
            cnt += 1

    #print(stemText)

    file = open("stem_{}_ko.txt".format(video_name), "w", encoding='UTF8')
    for i in range(len(time)):
        file.write(time[i] + "\n")
        for j in range(len(stemText[i])):
            file.write(stemText[i][j])
            if j != len(stemText[i]) - 1:
                file.write(" ")
        if i != len(time) - 1:
            file.write("\n")
    file.close()
    return 0, subtitle

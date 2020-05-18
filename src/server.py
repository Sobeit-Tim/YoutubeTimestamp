from socket import *
import threading
import os
import time

class Client_Thread(threading.Thread):                       #스레드는 혹시 몰라 일단 내버려둚
    def __init__(self, connectionaddr, connectionSocket):    #소켓 초기값
        threading.Thread.__init__(self)
        self.csocket = connectionSocket
        self.caddr = connectionaddr
    def run(self):
        msg = ''
        newMsg = ''
        User_ID = ''
        while True:
            msg = self.csocket.recv(4096).decode()
            print("받은 메시지!")            #http 메시지가 어떤 형식으로 오는 지 볼 수 있음
            print(msg)
            print("----------")

            try:
                input = msg[msg.find("/") + 1:msg.find("HTTP") - 1]
                print("어떤 파일을 요구?")
                print(input)
                print("형식은?")
                print(msg[0:4])
                print("----------")
                fileopen = ''

                if input == '' or input == 'TimeStamp.html' and msg[0:4] != "POST":  #defalut 페이지로 TimeStamp.html로 설정 -> 후에 index.php로 변경해야 함
                    fileopen = 'TimeStamp.html'
                    input = open(fileopen, "rb")              #TimeStamp.html을 "rb"로 열어서 msg를 만들 것
                    str = 'HTTP/1.1 200 OK\r\n\r\n'           #str형태로 200 OK를 적은 후
                    newMsg = str.encode()                     #encode해서 byte로 바꿔줆
                    while True:
                        content = input.read(BUFFER)
                        if not content:
                            break
                        newMsg = newMsg + content             #TimeStamp.html을 byte로 열었으니까 그 뒤에 이어서 붙여주면 됨 -> 완성된 newMsg 소켓을 통해 보냄

                elif input == "style.css" or input == "pngwing.com.png": #TimeStamp.html을 열 때 요구하는 파일들(css파일과 검색이미지파일)
                    fileopen = input
                    input = open(fileopen, "rb")
                    str = 'HTTP/1.1 200 OK\r\n\r\n'
                    newMsg = str.encode()
                    while True:
                        content = input.read(BUFFER)
                        if not content:
                            break
                        newMsg = newMsg + content

                elif msg[0:4] == "POST":            #검색 창에 url을 입력한 것을 받을 때
                    fileopen = "TimeStamp.html"

                    body = msg.split("\r\n\r\n")
                    bodyList = body[1].split("&")
                    url = bodyList[0].split("=")[1]
                    print("url 주소는?")
                    print(url)

                    input = open(fileopen, "rb")
                    str = 'HTTP/1.1 200 OK\r\n\r\n'
                    newMsg = str.encode()
                    while True:
                        content = input.read(BUFFER)
                        if not content:
                            break
                        newMsg = newMsg + content

                elif "font" in input:           #폰트
                    fileopen = input
                    input = open(fileopen, "rb")
                    str = 'HTTP/1.1 200 OK\r\n\r\n'
                    newMsg = str.encode()
                    while True:
                        content = input.read(BUFFER)
                        if not content:
                            break
                        newMsg = newMsg + content



            except:
                print("no file")

            self.csocket.send(newMsg)
            self.csocket.close()

serverPort = 10080  #포트번호
HOST = ''
BUFFER = 4096
serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.bind((HOST, serverPort))
print("Listening")  #서버가 정상적으로 돌아가면 뜸
#mut = threading.Lock() #threading lock은 필요 없음


while True:
    serversocket.listen(100)
    connectionSocket, connectionaddr = serversocket.accept()
    newthread = Client_Thread(connectionaddr, connectionSocket)
    newthread.start()

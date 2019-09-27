# import threading
from threading import Event
from threading import Thread

import sys
# import os
import json

import requests

url = "http://127.0.0.1:8080/goldennum"
closeUser = ""
farUser = ""
userNum = 0
listUser = []
goldNum = 0
secretKey = sys.argv[1]
roomid = sys.argv[2]
sleeptime = int(sys.argv[3])
real_user_num = 0


class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(sleeptime):
            print("Thread start")
            getAct()
            submitResult()


class User:
    userName = ""
    userAct1 = 0
    userAct2 = 0

    def __init__(self, userName, userAct1, userAct2):
        self.userName = userName
        self.userAct1 = userAct1
        self.userAct2 = userAct2


def getAct():
    global goldNum
    global closeUser
    global farUser
    global userNum
    global listUser
    global listUserFree
    global real_user_num
    global close_num
    global far_num
    #print('Hello Timer1!')

    # send request
    requestData = {"roomid": roomid, "key": secretKey}
    # print(requestData)
    # values = requests.get(url+"/getAct/",params=requestData)
    res = requests.get(url+"/getAct/", params=requestData)
    print(res)
    values = res.json()
    userNum = values.get('userNum')
    real_user_num = 0
    users = values.get('users')

    listUserFree = []
    listUser = []
    # users=[{"userName":"abc","userAct":[1,2]},{"userName":"er","userAct":[6,7]}]  #测试代码

    # init
    for user in users:
        if user.get("userAct")[0] != 0 and user.get("userAct")[1] != 0:
            listUser.append(User(
                userName=user.get('userName'),
                userAct1=user.get("userAct")[0],
                userAct2=user.get("userAct")[1]
            ))
            real_user_num += 1
        else:
            listUserFree.append(User(
                userName=user.get('userName'),
                userAct1=user.get("userAct")[0],
                userAct2=user.get("userAct")[1]
            ))

    total = 0
    for user in listUser:
        total += user.userAct1
        total += user.userAct2
    if listUser:
        goldNum = (total / (real_user_num * 2))*0.618
    else:
        goldNum = 0

    close_num = 10000  # 最接近黄金数的数
    far_num = goldNum  # 离黄金数最远的

    for user in listUser:
        if real_user_num > 2:
            if abs(user.userAct1 - goldNum) < abs(close_num - goldNum):
                close_num = user.userAct1
                closeUser = user.userName
            if abs(user.userAct2 - goldNum) < abs(close_num - goldNum):
                close_num = user.userAct2
                closeUser = user.userName
            if abs(user.userAct1 - goldNum) > abs(far_num - goldNum):
                far_num = user.userAct1
                farUser = user.userName
            if abs(user.userAct2 - goldNum) > abs(far_num - goldNum):
                far_num = user.userAct2
                farUser = user.userName
    # for test
    # print(goldNum)
    # print(closeUser,close_num)
    # print(farUser,far_num)

    if res.status_code == 200:
        print("GET success")


def submitResult():
    requestData = {"roomid": roomid, "key": secretKey}
    data = {"roundTime": sleeptime, "goldenNum": goldNum,
            "userNum": userNum, "users": [], "debug": []}

    if real_user_num > 2:
        for user in listUser:
            score = 0
            if abs(user.userAct1 - close_num) < 0.0001 or abs(user.userAct2 - close_num) < 0.0001:
                score += real_user_num - 2
            if abs(user.userAct1 - far_num) < 0.0001 or abs(user.userAct2 - far_num) < 0.0001:
                score -= 2
            data.get("users").append(
                {"userName": user.userName, "userScore": score})
        for user in listUserFree:
            data.get("users").append(
                {"userName": user.userName, "userScore": 0})
            # if user.userName == closeUser:
            #     data.get("users").append({"userName":user.userName, "userScore":userNum - 2})
            # elif user.userName == farUser:
            #     data.get("users").append({"userName": user.userName, "userScore": -2})
            # else:
            #     data.get("users").append({"userName": user.userName, "userScore": 0})
    else:
        for user in listUser:
            data.get("users").append(
                {"userName": user.userName, "userScore": 0})
        for user in listUserFree:
            data.get("users").append(
                {"userName": user.userName, "userScore": 0})

    data_json = json.dumps(data)
    r = requests.post(url+"/submitResult/", params=requestData, data=data_json)
    if r.status_code == 200:
        print("POST success")


if __name__ == "__main__":
    stopFlag = Event()
    thread = MyThread(stopFlag)
    thread.start()

    # this will stop the timer
    # stopFlag.set()

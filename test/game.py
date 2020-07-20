import requests
import string
import random
import time


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


URL_BASE = "https://bot.jbesu.com/goldennum/"
URL_REG = URL_BASE + "userReg/"
URL_ACT = URL_BASE + "userAct/"
URL_OUT = URL_BASE + "userOut/"

ROOM_NAME = "test2"
ROUND_TIME = 10
USER_NUM = 40
USER_PREFIX = get_random_string(5)

if __name__ == "__main__":
    session_dict = {}
    for i in range(USER_NUM):
        session_dict[f"{USER_PREFIX}{i}"] = requests.Session()

    while True:
        time_next = time.time() + ROUND_TIME
        actions = {}
        for name in session_dict:
            s = session_dict[name]
            s.get(URL_REG, params={"name": name})

            num1 = random.random() * 100
            num2 = random.random() * 100
            submit = {
                "roomid": ROOM_NAME,
                "num1": num1,
                "num2": num2,
            }
            s.get(URL_ACT, params=submit)

            s.get(URL_OUT)

            actions[name] = [num1, num2]

        print(actions)

        time.sleep(max(0, time_next - time.time()))

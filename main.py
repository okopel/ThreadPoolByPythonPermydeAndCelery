import threading

import requests


def postThread(r_id):
    url = 'http://localhost:6543/upload'
    data = {r_id: [1, 2, 0.5, 20, 1 / 20, 1, 1, 1, 1, 1, r_id]}
    r = requests.post(url, auth=('username', 'password'), verify=False, json=data)


def getmsg():
    url = 'http://localhost:6543/results/34'
    p = requests.get(url)
    print(p.content)
    url = 'http://localhost:6543/results/8888880'
    p = requests.get(url)
    print(p.content)


if __name__ == '__main__':
    for i in range(80, 200):
        t = threading.Thread(target=postThread, args=(i,))
        t.start()

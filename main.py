import threading

import requests


def postThread(r_id):
    url = 'http://localhost:6543/upload'
    data = {r_id: [1, 2, 0.5, 20, 1 / 20, 1, 1, 1, 1, 1, r_id]}
    r = None
    try:
        r = requests.post(url, auth=('username', 'password'), verify=False, json=data)
    except:
        print(r_id, r)


def getmsg(r_id):
    url = 'http://localhost:6543/results/{}'.format(r_id)
    p = requests.get(url)
    print(p.content)


if __name__ == '__main__':
    for i in range(100):
        t = threading.Thread(target=postThread, args=(i,)).start()
        t1 = threading.Thread(target=getmsg, args=(i,)).start()

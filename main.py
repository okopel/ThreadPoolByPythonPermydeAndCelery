import requests

if __name__ == '__main__':
    url = 'http://localhost:6543/upload'
    # data = {90: [5, 7, 2], 98: [8, 3, 2], 97: [2, 5, 1]}
    data = {32: [5, 7, 2, 5, 5, 5, 5, 5, -5.0545], 24: [5, 7, 2, 5, 5, 5, 5, 5, -5]}
    r = requests.post(url, auth=('username', 'password'), verify=False, json=data)
    # print(r.status_code)
    url = 'http://localhost:6543/results/990'
    p = requests.get(url)
    url = 'http://localhost:6543/results/8888880'
    p = requests.get(url)

import requests

if __name__ == '__main__':
    url = 'http://localhost:6543/upload'
    data = {34: [5, 7, 2, 5, 5, 5, 5, 5, -5.0545], 29: [5, 7, 2, 5, 5, 5, 5, 5, -5]}
    r = requests.post(url, auth=('username', 'password'), verify=False, json=data)
    # print(r.status_code)
    url = 'http://localhost:6543/results/320'
    p = requests.get(url)
    url = 'http://localhost:6543/results/8888880'
    p = requests.get(url)

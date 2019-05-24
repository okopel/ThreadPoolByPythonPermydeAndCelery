import requests

if __name__ == '__main__':
    url = 'http://localhost:6543/upload'
    data = {99: [5, 7, 2], 100: [8, 3, 2], 500: [2, 5, 1]}
    r = requests.post(url, auth=('username', 'password'), verify=False, json=data)
    print(r.status_code)
    url = 'http://localhost:6543/results/500'
    p = requests.get(url)

import requests
import json
import urllib.request

if __name__ == '__main__':
    url = 'http://localhost:6543/upload'
    # req.add_header('Content-Type','application/json')
    data = {1: [5, 7, 2], 2: [8, 3, 2], 3: [2, 5, 1]}
    r = requests.post(url, auth=('username', 'password'), verify=False, json=data)
    print(r.status_code)
""""
    # r = requests.post("http://localhost:6543/upload", data=json.dumps(j))
    myurl = "http://localhost:6543/upload"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    print(jsondataasbytes)
    # response = urllib.request.urlopen(req, jsondataasbytes)
"""

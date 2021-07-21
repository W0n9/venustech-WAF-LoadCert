# %%
import hashlib
import json
import time
import base64

import requests

timestamp = int(round(time.time() * 1000))


def getStrAsMD5(parmStr):
    #1、参数必须是utf8
    #2、python3所有字符都是unicode形式，已经不存在unicode关键字
    #3、python3 str 实质上就是unicode
    if isinstance(parmStr, str):
        # 如果是unicode先转utf-8
        parmStr = parmStr.encode("utf-8")
    m = hashlib.new('md5')
    m.update(parmStr)
    return m.hexdigest()


def readConfig(filename):
    with open(filename, "r") as f:
        config = json.load(f)
        return config


config = readConfig("config.json")
ts = str(timestamp)
api_uri = "/v2/certInfo"
user = config["user"]
password = config["password"]

sign = user + ':' + getStrAsMD5(ts + api_uri + user + getStrAsMD5(password))

baseURL = config["baseURL"]
url = baseURL + api_uri

payload = {
    "action": "mod",
    "ts": ts,
    "sign": sign,
}

data = {
    "cert_file_name": "wildcard.crt",
    "key_file_name": "wildcard.key",
    "type": 3,
    "password": "",
    "cert_file_content": "",
    "key_file_content": "",
    "upload_location": 0
}

r = requests.post(url,
                  params=payload,
                  allow_redirects=False,
                  data=json.dumps(data))
print(r.json())

# %%

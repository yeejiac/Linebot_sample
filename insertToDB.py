from sqlalchemy import create_engine
from datetime import datetime
import os
import sys
import requests
import pandas as pd
parent_dir = os.path.dirname(sys.path[0])
sys.path.insert(0, parent_dir)
import configparser
import hashlib

config = configparser.ConfigParser()
config.read("config.ini")
LINE_CHANNEL_ACCESS_TOKEN = config['line_bot']['LINE_CHANNEL_ACCESS_TOKEN']

disk_engine = create_engine('sqlite:///friend_storage.db')

def getMD5(plaintext):
    m = hashlib.md5()
    m.update(plaintext.encode("utf-8"))
    hashtext = m.hexdigest()
    return hashtext

def getUserProfile(userID):
    try:
        url = 'https://api.line.me/v2/bot/profile/'+userID
        headers = {'Content-Type': 'application/json', 'Authorization':'Bearer {}'.format(LINE_CHANNEL_ACCESS_TOKEN)}
        r = requests.get(url, headers=headers)
        data = r.json()
        return data['displayName']
    except:
        print("error happen")

def insertDB(dataList):
    dataList[1] = getUserProfile(dataList[0])
    now = datetime.now()
    dataList.append(now.strftime("%d/%m/%Y %H:%M:%S"))
    dataList[0] = getMD5(dataList[0])
    print(dataList)
    df = pd.DataFrame([dataList], columns=['userID','userName', 'Text', 'dateTime'])
    df.to_sql('friend_info', disk_engine, if_exists='append')
    showTable('select * from `friend_info`')

def showTable(sql):
    df = pd.read_sql(sql, disk_engine)
    print(df)
    return df

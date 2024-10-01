import os
from http.client import HTTPConnection
from base64 import b64encode
import json
from datetime import datetime
from dotenv import load_dotenv

# username and password for JUDO
load_dotenv()
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


def HTTPGetRequest(method: str, body: str):
    c = HTTPConnection("192.168.178.71")
    headers = {'Authorization': basic_auth(username, password)}
    c.request(method, body, headers=headers)
    res = c.getresponse()
    return res.read()

# Device information

def ReadDeviceType():
    data = HTTPGetRequest('GET', '/api/rest/FF00')
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    if data["data"] == '44':
        return "ZEWA i-SAFE FILT"
    else:
        return "UNKNOWN"


def ReadDeviceNumber():
    data = HTTPGetRequest('GET', '/api/rest/0600')
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    deviceNumber = data["data"][6:8] + data["data"][4:6] + data["data"][2:4] + data["data"][0:2]
    return int(deviceNumber, 16)


def ReadDeviceControlSoftwareVersion():
    data = HTTPGetRequest('GET', '/api/rest/0100')
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    swVersion = str(int(data["data"][4:6],16)) + '.' + str(int(data["data"][2:4],16)) + 'f'
    return swVersion


def ReadCommissioningDate():
    data = HTTPGetRequest('GET', '/api/rest/0E00')
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    dateInt = int(data["data"],16)
    return datetime.utcfromtimestamp(dateInt).strftime('%Y-%m-%d %H:%M:%S')


# Operating Data

# m^3
def ReadTotalWaterVolume():
    data = HTTPGetRequest('GET', '/api/rest/2800')
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"][6:8] + data["data"][4:6] + data["data"][2:4] + data["data"][0:2]
    water = int(water, 16)
    water = water/1000
    return water


# Water usage statistics

def ReadDayWaterUsage(day: int, month: int, year: int):
    dateToPass = "{:02x}".format(day) + "{:02x}".format(month) + "{:04x}".format(year)
    body = '/api/rest/FB00' + dateToPass
    data = HTTPGetRequest('GET', body)
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    hour00_03 = int(water[0:8], 16)
    hour03_06 = int(water[9:16], 16)
    hour06_09 = int(water[17:24], 16)
    hour09_12 = int(water[25:32], 16)
    hour12_15 = int(water[33:40], 16)
    hour15_18 = int(water[41:48], 16)
    hour18_21 = int(water[49:56], 16)
    hour21_24 = int(water[57:64], 16)
    return [hour00_03, hour03_06, hour06_09, hour09_12, hour12_15, hour15_18, hour18_21, hour21_24]


def ReadWeekWaterUsage(kw: int, year: int):
    dateToPass = "{:02x}".format(kw) + "{:04x}".format(year)
    body = '/api/rest/FC00' + dateToPass
    data = HTTPGetRequest('GET', body)
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    monday = int(water[0:8], 16)
    tuesday = int(water[9:16], 16)
    wednesday = int(water[17:24], 16)
    thursday = int(water[25:32], 16)
    friday = int(water[33:40], 16)
    saturday = int(water[41:48], 16)
    sunday = int(water[49:56], 16)
    return [monday, tuesday, wednesday, thursday, friday, saturday, sunday]


def ReadMonthWaterUsage(month: int, year: int):
    dateToPass = "{:02x}".format(month) + "{:04x}".format(year)
    body = '/api/rest/FD00' + dateToPass
    data = HTTPGetRequest('GET', body)
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    return_value = []
    for i in range(0, len(str(water))//8):
        return_value += [int(water[i*8:(i*8)+8], 16)]
    return return_value


def ReadYearWaterUsage(year: int):
    dateToPass = "{:04x}".format(year)
    body = '/api/rest/FE00' + dateToPass
    print(body)
    data = HTTPGetRequest('GET', body)
    print(data)
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    return_value = []
    for i in range(0, 12):
        return_value += [int(water[i * 8:(i * 8) + 8], 16)]
    return return_value


# Settings

def ReadSleepModeDuration():
    data = HTTPGetRequest('GET', '/api/rest/6600')
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    return int(water, 16)


def ReadLearningModeState():
    data = HTTPGetRequest('GET', '/api/rest/6400')
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    learnmodus_activ = bool(int(water[0:2],16))
    restWater = int(water[2:4])
    return learnmodus_activ, restWater


# 0-no automatic check; 1-automatic check with notification; 2-automatic check with notification and closing
def ReadLeackageCheckState():
    data = HTTPGetRequest('GET', '/api/rest/6500')
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    return int(water)


def ReadDateAndTime():
    data = HTTPGetRequest('GET', '/api/rest/5900')
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    data = data["data"]
    data = str(int(data[0:2],16)) + '.' + str(int(data[2:4],16)) + '.' + str(int(data[4:6],16)) + ' - ' + str(int(data[6:8],16)) + ':' + str(int(data[8:10],16)) + ':' + str(int(data[10:12],16))
    return data


# TODO: function not finished
def ReadOutOfHomeTime():
    data = HTTPGetRequest('GET', '/api/rest/6000')
    print(data)
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    data = str(int(data["data"]),16)
    return data
print(ReadOutOfHomeTime())
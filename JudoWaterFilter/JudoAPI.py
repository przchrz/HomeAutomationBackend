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


def ReadTotalWaterVolume():
    data = HTTPGetRequest('GET', '/api/rest/2800')
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"][6:8] + data["data"][4:6] + data["data"][2:4] + data["data"][0:2]
    water = int(water, 16)
    water = water/1000
    return water


# Water usage statistics

# TODO: function not finished
def ReadDayWaterUsage(day: int, month: int, year: int):
    dateToPass = "{:02x}".format(day) + "{:02x}".format(month) + "{:04x}".format(year)
    body = '/api/rest/FB00' + dateToPass
    print(body)
    data = HTTPGetRequest('GET', body)
    print(data)
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    return water


# TODO: function not finished
def ReadWeekWaterUsage(kw: int, year: int):
    dateToPass = "{:02x}".format(kw) + "{:04x}".format(year)
    body = '/api/rest/FC00' + dateToPass
    print(body)
    data = HTTPGetRequest('GET', body)
    print(data)
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    return water


# TODO: function not finished
def ReadMonthWaterUsage(month: int, year: int):
    dateToPass = "{:02x}".format(month) + "{:04x}".format(year)
    body = '/api/rest/FD00' + dateToPass
    print(body)
    data = HTTPGetRequest('GET', body)
    print(data)
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    return water


# TODO: function not finished
def ReadYearWaterUsage(year: int):
    dateToPass = "{:04x}".format(year)
    body = '/api/rest/FE00' + dateToPass
    print(body)
    data = HTTPGetRequest('GET', body)
    print(data)
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    return water

# Settings

# TODO: function not finished
def ReadSleepModeDuration():
    data = HTTPGetRequest('GET', '/api/rest/6600')
    print(data)
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    return water


# TODO: function not finished
def ReadLearningModeState():
    data = HTTPGetRequest('GET', '/api/rest/6400')
    print(data)
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    return water


# TODO: function not finished
def ReadLeackageCheckState():
    data = HTTPGetRequest('GET', '/api/rest/6500')
    print(data)
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    water = data["data"]
    return water


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

print(ReadDateAndTime())
import os
import math
import random
import requests

from datetime import date, datetime
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate

today = datetime.now()

# 微信公众测试号ID和SECRET
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

# 可把os.environ结果替换成字符串在本地调试
user_ids = os.environ["USER_ID"].split(',')
template_ids = os.environ["TEMPLATE_ID"].split(',')

poetry_type = os.environ["POETRY"].split(',')

# 获取天气和温度
def get_weather(city):
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp'])

# 获取古诗词
def get_poetry(poetry_type):
    param = ""
    for item in poetry_type:
        param = param + "c=" + item + "&"
    url = "https://v1.hitokoto.cn/?" + param
    res = requests.get(url).json()
    return res['from'],res['from_who'],res['hitokoto']



# 字体随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

for i in range(len(user_ids)):
    title,author,content = get_poetry(poetry_type)
    data = {
          "title": {"value": "标题{}".format(title)},
          "author": {"value": "作者{}".format(author)},
          "content": {"value": "内容{}".format(content)}
    }
    res = wm.send_template(user_ids[i], template_ids[i], data)
    print(res)

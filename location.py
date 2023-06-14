import random

import requests

import mysql


# 写入定位
def Writ(writ_user) -> None:
    print("  写入数据库：定位")
    sql = f"""UPDATE users SET longitude="{writ_user['longitude']}",latitude="{writ_user['latitude']}" WHERE name = '{writ_user["name"]}';"""
    mysql.update(sql=sql)


# 修改定位
def ModifyPositioning(position_user) -> dict:  # 用户信息 定位路径
    if position_user["latitude"] == '':
        lng, lat = Req(position_user['address'])
        position_user["latitude"] = lat
        position_user["longitude"] = lng
    print("    修改定位")
    latitude: str = str(position_user["latitude"])
    longitude: str = str(position_user["longitude"])
    position_user["latitude"] = latitude[0:len(latitude) - 1] + str(random.randint(0, 10))
    position_user["longitude"] = longitude[0:len(longitude) - 1] + str(random.randint(0, 10))
    Writ(writ_user=position_user)
    return position_user


# 获取定位
def Req(address) -> tuple:  # 详细地址
    print("    获取定位")
    url = f'https://apis.map.qq.com/ws/geocoder/v1/?address={address}&key=XN6BZ-6YYEX-2OE4C-ZTGOK-EAQRV-IZBZG'
    heasers = {
        'sec-ch-ua-platform': 'Windows',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.46'
    }
    res = requests.get(url=url, headers=heasers, ).json()
    lng = res['result']['location']['lng']
    lat = res['result']['location']['lat']
    # 经度
    if len(str(lng).split('.')[1]) < 6:
        lng = f"{str(lng).split('.')[0]}.{str(lng).split('.')[1]}{'0' * int(6 - len(str(lng).split('.')[1]))}"
    elif len(str(lng).split('.')[1]) > 6:
        lng = f"{str(lng).split('.')[0]}.{str(lng).split('.')[1][:6]}"
    # 维度
    if len(str(lat).split('.')[1]) < 6:
        lat = f"{str(lat).split('.')[0]}.{str(lat).split('.')[1]}{'0' * int(6 - len(str(lat).split('.')[1]))}"
    elif len(str(lat).split('.')[1]) > 6:
        lat = f"{str(lat).split('.')[0]}.{str(lat).split('.')[1][:6]}"
    return lng, lat

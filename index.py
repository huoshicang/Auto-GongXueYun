import datetime
import json
import time

import requests

import mysql
from UA import GetUserAgent
from getToken import getToken
from location import ModifyPositioning
from planId import GetPlanId
from save import Save
from signrecord import SignRecord


# 写入用户信息
def Writ(writ_user: dict) -> None:
    print("  写入数据库：token userid planid")
    sql = f"""UPDATE users SET token="{writ_user['token']}",userId="{writ_user['userId']}",planId="{writ_user['planId']}" WHERE name = '{writ_user["name"]}';"""
    mysql.update(sql=sql)


# 加入要推送的总消息
def SuccessFailure(name: str, sign: str, position: str, characteristic_push: str,
                   push_text: dict) -> None:  # 名字 签到 位置 推送
    if '不签' == sign:
        push_text[
            "content"] += f'<span style="color:gray">{name} | {sign} | {position} | {characteristic_push}</span><br/>'
    elif "失败" in position:
        push_text[
            "content"] += f'<span style="color:red">{name} | {sign} | {position} | {characteristic_push}</span><br/>'
    elif "空" in characteristic_push:
        push_text[
            "content"] += f'<span style="color:blue">{name} | {sign} | {position} | {characteristic_push}</span><br/>'
    else:
        push_text["content"] += f'<span>{name} | {sign} | {position} | {characteristic_push}</span><br/>'


# 获取token userid planid
def GetToken(getToken_user: dict, getToken_UA: str, getToken_push_text: dict) -> None:
    get_token_text: dict = getToken(get_token_user=getToken_user, Ua=getToken_UA)
    if "token" in get_token_text and "userId" in get_token_text:
        getToken_user['token'] = get_token_text['token']
        getToken_user['userId'] = get_token_text['userId']
    elif "sign" in get_token_text:
        SuccessFailure(name=user['name'], sign=get_token_text['sign'], position=get_token_text['position'],
                       characteristic_push=get_token_text['characteristic_push'], push_text=getToken_push_text)
        print("请求token失败，退出")
        return

    get_plan_text: dict = GetPlanId(get_planid_user=getToken_user, Ua=getToken_UA)
    if "planId" in get_plan_text:
        getToken_user['planId'] = get_plan_text['planId']
    elif "sign" in get_plan_text:
        SuccessFailure(name=user['name'], sign=get_token_text['sign'], position=get_token_text['position'],
                       characteristic_push=get_token_text['characteristic_push'], push_text=getToken_push_text)
        print("请求planid失败，退出")
        return

    Writ(writ_user=getToken_user)
    Sing(sing_user=getToken_user, sing_UA=getToken_UA, sign_push_text=getToken_push_text)  # 执行签到


# 判断是否需要签到并执行
def Sing(sing_user: dict, sing_UA: str, sign_push_text: dict) -> None:
    sign_record_test: dict = SignRecord(sign_record_user=sing_user, Ua=sing_UA)
    if "请求失败" == sign_record_test['sign']:
        SuccessFailure(name=sing_user['name'], sign=sign_record_test['sign'], position=sign_record_test['position'],
                       characteristic_push=sign_record_test['characteristic_push'], push_text=sign_push_text)
        print("请求记录失败，退出")
        return
    elif "token失效" == sign_record_test['sign']:
        GetToken(getToken_user=sing_user, getToken_UA=sing_UA, getToken_push_text=sign_push_text)
    elif "不需要签到" == sign_record_test['sign']:
        SuccessFailure(name=sing_user['name'], sign=sign_record_test['sign'], position=sign_record_test['position'],
                       characteristic_push=sign_record_test['characteristic_push'], push_text=sign_push_text)
    elif "没签过" == sign_record_test['sign'] or "需要签到" == sign_record_test['sign']:
        position_user_dict = ModifyPositioning(position_user=sing_user)
        save_text = Save(save_user=position_user_dict, Ua=sing_UA)
        # if "请求失败" == save_text['sign']:
        SuccessFailure(name=sing_user['name'], sign=save_text['sign'], position=save_text['position'],
                       characteristic_push=save_text['characteristic_push'], push_text=sign_push_text)


# 华为云入口
def handler(event, context):
    # 初始化全局变量
    time_start: float = time.time()
    user: dict = {}
    push_text: dict = {
        'channel': "wechat",
        'content': "",
        'template': "html",
        'title': f"{datetime.date.today()}    签到情况",
        'token': "8579e1dbab214980ab26f738e669f954",
    }
    # 连接数据库获取需要签到的用户信息
    user_information_list = mysql.query_data()
    # 循环用户列表
    for user_information in user_information_list:

        time.sleep(90)
        UA: str = GetUserAgent()
        user = {
            "name": user_information[1],
            "phone": user_information[2],
            "password": user_information[3],
            "token": user_information[4],
            "userId": user_information[5],
            "planId": user_information[6],
            "country": user_information[7],
            "province": user_information[8],
            "city": user_information[9],
            "area": user_information[10],
            "desc": user_information[11],
            "type": user_information[12],
            "address": user_information[13],
            "longitude": user_information[14],
            "latitude": user_information[15],
            "pushKey": user_information[16],
        }
        print(f"\n\n{user['name']}签到  ", end="进入休眠 ")
        if user['token'] == "":
            print("没有Token")
            GetToken(getToken_user=user, getToken_UA=UA, getToken_push_text=push_text)
        else:
            print("有token")
            Sing(sing_user=user, sing_UA=UA, sign_push_text=push_text)
    time_end: float = time.time()
    push_text['content'] += f'<p><b>{datetime.timedelta(seconds=time_end - time_start)}</b></p>'
    print("开始推送情况")
    requests.post(url='https://www.pushplus.plus/api/send', data=json.dumps(push_text))

    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "body": json.dumps(event),
        "headers": {
            "Content-Type": "application/json"
        }
    }

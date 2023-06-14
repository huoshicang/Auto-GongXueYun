import datetime
import json

import requests


def push(push_user: dict, createTime: str, savecode=None) -> str:  # 用户信息 签到时间 签到标识=None
    global res
    print("    推送", end="    ")
    code = "失败"
    a = ''
    now = datetime.datetime.now()
    if savecode == 200:
        code = '成功'
    if (now.weekday() + 1) == 7 or (now.weekday() + 1) == 6:
        a = f'今天星期{now.weekday() + 1}，有周报'
    if (now.day == 30) or (now.day == 31):
        a += f'今天是{now.day}，有月报'
    data = {
        'channel': "wechat",
        'content': f"""
|签到情况|
| :-: |
|{code} {createTime}|
|{push_user["name"]} {push_user["phone"]}|
|{push_user["address"]}|
|{a}|
|联系方式:没想好|
|毕竟不是正常签到，难免会出现问题|
|不确定，可以登录看看|
""",
        # | {sign_in_count(sign_in_count_user=push_user, )} |
        'template': "markdown",
        'title': f"{push_user['name']}  {code}签到情况",
        'token': f"{push_user['pushKey']}",
    }
    try:
        # return('200')
        res = requests.post(url='https://www.pushplus.plus/api/send', data=json.dumps(data)).json()
    except:
        pass

    if res['code'] == 200:
        return '200'
    else:
        return res['msg']
    # SuccessFailure(judgment_value=(user['name'], code, res["code"], msg))

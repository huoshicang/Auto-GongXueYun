import pymysql


def get_conn():
    print("  连接数据库")
    return pymysql.connect(
        host='',  # 地址
        user="",  # 用户
        password="177155",  # 密码
        database="",  # 表名
        port=3306,  # 端口
        # charset="utf-8"
    )


# "SELECT * FROM users WHERE enable='true';"
def query_data() -> tuple:
    print("  获取数据库数据")
    conn = get_conn()
    try:
        cur = conn.cursor()
        sql = "SELECT * FROM users;"
        cur.execute(sql)
        return cur.fetchall()
    finally:
        conn.close()


def update(sql):
    print("更新数据库数据")
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except:
        print("修改失败")
    finally:
        conn.close()

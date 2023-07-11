import json
import time
import sqlite3
import os
import requests
from datetime import datetime
from datetime import timedelta
from sqlite3 import Error


# db connect function
def connect_db():
    try:
        con = sqlite3.connect(
            '/var/lib/docker/volumes/dockprom_grafana_data/_data/grafana.db')  # db connect
        return con
    except Error:
        print(Error)


#
def find_info():
    with open('/root/dockprom/customer/info.txt', 'r') as info:
        print(info)


# api call function
def call_php(status, time):
    server_instance = "jun01"
    # server_value = 99
    # server_time = 10
    datas = {
        'id_type': 'MID',
        'id': '',
        'auth_key': '',
        'msg_type': 'KAT',
        'callback_key': '',
        'send_id_receive_number': '0260076273|01047249812',
        'template_code': 'dream_01',
        # 'content': '(드림라인 알림톡 발송)\n\n서버 : %s' % server_instance + '\n값 : %d' % server_value + '\n발생시간 : %d' % server_time + '\n\n감사합니다.',
        'content': '(드림라인 알림톡 발송)\n\n서버 : {}\n값 : {}\n발생시간 : {}\n\n감사합니다.'.format(server_instance, status, time),
        'resend': 'NONE'
    }

    url = 'https://ums.dreamline.co.kr/API/send_kkt.php'
    response = requests.post(url, data=datas, timeout=2)

    if response.status_code == 200:
        print(json.loads(response.text))
    print(datas)


# json_crawling function
def json_crawling():
    con = connect_db()
    cur = con.cursor()
    sql = "select id, new_state, prev_state, text, updated from annotation where prev_state = 'Pending' AND new_state = 'Alerting'"
    # json_object('uid', id, 'after_state', new_state, 'before_state', prev_state, 'data_value', text, 'alert_time', updated) AS json_result
    cur.execute(sql)
    json_read = cur.fetchall()
    for a in json_read:
        df = datetime.fromtimestamp(a[4]/1000)
        seconds = (datetime.now() - df).total_seconds()
        print('%s' % seconds)
        if seconds <= 12000:
            c = a[1]
            print('{}, {}'.format(c, df))
            call_php(c, df)
        # elif prev_state -> Alerting and new_state -> Normal --> OK:
        #
        else:
            print("no error")
    return 0


# apply
if __name__ == '__main__':
    json_crawling()
    # find_info()
    # call_php()

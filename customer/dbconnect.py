import json
import sqlite3
import requests
from datetime import datetime
from sqlite3 import Error

global path
path = '/data/docker/volumes/dockprom'
#path = '/var/lib/docker/volumes/dockprom_grafana_data/_data/grafana.db'


# db connect function
def connect_db():
    try:
        # con = sqlite3.connect('/var/lib/docker/volumes/dockprom_grafana_data/_data/grafana.db')  # db connect
        con = sqlite3.connect(path)
        return con
    except Error:
        print(Error)


# find IP from info.txt
def find_info(error_ip):
    with open('/root/dockprom/customer/info.txt', 'r') as info:
        for a in info:
            list_ip = a.strip().split('|')
            if error_ip == list_ip[3]:
                return (list_ip[1], list_ip[2], list_ip[4])
    return None


# api call function
def call_php(company_name, person, phone_number, server_instance, status, time):
    value = 100
    type = 'disk'
    datas = {
        'id_type': 'MID',
        'id': '',
        'auth_key': '',
        'msg_type': 'KAT',
        'callback_key': '',
        'send_id_receive_number': '0260076273|{}'.format(phone_number),
        'template_code': 'dream_test01',
        'content': '(드림라인 알림톡 발송)\n알림 안내\n{} {}님, 안녕하세요.\n서버 : {} {}의\n값이 {}으로 임계치를 초과한 상태 입니다.\n서버 담당자확인 후 통보 드리겠습니다.'.format(company_name, person, server_instance, type, value),
        'resend': 'NONE'
    }
    # url = 'https://ums.dreamline.co.kr/API/send_kkt.php'
    # response = requests.post(url, data=datas, timeout=2)
    # if response.status_code == 200:
    #     print(json.loads(response.text))
    # else:
    #     print("Failed to send HTTP request")
    print(datas)


# json_crawling function
def json_crawling():
    con = connect_db()
    cur = con.cursor()
    sql = "select id, new_state, prev_state, text, updated from annotation where prev_state = 'Pending' AND new_state = 'Alerting'"
    cur.execute(sql)
    json_read = cur.fetchall()
    print(json_read)
    if json_read is not None:
        for a in json_read:
            df = datetime.fromtimestamp(
                a[4]/1000).strftime("%Y-%m-%d %H:%M:%S")
            seconds = (datetime.now() - datetime.strptime(df,
                       "%Y-%m-%d %H:%M:%S")).total_seconds()
            if seconds <= 15000:
                c = a[1]
                error_ip = a[3].split(' ')
                error_ip_fix = error_ip[0]
                info = find_info(error_ip[0])
                if info is not None:
                    company_name, person, phone_number = info
                    call_php(company_name, person,
                             phone_number, error_ip_fix, c, df)
                else:
                    print("No company name and phone number found")
            else:
                print("No match found for ip")
    else:
        print("No data found")
    return 0


# apply
if __name__ == '__main__':
    json_crawling()

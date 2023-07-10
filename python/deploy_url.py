import requests as req
import time
import pymysql
from datetime import datetime

dbcon = pymysql.connect(host='maria', user='root', password='wnsgmldi1', db='test', charset='utf8')
cur = dbcon.cursor()

# check 대상 api
#sites = ('서비스URL', '서비스URL2')
#sites = ('http://101.202.100.142:8081', 'http://101.202.100.142:8080', 'http://101.202.100.131:8000', 'http://101.202.100.131:3000', 'https://www.naver.com','https://google.com/')
sites = ('http://101.202.100.142:8081', 'http://101.202.100.131:8000')

# 슬랙 메세지 전송 함수
def send_slack_message(msg):
    # grafana alert
    # webhook_url = "https://hooks.slack.com/services/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"
    # vmware alert
    webhook_url = "https://hooks.slack.com/services/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"
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
    payload = {
        "text": "[ERROR] \n" +
        today + "\n" + msg
    }
    req.post(webhook_url, json=payload)

def send_db_status():
    sql = 'insert into info (date,URL,status) values ("%s", "%s", "%s")' % (str(datetime.today())[:19], site, r.status_code)
    cur.execute(sql)

# 서비스 체크
for site in sites:
    r = req.get(site)
    #code_list = ['200', '201', '202', '203', '204', '205', '206]
    if r.status_code != 200:
      send_slack_message("[" + site + "]" + " service is not running !!")
      print(site, 'return_code :', r.status_code)
      send_db_status()
      print("send_db_status")
    else:
      print(site, 'return_code :', r.status_code)
      send_db_status()
    dbcon.commit()
    time.sleep(5)

dbcon.close()

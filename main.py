import pymysql.cursors
import pandas as pd
from datetime import datetime, timedelta
import requests
from dotenv import dotenv_values
# Connect to the database
config = dotenv_values(".env")

connection = pymysql.connect(host=config['DB_HOST'],
                             user=config['DB_USER'],
                             password=config['DB_PWD'],
                             database=config['DB_NAME'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

data = []
with connection:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `wp_frm_item_metas`"
        cursor.execute(sql, ())
        result = cursor.fetchall()
        for i in range(0, len(result), 10):
            record = {}
            for j in result[i:i+10]:
                if j['field_id'] == 6:
                    record['phone_num'] = j['meta_value']
                if j['field_id'] == 16:
                    record['dob'] = j['meta_value']
                if j['field_id'] == 17:
                    record['dob'] = record['dob'] + "-" + j['meta_value']
            data.append(record)
todays_birthdays = []
two_days_from_now = datetime.now() + timedelta(days=2)
currentDay = str(two_days_from_now.day)
currentMonth = str(two_days_from_now.month)
todays_day_month = currentDay + "-" + currentMonth

for i in data:
    if i['dob'] == todays_day_month:
        todays_birthdays.append("+61"+i['phone_num'])

headers = {"APPKEY": config['APPKEY'], 'Accept': "application/json", "Content-Type": "application/json"}
r = requests.post("https://cellcast.com.au/api/v3/send-sms", headers=headers, data={"sms_text": "Hi Hari, Vikky Testing", "numbers": todays_birthdays})
# r = requests.post(config['URL'], data={"sms_text": "Hi Hari, Vikky Testing", "numbers": todays_birthdays})


print(todays_birthdays)

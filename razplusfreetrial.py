"""This is for razplus-trial"""
import random
import string
import sys
import time
from queue import Queue
from threading import Thread

import pyquery
import requests

rs = requests.Session()

def get_email(q):
    # Get Email address
    print("in get_email ...")
    mail_url = "https://10minutemail.com/10MinuteMail/index.html"
    mail_final_url = rs.get(mail_url).url
    r_mail = rs.get(mail_final_url).text
    pq = pyquery.PyQuery(r_mail)
    mail_address = pq('#mailAddress').attr("value")
    q.put(mail_address)


def check_email(q):
    # Check Email
    print("in check_email ...")
    start_time = time.time()
    while True:
        mail_final_url = rs.get("https://10minutemail.com/10MinuteMail/index.html").url
        r_mail = rs.get(mail_final_url).text
        pq = pyquery.PyQuery(r_mail)
        mail = pq('#mail-clock-wrapper > div.mail-notification.unread')
        print(mail)
        time.sleep(1)
        stop_time = time.time()
        if (stop_time - start_time) > 120:
            break


def register_razplus(q):
    # Register in raz-plus
    print("in register_razplus ...")
    mail_address = q.get()
    username = mail_address.split("@")[0]
    f_name = ''.join(random.sample(string.ascii_letters, 4))
    l_name = ''.join(random.sample(string.ascii_letters, 4))
    rs_razplus = requests.Session()
    rs_razplus.get(
        "https://accounts.learninga-z.com/accountsweb/marketing/trial.do?campaign=trialbtnnxtologoRP"
    )
    headers = {
        "Content-Type":
            "application/x-www-form-urlencoded",
        "Connection":
            "keep-alive",
        "Upgrade-Insecure-Requests":
            "1",
        "Host":
            "accounts.learninga-z.com",
        "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Origin":
            "https://accounts.learninga-z.com",
        "Referer":
            "https://accounts.learninga-z.com/accountsweb/marketing/trial.do?campaign=trialbtnnxtologoRP"
    }
    payload = {
        "mdrQuery.stateId": 0,
        "mdrQuery.mdrType": "public",
        "international": "true",
        "mdrQuery.useMdr": "false",
        "campaignName": "trialbtnnxtologoRP",
        "org": "HHJJKK",
        "customerType": "new",
        "usageType": "classroom",
        "firstName": f_name,
        "lastName": l_name,
        "zip": 99999,
        "countryId": 98,
        "email": mail_address,
        "occupation": 39,
        "mdrQuery.freeFormOrgName": "HHJJKK",
        "newUserUsername": username
    }
    response = rs_razplus.post(
        "https://accounts.learninga-z.com/accountsweb/marketing/trial.do",
        data=payload,
        headers=headers)
    if "An email has been sent" in response.text and mail_address in response.text:
        print("Registed in RAZPLUS Successfully!")
    else:
        print("Registed in RAZPLUS failed!")
        sys.exit()


if __name__ == "__main__":
    q = Queue()
    t1 = Thread(target=get_email, args=(q,), name="get_email")
    t2 = Thread(target=register_razplus, args=(q,), name="razplus")
    t3 = Thread(target=check_email, args=(q,), name="check_email")
    t1.start()
    t1.join()
    t2.start()
    t2.join()
    t3.start()
    t3.join()

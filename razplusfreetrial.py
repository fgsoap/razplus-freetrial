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
    headers = {
        "authority":
            "tempail.com",
        "user-agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "sec-fetch-mode":
            "navigate"
    }
    print("in get_email ...")
    r_mail = rs.get("https://tempail.com/en/", headers=headers).text
    pq = pyquery.PyQuery(r_mail)
    mail_address = pq('#eposta_adres').attr('value')
    print(mail_address)
    q.put(mail_address)


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


def check_email():
    # Check Email
    print("in check_email ...")
    start_time = time.time()
    while True:
        r_mail = rs.get("https://tempail.com/en/").text
        pq = pyquery.PyQuery(r_mail)
        mail = pq('.mail ').attr('id')
        print(mail)
        if mail is not None:
            msg = rs.get("https://tempail.com/en/" + mail).text
            pq = pyquery.PyQuery(msg)
            razplus_msg = pq('#iframe').attr('src')
            print(razplus_msg)
            break
        time.sleep(1)
        stop_time = time.time()
        if (stop_time - start_time) > 120:
            break


if __name__ == "__main__":
    q = Queue()
    t1 = Thread(target=get_email, args=(q,), name="get_email")
    t2 = Thread(target=register_razplus, args=(q,), name="razplus")
    t3 = Thread(target=check_email, args=(), name="check_email")
    t1.start()
    t1.join()
    t2.start()
    t2.join()
    t3.start()
    t3.join()

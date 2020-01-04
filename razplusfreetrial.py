"""This is for razplus-trial"""
import random
import string
import sys
import time
from queue import Queue

import pyquery
import requests

rs = requests.Session()


class RazPlusFreeTrial:
    def __init__(self, queue, url, register_url):
        self.queue = queue
        self.url = url
        self.register_url = register_url

    def register(self):
        mail_address = self.queue.get()
        username = mail_address.split("@")[0]
        rs_razplus = requests.Session()
        rs_razplus.get(self.url)
        payload = {
            "mdrQuery.stateId": 0,
            "mdrQuery.mdrType": "public",
            "international": "true",
            "mdrQuery.useMdr": "false",
            "campaignName": "trialbtnnxtologoRP",
            "org": "HHJJKK",
            "customerType": "new",
            "usageType": "classroom",
            "firstName": ''.join(random.sample(string.ascii_letters, 4)),
            "lastName": ''.join(random.sample(string.ascii_letters, 4)),
            "zip": 99999,
            "countryId": 98,
            "email": mail_address,
            "occupation": 39,
            "mdrQuery.freeFormOrgName": "HHJJKK",
            "newUserUsername": username
        }
        response = rs_razplus.post(self.register_url, data=payload)
        if "An email has been sent" in response.text and mail_address in response.text:
            print("Registed in RazPlus Successfully!")
        else:
            print("Registed in RazPlus failed!")
            sys.exit()


class TempEmail:
    def __init__(self, url, queue):
        self.url = url
        self.queue = queue

    def get_email(self):
        mail = rs.get(self.url).text
        pq = pyquery.PyQuery(mail)
        mail_address = pq('#eposta_adres').attr('value')
        self.queue.put(mail_address)

    def check_mail(self):
        start_time = time.time()
        while True:
            r_mail = rs.get(self.url).text
            pq = pyquery.PyQuery(r_mail)
            mail = pq('.mail ').attr('id')
            print(mail)
            if mail is not None:
                pq = pyquery.PyQuery(rs.get(self.url + mail).text)
                msg = rs.get(pq('#iframe').attr('src')).text
                pq = pyquery.PyQuery(msg)
                msg_url = pq('tbody tr td table tr td a').attr('href')
                print(msg_url)
                self.queue.put(msg_url)
                break
            time.sleep(5)
            stop_time = time.time()
            if (stop_time - start_time) > 120:
                print("Failed to get registered!")
                break


# def get_email(q):
#     # Get Email address
#     print("in get_email ...")
#     r_mail = rs.get("https://tempail.com/en/").text
#     pq = pyquery.PyQuery(r_mail)
#     mail_address = pq('#eposta_adres').attr('value')
#     print(mail_address)
#     q.put(mail_address)
#
#
# def register_razplus(q):
#     # Register in raz-plus
#     print("in register_razplus ...")
#     mail_address = q.get()
#     username = mail_address.split("@")[0]
#     rs_razplus = requests.Session()
#     rs_razplus.get(
#         "https://accounts.learninga-z.com/accountsweb/marketing/trial.do?campaign=trialbtnnxtologoRP"
#     )
#     payload = {
#         "mdrQuery.stateId": 0,
#         "mdrQuery.mdrType": "public",
#         "international": "true",
#         "mdrQuery.useMdr": "false",
#         "campaignName": "trialbtnnxtologoRP",
#         "org": "HHJJKK",
#         "customerType": "new",
#         "usageType": "classroom",
#         "firstName": ''.join(random.sample(string.ascii_letters, 4)),
#         "lastName": ''.join(random.sample(string.ascii_letters, 4)),
#         "zip": 99999,
#         "countryId": 98,
#         "email": mail_address,
#         "occupation": 39,
#         "mdrQuery.freeFormOrgName": "HHJJKK",
#         "newUserUsername": username
#     }
#     response = rs_razplus.post(
#         "https://accounts.learninga-z.com/accountsweb/marketing/trial.do",
#         data=payload)
#     if "An email has been sent" in response.text and mail_address in response.text:
#         print("Registed in RazPlus Successfully!")
#     else:
#         print("Registed in RazPlus failed!")
#         sys.exit()
#
#
# def check_email(q):
#     # Check Email
#     print("in check_email ...")
#     start_time = time.time()
#     while True:
#         r_mail = rs.get("https://tempail.com/en/").text
#         pq = pyquery.PyQuery(r_mail)
#         mail = pq('.mail ').attr('id')
#         print(mail)
#         if mail is not None:
#             msg = rs.get("https://tempail.com/en/" + mail).text
#             pq = pyquery.PyQuery(msg)
#             msg_url = pq('#iframe').attr('src')
#             msg_razplus = rs.get(msg_url).text
#             pq = pyquery.PyQuery(msg_razplus)
#             msg_razplus_url = pq('tbody tr td table tr td a').attr('href')
#             print(msg_razplus_url)
#             q.put(msg_razplus_url)
#             break
#         time.sleep(5)
#         stop_time = time.time()
#         if (stop_time - start_time) > 120:
#             print("Failed to get registered!")
#             break
#
#
# def set_account(q):
#     register_url = q.get()


if __name__ == "__main__":
    q = Queue()
    # t1 = Thread(target=get_email, args=(q,), name="get_email")
    # t2 = Thread(target=register_razplus, args=(q,), name="register_razplus")
    # t3 = Thread(target=check_email, args=(q,), name="check_email")
    # t4 = Thread(target=set_account, args=(q,), name="set_account")
    # t1.start()
    # t1.join()
    # t2.start()
    # t2.join()
    # t3.start()
    # t3.join()
    # t4.start()
    # t4.join()
    tempMail = TempEmail('https://tempail.com/en/', q)
    tempMail.get_email()
    razPlus = RazPlusFreeTrial(q,
                               "https://accounts.learninga-z.com/accountsweb/marketing/trial.do?campaign=trialbtnnxtologoRP",
                               "https://accounts.learninga-z.com/accountsweb/marketing/trial.do")
    razPlus.register()
    tempMail.check_mail()

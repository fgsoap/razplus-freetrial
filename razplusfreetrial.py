"""This is for razplus-trial"""
import random
import string
import sys
import time
from queue import Queue

import pyquery
import requests


class RazPlusFreeTrial:
    def __init__(self, queue, url, register_url):
        self.queue = queue
        self.url = url
        self.register_url = register_url

    def register(self):
        mail_address = self.queue.get()
        username = mail_address.split("@")[0]
        # rs = requests.Session()
        # rs.get(self.url)
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
        response = requests.post(self.register_url, data=payload)
        if "An email has been sent" in response.text and mail_address in response.text:
            print("Registered in RazPlus Successfully!")
        else:
            print("Registered in RazPlus failed!")
            sys.exit()


class TempEmail:
    def __init__(self, url, queue, rs):
        self.url = url
        self.queue = queue
        self.rs = rs

    def get_email(self):
        mail = self.rs.get(self.url).text
        pq = pyquery.PyQuery(mail)
        mail_address = pq('#eposta_adres').attr('value')
        self.queue.put(mail_address)

    def check_mail(self):
        start_time = time.time()
        while True:
            r_mail = self.rs.get(self.url).text
            pq = pyquery.PyQuery(r_mail)
            mail = pq('.mail ').attr('id')
            print(mail)
            if mail is not None:
                pq = pyquery.PyQuery(self.rs.get(self.url + mail).text)
                msg = self.rs.get(pq('#iframe').attr('src')).text
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


if __name__ == "__main__":
    q = Queue()
    r = requests.Session()
    tempMail = TempEmail('https://tempail.com/en/', q, r)
    tempMail.get_email()
    razPlus = RazPlusFreeTrial(q, "https://accounts.learninga-z.com/accountsweb/marketing/trial.do?campaign"
                                  "=trialbtnnxtologoRP",
                               "https://accounts.learninga-z.com/accountsweb/marketing/trial.do")
    razPlus.register()
    tempMail.check_mail()

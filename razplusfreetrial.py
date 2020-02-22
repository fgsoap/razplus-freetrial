"""This is for razplus-trial"""
import datetime
import random
import string
import sys
import time
from queue import Queue

import pyquery
import requests


class RazPlusFreeTrial:
    def __init__(self, queue, url):
        self.queue = queue
        self.url = url

    def get_registered(self):
        mail_address = self.queue.get()
        username = mail_address.split("@")[0]
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
        response = requests.post(self.url, data=payload)
        if "An email has been sent" in response.text and mail_address in response.text:
            print("Registered in RazPlus Successfully!")
        else:
            print("Registered in RazPlus failed!")
            sys.exit()

    def set_password(self):
        url = self.queue.get()
        pq = pyquery.PyQuery(requests.get(url).text)
        username = pq('#username').attr('value')
        password = ''.join(random.sample(string.ascii_letters, 8))
        action_url = pq('#f').attr('action')
        member_id = pq('#memberId').attr('value')
        email_certificate = pq('#emailCertificate').attr('value')
        url = 'https://accounts.learninga-z.com' + action_url
        payload = {
            "memberId": member_id,
            "emailCertificate": email_certificate,
            "password1": password,
            "password2": password,
        }
        requests.post(url, data=payload)
        data = {"username": username,
                "password": password,
                "expire time": datetime.datetime.now() + datetime.timedelta(days=14), }
        # https://requestbin.com/
        requests.post('https://enak80j25b8w.x.pipedream.net', data=data)


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
            mail = self.rs.get(self.url).text
            pq = pyquery.PyQuery(mail)
            mail = pq('.mail ').attr('id')
            if mail is not None:
                pq = pyquery.PyQuery(self.rs.get(self.url + mail).text)
                msg = self.rs.get(pq('#iframe').attr('src')).text
                pq = pyquery.PyQuery(msg)
                url = pq('tbody tr td table tr td a').attr('href')
                self.queue.put(url)
                break
            time.sleep(1)
            stop_time = time.time()
            if (stop_time - start_time) > 60:
                print("Failed to get registered!")
                break


if __name__ == "__main__":
    q = Queue()
    r = requests.Session()
    try:
        temp_mail_url = 'https://tempail.com/en/'
        tempMail = TempEmail(temp_mail_url, q, r)
        tempMail.get_email()
        register_url = 'https://accounts.learninga-z.com/accountsweb/marketing/trial.do?campaign=trialbtnnxtologoRP'
        razPlus = RazPlusFreeTrial(q, register_url)
        razPlus.get_registered()
        tempMail.check_mail()
        razPlus.set_password()
    except Exception as e:
        print('Error:', e)
    finally:
        print('Done!')

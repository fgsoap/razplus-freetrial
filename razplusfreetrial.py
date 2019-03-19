"""This is for razplus-trial"""
import random
import string
import requests
import pyquery

# get Email address from 10 Minutes Mail https://10minutemail.com

MAIL_URL = "https://10minutemail.com"
RS = requests.Session()
MAIL_FINAL_URL = RS.get(MAIL_URL).url
R_MAIL = RS.get(MAIL_FINAL_URL).text
PQ = pyquery.PyQuery(R_MAIL)
MAIL_ADDRESS = PQ('#mailAddress').attr("value")


#register in raz-plus
USERNAME = MAIL_ADDRESS.split("@")[0]
F_NAME = ''.join(random.sample(string.ascii_letters, 4))
L_NAME = ''.join(random.sample(string.ascii_letters, 4))


RS_RAZPLUS = requests.Session()
RS_RAZPLUS.get("https://accounts.learninga-z.com/accountsweb/marketing/trial.do?\
    campaign=trialbtnnxtologoRP")
HEADERS = {"Content-Type": "application/x-www-form-urlencoded",
           "Connection": "keep-alive",
           "Upgrade-Insecure-Requests": "1", "Host": "accounts.learninga-z.com",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,\
           image/webp,image/apng,*/*;q=0.8",
           "Origin": "https://accounts.learninga-z.com",
           "Referer": "https://accounts.learninga-z.com/accountsweb/marketing/trial.do?\
           campaign=trialbtnnxtologoRP"
          }
PAYLOAD = {"mdrQuery.stateId": 0, "mdrQuery.mdrType": "public",
           "international": "true",
           "mdrQuery.useMdr": "false", "campaignName": "trialbtnnxtologoRP",
           "org": "HHJJKK", "customerType": "new", "usageType": "classroom",
           "firstName": F_NAME, "lastName": L_NAME, "zip": 99999, "countryId": 98,
           "email": MAIL_ADDRESS, "occupation": 39, "mdrQuery.freeFormOrgName": "HHJJKK",
           "newUserUsername": USERNAME
          }
RS_RAZPLUS.post("https://accounts.learninga-z.com/accountsweb/marketing/trial.do",\
    data=PAYLOAD, headers=HEADERS)

# r_mail = rs.get(mail_final_url).text
# pq= pyquery.PyQuery(r_mail)
# mail_address = pq('#mailAddress').attr("value")
# print(mail_address)
# print(mail_final_url)

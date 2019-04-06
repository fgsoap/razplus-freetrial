"""This is for razplus-trial"""
import random
import string
import time
import requests
import pyquery

# Get Email address from TEMPAIL https://tempail.com/en/

MAIL_URL = "https://tempail.com/en/"
RS_TEMPAIL = requests.Session()
MAIL_FINAL_URL = RS_TEMPAIL.get(MAIL_URL).url
R_MAIL = RS_TEMPAIL.get(MAIL_FINAL_URL).text
PQ = pyquery.PyQuery(R_MAIL)
MAIL_ADDRESS = PQ('#eposta_adres').attr("value")

# Register in raz-plus

USERNAME = MAIL_ADDRESS.split("@")[0]
F_NAME = ''.join(random.sample(string.ascii_letters, 4))
L_NAME = ''.join(random.sample(string.ascii_letters, 4))

RS_RAZPLUS = requests.Session()
RS_RAZPLUS.get(
    "https://accounts.learninga-z.com/accountsweb/marketing/trial.do?campaign=trialbtnnxtologoRP"
)
HEADERS = {
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
PAYLOAD = {
    "mdrQuery.stateId": 0,
    "mdrQuery.mdrType": "public",
    "international": "true",
    "mdrQuery.useMdr": "false",
    "campaignName": "trialbtnnxtologoRP",
    "org": "HHJJKK",
    "customerType": "new",
    "usageType": "classroom",
    "firstName": F_NAME,
    "lastName": L_NAME,
    "zip": 99999,
    "countryId": 98,
    "email": MAIL_ADDRESS,
    "occupation": 39,
    "mdrQuery.freeFormOrgName": "HHJJKK",
    "newUserUsername": USERNAME
}
response = RS_RAZPLUS.post(
    "https://accounts.learninga-z.com/accountsweb/marketing/trial.do",
    data=PAYLOAD,
    headers=HEADERS)
if "An email has been sent" in response.text:
    print "Registed in RAZPLUS Successfully!"
else:
    print "Registed in RAZPLUS failed!"

time.sleep(120)

RR_MAIL = RS_TEMPAIL.get(MAIL_FINAL_URL).text
print RR_MAIL.text

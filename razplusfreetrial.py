#import libs
import threading
import random, string
import requests, pyquery
import time

#get Email address from 10 Minutes Mail https://10minutemail.com

mail_url = "https://10minutemail.com"
rs = requests.Session()
mail_final_url = rs.get(mail_url).url
r_mail = rs.get(mail_final_url).text 
pq= pyquery.PyQuery(r_mail)
mail_address = pq('#mailAddress').attr("value")
print(mail_address)
print(mail_final_url)

    
    
#register in raz-plus
username = mail_address.split("@")[0]
fname = ''.join(random.sample(string.ascii_letters, 4))
lname = ''.join(random.sample(string.ascii_letters, 4))
print(fname, lname)


rs_razplus = requests.Session()
rs_razplus.get("https://accounts.learninga-z.com/accountsweb/marketing/trial.do?campaign=trialbtnnxtologoRP")
headers = {"Content-Type": "application/x-www-form-urlencoded", "Connection": "keep-alive", \
          "Upgrade-Insecure-Requests": "1", "Host": "accounts.learninga-z.com", \
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", \
          "Origin": "https://accounts.learninga-z.com", \
          "Referer": "https://accounts.learninga-z.com/accountsweb/marketing/trial.do?campaign=trialbtnnxtologoRP"}
payload = {"mdrQuery.stateId": 0, "mdrQuery.mdrType": "public", "international": "true", \
           "mdrQuery.useMdr": "false", "campaignName": "trialbtnnxtologoRP", "org": "HHJJKK", \
           "customerType": "new", "usageType": "classroom", "firstName": fname, \
           "lastName": lname, "zip": 99999, "countryId": 98, "email": mail_address, \
           "occupation": 39, "mdrQuery.freeFormOrgName": "HHJJKK", "newUserUsername": username}
r_razplus = rs_razplus.post("https://accounts.learninga-z.com/accountsweb/marketing/trial.do", data=payload, headers=headers)
print(r_razplus.text)

# r_mail = rs.get(mail_final_url).text 
# pq= pyquery.PyQuery(r_mail)
# mail_address = pq('#mailAddress').attr("value")
# print(mail_address)
# print(mail_final_url)
import asyncio
from pyppeteer import launch

async def main():
    browser = await launch({'executablePath': '/usr/bin/chromium-browser'})
    page = await browser.newPage()
    await page.goto('https://10minutemail.com')
    print("10minutes")
#     print(page.querySelector('#mailAddress'))
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())


# from pyppeteer.launcher import launch

# #get Email address from 10 Minutes Mail https://10minutemail.com

# browser = await launch({'executablePath': '/usr/bin/chromium-browser'})

# mail_url = "https://10minutemail.com"

# page = await browser.newPage()
# await page.goto(mail_url)
# mailAddress = page.querySelector('#mailAddress')


# print(mailAddress)

# browser.close()
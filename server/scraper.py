from bs4 import BeautifulSoup
import re
import requests


def pull_privacy_policy(website):
    r = requests.get(website)
    soup = BeautifulSoup(r.content, 'html.parser')
    hrefs = soup.find_all('a', href=re.compile('.*/privacy.*'), string=re.compile('.*(P|p)rivacy.*'))
    policy_website = hrefs[0]

    address = re.search('href=\".*\"', policy_website)
    print (address)
    return hrefs[0]

# def get_policy_info(policy_link):
#

link = pull_privacy_policy('https://www.newyorktimes.com')

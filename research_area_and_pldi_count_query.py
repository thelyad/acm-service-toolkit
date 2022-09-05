"""
Given the name of the person and the acm profile url, this is an interactive script to find out:
1. What is the research area of this person according to ACM?
2. How many PLDI publications has this person published?
"""

from requests.models import parse_header_links
from bs4 import BeautifulSoup
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import re


STRINGS_FOR_TEST = ["Collaborative Writing"]
DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
PUB_SEARCH_URL = DBLP_BASE_URL + "search/author/api"


def get_url(pub_string=STRINGS_FOR_TEST):
    '''
    returns the BeautifulSoup object of a query to DBLP

    :param pub_string: A list of strings of keywords
    :return: BeautifulSoup: A BeautifulSoup Object
    '''
    resp = requests.get(PUB_SEARCH_URL, params={'q':pub_string, 'h': 1})
    root = ET.fromstring(resp.content)
    for url_attrib in root.iter('url'):
        url = url_attrib.text
        break
    return url

def find_num_of_pldi(url):
    count = 0
    print("url:", url)
    resp = requests.get("{}.xml".format(url))
    root = BeautifulSoup(resp.content)
    for r_attrib in root.findAll('r'):
        text = r_attrib.get_text()
        if 'PLDI' in text:
            count += 1
    print("actual count: ", count)
    if count >= 1 and count <=2:
        print("count: 1-2")
    elif count >= 3:
        print("count: 3+")

label_re = r'\"label\":\"([\w -]+)\"'
def find_research_area(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content)
    # print(soup.prettify())
    for h4_attrib_div in soup.find_all(class_='colored-block__title clearfix'):
            text = h4_attrib_div.get_text()
            if "subject area" in text.lower():
                # print(h4_attrib_div.next_sibling.get_text())
                for sibling in h4_attrib_div.next_siblings:
                        text = repr(sibling)
                        if text.startswith('<div'):
                            matches = re.finditer(label_re, text, re.MULTILINE)
                            matches_labels = [match.group(1) for _, match in enumerate(matches, start=1)]
                            print('research_area:', ','.join(matches_labels))
                            break

                        # print("h:", repr(sibling))


while(True):
    name = input('name: ').strip()
    acm_url = input('acm_url: ').strip()

    find_research_area(acm_url)
    find_num_of_pldi(get_url(name))




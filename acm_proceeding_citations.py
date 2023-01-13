"""
Given a ACM proceeding website (e.g. https://dl.acm.org/doi/proceedings/10.1145/2384616), scrape the title of the paper and its corresponding citation count. Return a ranked list from highest citation to lowest citation.

Pre-requisite: 
    - you need to expand all the collapsed columns to successfully scrape all the papers published in this proceeding. 
    - to obtain citation stats from Google Scholar, you need to have a Scraper_API. Store your own YOUR_SCRAPER_API_KEY as a system variable.

"""

import os
from bs4 import BeautifulSoup
from scholarly import scholarly, ProxyGenerator

pg = ProxyGenerator()
success = pg.ScraperAPI(os.getenv('YOUR_SCRAPER_API_KEY'))
scholarly.use_proxy(pg)

html_file = 'popl_proceeding_2013.html'

with open(html_file, 'r') as f:
    contents = f.read()


soup = BeautifulSoup(contents, 'lxml')
papers = soup.find_all("div", {"class": "issue-item-container"})

paper_acm_citation_pairs = []
paper_google_citation_pairs = []

for paper in papers:
    # get ACM citations
    title = paper.find_all("h5", {"class": "issue-item__title"})[0].find('a').contents[0]
    print("title:" , title)

    acm_citation = int(paper.find_all("span", {"class": "citation"})[0].text)
    print("acm citation:" , acm_citation)

    paper_acm_citation_pairs.append((title, acm_citation))

    # get Google Scholar citation
    search_res = scholarly.search_pubs(title)
    entry = next(search_res)
    if not entry['bib']['title'].lower() == title.lower():
        google_citation = -1
    else:
        google_citation = int(entry['num_citations'])
    print("google citation:" , google_citation)

    paper_google_citation_pairs.append((title, google_citation))

print("acm citation pairs:")
print(paper_acm_citation_pairs)
print(len(paper_acm_citation_pairs))

print("google citation pairs:")
print(paper_google_citation_pairs)
print(len(paper_google_citation_pairs))

# sort from highest to lowest
paper_acm_citation_pairs_sorted = sorted(paper_acm_citation_pairs, key=lambda x: x[1], reverse=True)
paper_google_citation_pairs_sorted = sorted(paper_google_citation_pairs, key=lambda x: x[1], reverse=True)

# final results
print("=========== Results ACM ===========")

for paper, citation in paper_acm_citation_pairs_sorted:
    print("{} : {}".format(paper, citation))

print("=========== Results Google Scholar ===========")

for paper, citation in paper_google_citation_pairs_sorted:
    print("{} : {}".format(paper, citation))
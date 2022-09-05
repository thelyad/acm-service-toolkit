"""
Given a ACM proceeding website (e.g. https://dl.acm.org/doi/proceedings/10.1145/2384616), scrape the title of the paper and its corresponding citation count. Return a ranked list from highest citation to lowest citation.

Pre-requisite: you need to expand all the collapsed columns to successfully scrape all the papers published in this proceeding. 

"""

from bs4 import BeautifulSoup

html_file = 'oopsla_proceeding_2012.html'

with open(html_file, 'r') as f:
    contents = f.read()


soup = BeautifulSoup(contents, 'lxml')
papers = soup.find_all("div", {"class": "issue-item-container"})

paper_citation_pairs = []

for paper in papers:
    # get citations
    title = paper.find_all("h5", {"class": "issue-item__title"})[0].find('a').contents[0]
    print("title:" , title)

    citation = int(paper.find_all("span", {"class": "citation"})[0].text)
    print("citation:" , citation)

    paper_citation_pairs.append((title, citation))


print(paper_citation_pairs)
print(len(paper_citation_pairs))

# sort from highest to lowest
paper_citation_pairs_sorted = sorted(paper_citation_pairs, key=lambda x: x[1], reverse=True)

# final results
print("=========== Results ===========")

for paper, citation in paper_citation_pairs_sorted:
    print("{} : {}".format(paper, citation))
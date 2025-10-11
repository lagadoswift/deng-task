import requests
from bs4 import *
from string import ascii_letters as letters
import re
from functools import reduce
import pandas as pd
import os

# Getting the content
url = "https://en.wikipedia.org/w/index.php?title=List_of_presidents_of_the_United_States&oldid=1312863317"

# the Wikimedia policy requires setting up a user agent
# https://wikitech.wikimedia.org/wiki/Robot_policy
# https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy
# https://phabricator.wikimedia.org/T400119

headers = {
    "User-Agent": "Beautiful Soup Scraper 30.09.2025 ; kirillovdm2002@gmail.com)"
}

response = requests.get(url, headers=headers)
content = response.content
soup = BeautifulSoup(content, "html.parser")
# print(soup.title)
# print(soup.title.get_text())
# print(soup.body)
# print(response.status_code)

table = soup.find_all("tr")

# print(soup)
# print(table)

# print(tables[2])

cont = BeautifulSoup(str(table[3]), "html.parser")

# Defining the functions

# for td:
# 0 - portrait - not needed for scraping
# 1 - Name and (birth-death)
# 2 - Term(s)
# 3 - Background colour - not needed for scraping
# 4 - Party
# 5 - Election
# 6 - Vice president

# The table has a very complex structure... it's hard to scrape


def iterate_table(table):
    lst = list()
    for it in table[1:48]:
        #        print(it)
        cont = BeautifulSoup(str(it), "html.parser")
        lst.append(get_values(cont))
    return lst


# a function to get terms (complex formatting makes it very hard to get in a straight way)
def get_terms(arg):
    words = reduce(lambda x, y: x + y, arg)
    # delete bad substrings
    words = re.sub(r"\[\w\]", "", string=words)
    words = re.sub(r"\n", "", string=words)
    return words


def get_values(cont):
    strings = list()
    tds = cont.find_all("td")

    for val in tds:
        print(list(val.strings))
        strings.append(list(val.strings))
    #        print(strings)
    dct = dict()

    bad_substrings = ("\n", "[", "]", *letters)
    dct["Name"] = strings[1][0]
    dct["Dates of birth and death"] = reduce(lambda x, y: x + y, strings[1][1])
    #    dct['Term'] = reduce(lambda x,y : x + y , strings[2][0:3])
    dct["Term"] = get_terms(strings[2])
    dct["Party"] = reduce(
        lambda x, y: x + " " + y, filter(lambda x: x not in bad_substrings, strings[4])
    )
    dct["Election"] = reduce(
        lambda x, y: x + " ; " + y, filter(lambda x: x != "\n", strings[5])
    )
    dct["Vice President"] = reduce(
        lambda x, y: x + "; " + y,
        filter(lambda x: not x in bad_substrings, strings[6]),
    )

    return dct


results = iterate_table(table)

print(results)

# "DATE OF BIRTH AND DEATH" FOR LIVING PEOPLE IS STILL SCRAPED INCORRECTLY DUE TO COMPLEXITIES WITH FORMATTING

df = pd.DataFrame(data=results)

print(df)


script_dir = str(os.path.dirname(__file__))
files_dir = script_dir + "\\data\\"

if not os.path.exists(files_dir):
    os.makedirs(files_dir)

# Saving to parquet doesn't work (allegedly due to bad scraping of birth-death)
df.to_csv(files_dir + "dataset.csv", index=False)

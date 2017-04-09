__author__ = 'Dongjie Fan'
# Input: Histroical Data (fetched before)
# Format: csv or else

from bs4 import BeautifulSoup
import urllib
import re
import pandas as pd
import os
import sys

if not len(sys.argv) == 5:
    print "Invalid number of arguments:"
    print "[Input File] [Output File] [Page Start] [Page End]"
    sys.exit()


# All Column Names:
def get_colnames():
	first = urllib.urlopen('http://wwe2.osc.state.ny.us/transparency/contracts/contractresults.cfm?PageNum_rsContract=1&sb=a&a=Z0000&ac=&v=%28Enter+Vendor+Name%29&vo=B&cn=&c=-1&m1=0&y1=0&m2=0&y2=0&am=0&b=Search&order=VENDOR_NAME&sort=ASC')
	soup = BeautifulSoup(first, "lxml")
	colnames = []
	th = soup.find_all('th')
	for name in th:
		colnames.append(name.find_all('a')[1].text)
	return colnames

def url(page_num):
    base1 = 'http://wwe2.osc.state.ny.us/transparency/contracts/contractresults.cfm?PageNum_rsContract='
    base2 = '&sb=a&a=Z0000&ac=&v=%28Enter+Vendor+Name%29&vo=B&cn=&c=-1&m1=0&y1=0&m2=0&y2=0&am=0&b=Search&order=VENDOR_NAME&sort=ASC' 
    return base1 + str(page_num) + base2

input_file = sys.argv[1]
output_file = sys.argv[2]
page_start = int(sys.argv[3])
page_end = int(sys.argv[4])
pages_range = range(page_start,page_end+1)

update = []
append = []
colnames = get_colnames()

# Load Historical Data And Make a copy
df = pd.read_csv(input_file, index_col=False)
test = df.copy()
id_exist = map(lambda x: str(x), test['Contract Number'].values)
test['hash'] = test.apply(lambda x: hash(tuple(x)), axis = 1)

for i in pages_range:
    page_url = url(i)
    page = urllib.urlopen(page_url)
    soup = BeautifulSoup(page, "lxml")
    rows = soup.find('table').find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        content = [ele.text.strip() for ele in cols]
        if not str(content[2]) in id_exist:
            append.append(content)
        else:
            target_id = str(content[2])
            old_hash = test[test['Contract Number'] == target_id]['hash'].values
            new_hash = hash(tuple(content)) 
            #hash function: hash value then for comparing two rows
            if old_hash != new_hash:
                update.append(content)

# append
df = df.append(pd.DataFrame(append, columns=colnames), ignore_index=True)
# update
df = df.append(pd.DataFrame(update, columns=colnames), ignore_index=True)
df = df.drop_duplicates(subset=['Contract Number'], keep='last') 
# reset index
df.reset_index(drop=True, inplace=True)
# output: overwrite
df.to_csv(output_file, index=False)

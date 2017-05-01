from bs4 import BeautifulSoup
import urllib, re, pandas as pd
import os
import sys
import time

t0 = time.time()

if not len(sys.argv) == 4:
    print "Invalid number of arguments:"
    print "[Output File] [Page Start] [Page End]"
    sys.exit()

output_file = sys.argv[1]
page_start = int(sys.argv[2])
page_end = int(sys.argv[3])
pages_range = range(page_start,page_end+1)# Choose the range of pages you want to parse; all -> range(1, 2614)


# first page
first = urllib.urlopen('http://wwe2.osc.state.ny.us/transparency/contracts/contractresults.cfm?PageNum_rsContract=1&sb=a&a=Z0000&ac=&v=%28Enter+Vendor+Name%29&vo=B&cn=&c=-1&m1=0&y1=0&m2=0&y2=0&am=0&b=Search&order=VENDOR_NAME&sort=ASC')
soup = BeautifulSoup(first, "lxml")

colnames = []
th = soup.find_all('th')
for name in th:
    colnames.append(name.find_all('a')[1].text)

# Order those records by different column. Remember to change their urls.
def url(page_num):
    base1 = 'http://wwe2.osc.state.ny.us/transparency/contracts/contractresults.cfm?PageNum_rsContract='
    base2 = '&sb=a&a=Z0000&ac=&v=%28Enter+Vendor+Name%29&vo=B&cn=&c=-1&m1=0&y1=0&m2=0&y2=0&am=0&b=Search&order=VENDOR_NAME&sort=ASC' 
    return base1 + str(page_num) + base2

df = pd.DataFrame(columns=colnames) 
for i in pages_range:
    page_url = url(i)
    page = urllib.urlopen(page_url)
    soup = BeautifulSoup(page, "lxml")
    page_data = []
    rows = soup.find('table').find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        page_data.append([ele for ele in cols if ele]) # why if TRUE?
    temp = pd.DataFrame(page_data, columns=colnames)
    df = df.append(temp, ignore_index=True)
   
df.to_csv(output_file, index=False)

t1 = time.time()
total = t1-t0
print "time diff: {}s".format(total)
#### Step 1: Fetch All Historical Data [[Link](http://wwe2.osc.state.ny.us/transparency/contracts/contractresults.cfm?PageNum_rsContract=1&sb=a&a=Z0000&ac=&v=%28Enter+Vendor+Name%29&vo=B&cn=&c=-1&m1=0&y1=0&m2=0&y2=0&am=0&b=Search&order=VENDOR_NAME&sort=ASC)]

- Two Solutions:
  - Use Our Paser (made by tools, like beautifulsoup)
  - Download all data from Link above (doesn't work for now, because the format is not **friendly**)



#### Step 2: Update & Append 

- *Update and Append.ipynb*
- cusp_hackathon.csv (for testing)
- *scrapy.py:*

```bash
# python scrapy.py [Input] [Output] [Page Start] [Page End]

# Input: historical data. (csv)
# Output: if same with Input, overwrite. (csv)
# Page Start: from 1.
# Page End: last page, 2613 for now.

# eg:
python scrapy.py ./cusp_hackathon.csv ./cusp_hackathon2.csv 1 3 
```
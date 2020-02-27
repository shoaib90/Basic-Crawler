#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import grequests
import pandas as pd
from bs4 import BeautifulSoup
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #To disable security warning
import warnings
warnings.simplefilter("ignore", category=UserWarning) #To suppress the warning.
import urllib.parse as urlparse
from urllib.parse import parse_qs

url_lst = []
lhandles = []
thandles = []
csv_input = pd.read_csv('output1.csv') #The csv file which consist the details of company that we have previously fetched.
url_lst = csv_input['url']

for url in url_lst:
    main_page = [grequests.get(url, verify=False)]
    response = grequests.map(main_page)
    for r in response:
        #print(r.request.url) #To know what response is coming first
        try:
            soup = BeautifulSoup(r.text, features="lxml")
            thandle = [a["href"] for a in soup.find_all("a", href=True) if ("twitter.com" in a["href"])] #Finding handles
            if thandle:                                     #For checking whether there is any data or not, otherwise it was skipping this in main list and moving onto next company.
                for elem in thandle:                         #cleaning unwanted data
                        parsed = urlparse.urlparse(elem)
                        try:
                            text = urlparse.parse_qs(parsed.query)['text']
                            if text:
                                continue
                        except KeyError:                 #As our desired result does not conatin text
                             thandles.append([elem])   
                             break
            else:
                thandles.append(thandle)
        except AttributeError:
            thandles.append(None)
        try:
            soup = BeautifulSoup(r.text, features="lxml")
            lhandle = [a["href"] for a in soup.find_all("a", href=True) if ("linkedin.com/compan" in a["href"])]  # Checking whether linkedin.com is present in the whole page.
            if lhandle:
                for c in lhandle:
                    lhandles.append([c])
                    print(lhandles)
                    break
            else:
                lhandles.append(lhandle)
        except AttributeError:
            lhandles.append(None)

        




        # print(thandles, lhandles)
        # sys.exit()


# In[ ]:


csv_input = pd.read_csv('output1.csv')
csv_input['Twitter'] = thandles
csv_input['LinkedIn'] = lhandles
csv_input.to_csv('output_final.csv', index=False)







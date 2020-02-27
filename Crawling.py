#!/usr/bin/env python
# coding: utf-8

# In[1]:


import grequests
import requests
from bs4 import BeautifulSoup
import csv
import pandas
import sys
import json
import warnings
warnings.simplefilter("ignore", category=UserWarning) # To suppress this: libuv only supports millisecond timer resolution; all times less will be set to 1 ms


# In[2]:


main_page_url = 'https://www.drupal.org/organizations/india'
base_url = 'https://www.drupal.org'


# In[3]:



main_page = requests.get(main_page_url)
soup = BeautifulSoup(main_page.text,'html.parser')

# Find main parent div of similar divs
all_references = soup.find('div', {'class': 'view-content'})

# Retriev child nodes array
child_divs = all_references.findChildren("div" , recursive=False)


# In[4]:


data = []
for reference in child_divs:
    sub_url = reference.h2.a.attrs.get('href')
    reference_page = [grequests.get(base_url+sub_url)]
    response = grequests.map(reference_page) 
    row = []
    for r in response:
        reference_soup = BeautifulSoup(r.text)
        row.append(reference_soup.find('h1', {'id': 'page-subtitle'}).text)
        company_url_reference = reference_soup.find('div', {'class':'intro'})
        row.append(company_url_reference.a.attrs.get('href'))
    #key = reference.h2.a.text
    contri = reference.find('div', {'class':'contributions'}) #Finding divs that contains our information about organization.
    contris = contri.findAll('div')
    i = 0
    for cont in contris:
        if 'people on' in cont.text or 'person on' in cont.text and i == 0:
            row.append(cont.text)
        elif 'projects supported' in cont.text and i == 1:
            row.append(cont.text)
        elif 'issue credits' in cont.text and i == 2:
            row.append(cont.text)
        elif 'case studies' in cont.text and i == 3:
            row.append(cont.text)
        else:
            row.append(None)
        i += 1
    data.append(row)


# In[5]:


# data = {}
# Getting parent div of all the list-items
lst_item_parent = soup.find('div', {'class':'item-list'})

#Getting all the content of class pager-item
lst_item_parent_pager = lst_item_parent.findChildren('li',{'class':'pager-item'})
for count in lst_item_parent_pager:
    pages_url = count.a.get('href')
    #print(pages_url)
    #continue
    next_page = base_url + pages_url 
    main_page = [grequests.get(next_page)]
    responses = grequests.map(main_page)
    for r in responses:
        soup = BeautifulSoup(r.text)
        # Find parent div of similar divs
        all_references = soup.find('div', {'class': 'view-content'})
        # Retriev child nodes array
        child_divs = all_references.findChildren("div" , recursive=False)
        for reference in child_divs:
            sub_url = reference.h2.a.attrs.get('href')
            reference_page = [grequests.get(base_url+sub_url)]
            response = grequests.map(reference_page) 
            for r in response:
                reference_soup = BeautifulSoup(r.text)
                row.append(reference_soup.find('h1', {'id': 'page-subtitle'}).text)
                company_url_reference = reference_soup.find('div', {'class':'intro'})
                row.append(company_url_reference.a.attrs.get('href'))
            #key = reference.h2.a.text
            contri = reference.find('div', {'class':'contributions'})
            contris = contri.findAll('div')
            i = 0
            for cont in contris:
                if 'people on' in cont.text or 'person on' in cont.text  and i == 0:
                    row.append(cont.text)
                elif 'projects supported' in cont.text and i == 1:
                    row.append(cont.text)
                elif 'issue credits' in cont.text and i == 2:
                    row.append(cont.text)
                elif 'case studies' in cont.text and i == 3:
                    row.append(cont.text)
                else:
                    row.append(None)
                i += 1
            data.append(row)

    #for writing data            
# import io    #So that unicode error will be eradicated
# #print(data)
# with io.open('output_final.csv','w',encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(['name', 'url', 'people', 'projects', 'issue credited', 'cases studies'])
#     writer.writerows(data)


# In[ ]:


#For Database
import mysql.connector as mysql

## connecting to the database using 'connect()' method
## it takes 3 required parameters 'host', 'user', 'passwd'
db = mysql.connect(
    host = "localhost",
    user = "Shoaib",
    passwd = "pass@123",
    database = "crawler",
    auth_plugin = 'mysql_native_password'
)

## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS info")
cursor.execute("CREATE TABLE Information (name VARCHAR(255), url VARCHAR(255), people VARCHAR(255), projects VARCHAR(255), issues_credited VARCHAR(255), case_studies VARCHAR(255),Twitter VARCHAR(255), LinkedIn VARCHAR(255))  ")
cursor.execute("ALTER TABLE information ADD COLUMN id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")
cursor.execute("DESC Information")
print(cursor.fetchall())


# In[7]:


## defining the query
import mysql.connector as mysql
import sys

## connecting to the database using 'connect()' method
## it takes 3 required parameters 'host', 'user', 'passwd'
db = mysql.connect(
    host = "localhost",
    user = "Shoaib",
    passwd = "pass@123",
    database = "ccrawler",
    auth_plugin = 'mysql_native_password'
)

## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS information")
cursor.execute("CREATE TABLE Information (name VARCHAR(255), url VARCHAR(255), people VARCHAR(255), projects VARCHAR(255), issues_credited VARCHAR(255), case_studies VARCHAR(255),Twitter VARCHAR(255), LinkedIn VARCHAR(255))  ")
cursor.execute("ALTER TABLE information ADD COLUMN id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")
csv_data = csv.reader(open('output_final.csv'))
for row in csv_data:
    cursor.execute('INSERT INTO information(name, url, people, projects, issues_credited,case_studies, Twitter, LinkedIn )' 
          'VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")', row)
    print(cursor.rowcount, "records inserted")

## to make final output we have to run the 'commit()' method of the database object
db.commit()
cursor.close()
db.close()







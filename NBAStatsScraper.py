# import libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests as re
from tqdm import tqdm

years = ['1983', '1993', '2003', '2013', '2023']
# initialize vectors
nameresults = []
ageresults = []
hrefresults = []

for year in years:
    # set webdriver and open page
    site = re.get('https://www.basketball-reference.com/leagues/NBA_' + year + '_totals.html').content

    # store page source and parse 
    soup = BeautifulSoup(site, 'html.parser')

    # pull data from basketballreference.com
    for a in soup.findAll(attrs = 'full_table'):
        name = a.find('td')
        nameresults.append(name.text)

    for b in soup.findAll(attrs = 'full_table'):
        age = b.find('td',{'data-stat':'age'})
        ageresults.append(age.text)

    for k in soup.findAll(attrs = 'full_table'):
        href = k.find('td',{'data-stat':'player'})
        href2 = href.findAll('a')
        href3 = str(href2).split('"')[1]
        hrefresults.append(href3)

    # create data frame and convert to comma separated values     
df = pd.DataFrame({'Names': nameresults, 'Age': ageresults, 'Href':hrefresults})
df.to_csv('NBAStats.csv', index=False, encoding='utf-8')
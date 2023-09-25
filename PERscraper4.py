import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm

df =  pd.read_csv('C:/Users/Caleb/OneDrive/Desktop/OneDrive/Projects/NBA Draft Outcome Predictor/NBAStats.csv')[1574:]

nameresults = df['Name']
PERresults = []

for player in tqdm(range(0, len(df))):
    try:    
        # set webdriver and open page
        service = Service('C:/Users/Caleb/OneDrive/Documents/chromedriver/chromedriver.exe')
        driver = webdriver.Chrome(service=service) #flip slashes for Python
        driver.get('https://www.basketball-reference.com' + df.iloc[player,].Href + '#all_advanced-playoffs_advanced')

        # store page source and parse 
        content = driver.page_source
        soup = BeautifulSoup(content,features="html.parser")

        # pull data from basketballreference.com
        try:
            table = soup.find('table', id='advanced')
            tfoot = table.find('tfoot')
            
            PER = tfoot.find('td', {'data-stat':'per'}).get_text()
            PERresults.append(PER)

        except:
            PERresults.append('DNP')
            
        # close web page
        driver.quit()
    except:
        PERresults.append('CRASH')
        
# create data frame and convert to comma separated values     
df = pd.DataFrame({'Names': nameresults, 'PER': PERresults})
df.to_csv('PER4.csv', index=False, encoding='utf-8')
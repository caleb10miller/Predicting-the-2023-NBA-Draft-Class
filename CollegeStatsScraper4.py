import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm

df =  pd.read_csv('/Users/calebmiller/Library/CloudStorage/OneDrive-Personal/Projects/NBA Draft Outcome Predictor/NBAStats.csv')[1574:]

nameresults = df['Names'] 
pointresults = [] 
gresults = []
minutesresults = []
offreboundsresults = []
reboundsresults = [] 
assistresults = []
stealsresults = []
blocksresults = []
fgmresults = []
fgaresults = [] 
ftaresults = []
fgpresults = []
threemaderesults = []
threeattemptresults = []
threepercentresults = [] 
freethrowmaderesults = []
freethrowpercentresults = []

for player in tqdm(range(0, len(df))): 
    # set webdriver and open page
    service = Service('/Users/calebmiller/Library/CloudStorage/OneDrive-Personal/Projects/NBA Draft Outcome Predictor/chromedriver-mac-arm64/chromedriver')
    driver = webdriver.Chrome(service=service) #flip slashes for Python
    driver.get('https://www.basketball-reference.com' + df.iloc[player,].Href + '#all_all_college_stats')

    try:

        # store page source and parse 
        content = driver.page_source
        soup = BeautifulSoup(content,features="html.parser")

        # pull data from basketballreference.com

        table = soup.find('table', id='all_college_stats')
        tbody = table.find('tbody')
        trow = tbody('tr')[0]
        
        g = trow.find('td', {'data-stat':'g'}).get_text()
        gresults.append(g)

        minutes = trow.find('td', {'data-stat':'mp'}).get_text()
        minutesresults.append(minutes)

        points = trow.find('td', {'data-stat':'pts'}).get_text()
        pointresults.append(points)

        offrebounds = trow.find('td', {'data-stat':'orb'}).get_text()
        offreboundsresults.append(offrebounds)       
        
        rebounds = trow.find('td', {'data-stat':'trb'}).get_text()
        reboundsresults.append(rebounds)

        assists = trow.find('td', {'data-stat':'ast'}).get_text()
        assistresults.append(assists)

        steals = trow.find('td', {'data-stat':'stl'}).get_text()
        stealsresults.append(steals)

        blocks = trow.find('td', {'data-stat':'blk'}).get_text()
        blocksresults.append(blocks)

        fgm = trow.find('td', {'data-stat':'fg'}).get_text()
        fgmresults.append(fgm)

        fga = trow.find('td', {'data-stat':'fga'}).get_text()
        fgaresults.append(fga)

        fgp = trow.find('td', {'data-stat':'fg_pct'}).get_text()
        fgpresults.append(fgp)

        tpm = trow.find('td', {'data-stat':'fg3'}).get_text()
        threemaderesults.append(tpm)

        tpa = trow.find('td', {'data-stat':'fg3a'}).get_text()
        threeattemptresults.append(tpa)

        tpp = trow.find('td', {'data-stat':'fg3_pct'}).get_text()
        threepercentresults.append(tpp)

        ftm = trow.find('td', {'data-stat':'ft'}).get_text()
        freethrowmaderesults.append(ftm)

        fta = trow.find('td', {'data-stat':'fta'}).get_text()
        ftaresults.append(fta)

        ftp = trow.find('td', {'data-stat':'ft_pct'}).get_text()
        freethrowpercentresults.append(ftp)

    # in case a player didn't play in college
    
    except:
        gresults.append('DNP')
        pointresults.append('DNP')
        minutesresults.append('DNP')
        offreboundsresults.append('DNP')       
        reboundsresults.append('DNP')
        assistresults.append('DNP')
        stealsresults.append('DNP')
        blocksresults.append('DNP')
        fgmresults.append('DNP')
        fgaresults.append('DNP')
        fgpresults.append('DNP')
        threemaderesults.append('DNP')
        threeattemptresults.append('DNP')
        threepercentresults.append('DNP')
        ftaresults.append('DNP')
        freethrowmaderesults.append('DNP')
        freethrowpercentresults.append('DNP')

    # close web page
    driver.quit()

# create data frame and convert to comma separated values     
df = pd.DataFrame({'Names': nameresults, 'Games': gresults, 'Minutes': minutesresults, 'Points': pointresults, 'OffRebounds':offreboundsresults, 'Rebounds': reboundsresults, 'Assists': assistresults, 'Steals': stealsresults, 'Blocks': blocksresults, 'Fgm': fgmresults, 'Fga': fgaresults, 'Fta': ftaresults, 'Fg%':fgpresults, '3pm':threemaderesults, '3pa':threeattemptresults, '3p%':threepercentresults, 'Ftm':freethrowmaderesults, 'Ft%':freethrowpercentresults})
df.to_csv('CollegeStats4.csv', index=False, encoding='utf-8')
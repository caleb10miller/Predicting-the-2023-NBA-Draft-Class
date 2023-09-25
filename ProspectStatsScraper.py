import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = 'https://basketball.realgm.com/nba/draft/prospects/stats/Totals/All/'

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table element that contains the data
table = soup.find('table', {'class': 'tablesaw'})

# Find the table header row and extract the column names
header_row = table.find('thead').find('tr')
column_names = [th.text.strip() for th in header_row.find_all('th')]

# Find all table rows (excluding the header row) and extract the data
rows = table.find('tbody').find_all('tr')
data = []
for row in rows:
    row_data = [td.text.strip() for td in row.find_all('td')]
    data.append(row_data)

data = pd.DataFrame(data, columns=column_names)
data.to_csv('ProspectStats.csv', index=False, encoding='utf-8')
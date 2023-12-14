from selenium import webdriver
from bs4 import BeautifulSoup
import openpyxl
import pandas as pd
import time

driver = webdriver.Chrome()

data = []
website = {'seek': 'https://www.seek.com.au/jobs?page=', 
           'indeed': 'https://au.indeed.com/',
           'bbs': 'https://brisbanebbs.com/forum.php?mod=forumdisplay&fid=14&page=',
           }
key_words = {'software', 'develop', 'data', 'machine', 'learning', 'artificial', 'intelligence'}
# Parse pages
for i in range(1, 10):
    url = "https://brisbanebbs.com/forum.php?mod=forumdisplay&fid=14&page=" + str(i)
    driver.get(url)

    # Wait to load the webpage
    time.sleep(2)

    pagesource = driver.page_source
    soup = BeautifulSoup(pagesource, 'html.parser')
    # Find all button containing work opportunity
    result = soup.find_all('a', class_='s xst')

    # Iterate through buttons
    for re in result:
        if re.text.strip() == '已關閉':
            pass
        else:
            opportunity = re.text.strip()
            numberOfOpportunity = opportunity.split('(')[1].split(')')[0]
            # Show 999+ at most
            if len(numberOfOpportunity) >= 4:
                numberOfOpportunity = '999'
            companyName = re.get('title')[0:-5]
            data.append((companyName, int(numberOfOpportunity)))

    print('Finish parsing page ' + str(i))

df_temp = pd.DataFrame(data, columns=['公司名稱', '工作機會'])
df_temp.to_excel('上市櫃公司工作機會.xlsx')

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 15:54:21 2021

@author: romul
"""
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
#from selenium.webdriver.common.keys import Keys
#from selenium.common.exceptions import NoSuchElementException
#from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import json

url = 'https://www.nba.com/stats/players/traditional/?sort=PLAYER_NAME&dir=1&Season=2020-21&SeasonType=Regular%20Season'

top10ranking = {}

rankings = {
  '3points':{'field':'FG3M','label':'3PM'},
  'points':{'field':'PTS','label':'PTS'},
  'assists':{'field':'AST','label':'AST'},
  'rebounds':{'field':'REB','label':'REB'},
  'steels':{'field':'STL','label':'STL'},
  'blocks':{'field':'BLK','label':'BLK'}, 
}

def buildrank(type):
  
  field = rankings[type]['field']
  label = rankings[type]['label']
  
  
  driver.find_element_by_xpath(f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()
  
  element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
  html_content = element.get_attribute('outerHTML')
  
  soup = BeautifulSoup(html_content, 'html.parser')
  table = soup.find(name='table')
  
  df_full = pd.read_html(str(table))[0].head(10)
  df = df_full[['Unnamed: 0', 'PLAYER','TEAM', label ]]
  df.colums = ['pos', 'plyer', 'team', 'pontos']
  return df.to_dict('records')
  

options = Options()
#options.headless = True
driver = webdriver.Firefox(options=options)


#options = EdgeOptions()
#options.use_chromium = True
#options.headless = True
#driver = Edge(options=options)

driver.get(url)
driver.implicitly_wait(15)

driver.find_element_by_xpath("//div[@class='banner-actions-container']//button[@id='onetrust-accept-btn-handler']").click()

for k in rankings:
  top10ranking[k] = buildrank(k)

driver.quit()

js = json.dumps(top10ranking)
fp = open('ranking.json', 'w')
fp.write(js)
fp.close()
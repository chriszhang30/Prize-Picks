# install selenium
pip install selenium

# import selenium packages
from selenium import webdriver
from selenium.webdriver.common.by import By

import time

# read this: https://pypi.org/project/undetected-chromedriver/
# need this so prizepicks doesn't know ur a bot; need the chromedriver file in the same folder as wherever you're running this (i used a jupyter notebook)
pip install undetected-chromedriver


# set up chromedriver
import undetected_chromedriver as uc
import pandas as pd

options = uc.ChromeOptions()
options.headless = False

# this will open up a new Chrome browser window where the scraping will be done
driver = uc.Chrome(options=options,version_main=119)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Scraping PrizePicks -- you will probably have to manually click allow location for this to get to next step
driver.get("https://app.prizepicks.com/")
time.sleep(3)

# Waiting and closes popup
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "close")))
time.sleep(3)
driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/div/div[3]/button").click()
# /html/body/div[3]/div[3]/div/div/div[1]
time.sleep(3)

# Creating tables for players
ppPlayers = []

# CHANGE NBA TO ANY SPORT THAT YOU LIKE!!!!! IF THE SPORT IS NOT OFFERED ON PP THEN THE PROGRAM WILL RUN AN ERROR AND EXIT.
driver.find_element(By.XPATH, "//div[@class='name'][normalize-space()='NBA']").click()
time.sleep(5)

# Waits until stat container element is viewable
stat_container = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))


# Finding all the stat elements within the stat-container
categories = driver.find_element(By.CSS_SELECTOR, ".stat-container").text.split('\n')

# Collecting categories
for category in categories:
    driver.find_element(By.XPATH, f"//div[text()='{category}']").click()

    projectionsPP = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection")))

    for projections in projectionsPP:
        names = projections.find_element(By.CLASS_NAME, "name").text
        positions = projections.find_element(By.CLASS_NAME, "team-position").text
        opps = projections.find_element(By.CLASS_NAME, "opponent").text
        value = projections.find_element(By.CLASS_NAME, "presale-score").get_attribute('innerHTML')
        proptype = projections.find_element(By.CLASS_NAME, "text").get_attribute('innerHTML')

        players = {
            'Name': names,
            'Position': positions,
            'Opponent': opps,
            'Value': value,
            'Prop': proptype.replace("<wbr>", "")
        }
        ppPlayers.append(players)
        
    time.sleep(3)

dfProps = pd.DataFrame(ppPlayers)

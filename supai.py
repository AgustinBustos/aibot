from __future__ import annotations
import time, random, os, csv, platform
import logging
import selenium
from bs4 import BeautifulSoup
import pandas as pd
import pyautogui
import undetected_chromedriver as uc
from urllib.request import urlopen
import re
from datetime import datetime, timedelta
from reducehtml import html_remover
import openai
from openai_functions import get_job_links
import pandas as pd
import datetime

name_of_class_for_scroll_down=".jobs-search-results-list"
user_data_dir=r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
profile_directory='Default'

# url="https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords="+position+location+"&start="+str(jobs_per_page)
url=r"https://www.linkedin.com/jobs/search/?distance=25&f_AL=true&f_TPR=r86400&geoId=100446943&keywords=Cient%C3%ADfico%20de%20datos&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"
next_page_button_selector=r"button[aria-label='Page "

done_in=datetime.datetime.now()
def open_browser(user_data_dir,profile_directory,url):
# log = logging.getLogger(__name__)
# driver = webdriver.Chrome(ChromeDriverManager().install())
    options = uc.ChromeOptions()
    options.add_argument('--user-data-dir='+user_data_dir) 
    options.add_argument(r'--profile-directory='+profile_directory) #e.g. Profile 3
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")

    # Disable webdriver flags or you will be easily detectable
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver=uc.Chrome(options=options)
    driver.get(url)
    return driver
# driver = webdriver.Chrome(ChromeDriverManager().install())

def setupLogger() -> None:
    dt: str = datetime.strftime(datetime.now(), "%m_%d_%y %H_%M_%S ")

    if not os.path.isdir('./logs'):
        os.mkdir('./logs')

    # TODO need to check if there is a log dir available or not
    logging.basicConfig(filename=('./logs/' + str(dt) + 'applyJobs.log'), filemode='w',
                        format='%(asctime)s::%(name)s::%(levelname)s::%(message)s', datefmt='./logs/%d-%b-%y %H:%M:%S')
    log.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)
    c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
    c_handler.setFormatter(c_format)
    log.addHandler(c_handler)
def avoid_lock() -> None:
        x, _ = pyautogui.position()
        pyautogui.moveTo(x + 200, pyautogui.position().y, duration=1.0)
        pyautogui.moveTo(x, pyautogui.position().y, duration=0.5)
        time.sleep(2)
        pyautogui.keyDown('ctrl')
        time.sleep(2)
        pyautogui.press('esc')
        time.sleep(2)
        pyautogui.keyUp('ctrl')
        time.sleep(2)
        pyautogui.press('esc')
def load_page(driver, sleep=1):
        scroll_page = 0
        while scroll_page < 4000:
            driver.execute_script("window.scrollTo(0," + str(scroll_page) + " );")
            scroll_page += 200
            time.sleep(sleep)
def fill_data(driver) -> None:
    driver.set_window_size(1, 1)
    driver.set_window_position(2000, 2000)
    driver.maximize_window()
def scroll_down(selected_to_scroll_from,driver):
    scroll_origin = selenium.webdriver.common.actions.wheel_input.ScrollOrigin.from_element(selected_to_scroll_from)    
    for i in range(30):
        selenium.webdriver.common.action_chains.ActionChains(driver)\
            .scroll_from_origin(scroll_origin, 0, 200)\
            .perform()
        time.sleep(1)
     
if __name__ == '__main__':
    
    driver=open_browser(user_data_dir,profile_directory,url)

    all_links=[]
    for page_number in range(4):
        #startup 
        avoid_lock()
        fill_data(driver)

        #scroll down
        selected_html=driver.find_element(selenium.webdriver.common.by.By.CSS_SELECTOR, name_of_class_for_scroll_down)
        scroll_down(selected_html,driver)

        # simplify html
        html = driver.page_source
        # html=driver.find_element(selenium.webdriver.common.by.By.CSS_SELECTOR, name_of_class_for_scroll_down).get_attribute('outerHTML')
        
        simplified_html=html_remover(html)
        # with open("example.html", "w",encoding="utf-8") as file:
        #     file.write(simplified_html)
        
        # time.sleep(10000)
        
        #save data
        found_jobs=get_job_links(simplified_html)
        to_add=[]
        for i in found_jobs:
            try:
                to_add.append(driver.find_element(selenium.webdriver.common.by.By.CSS_SELECTOR, f"a[href*='{i}']").get_attribute('href'))
            except:
                to_add.append(i)
        all_links=all_links+to_add
        to_export=pd.DataFrame([i.dict() for i in all_links])
        to_export['time']=done_in
        to_export.to_csv("links_to_use_later.csv") 

        #next page
        driver.find_element(selenium.webdriver.common.by.By.CSS_SELECTOR, f"{next_page_button_selector}{page_number+2}']").click()
        time.sleep(2)
    # print(all_links)
    to_export=pd.DataFrame([i.dict() for i in all_links])
    to_export['time']=done_in
    to_export.to_csv("links_to_use_later.csv")



    
        
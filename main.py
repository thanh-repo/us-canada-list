# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:03:56 2022

@author: ThanhOffice
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json

urls = {"US": "https://www.britannica.com/topic/list-of-cities-and-towns-in-the-United-States-2023068",
        "Canada": "https://www.britannica.com/topic/list-of-cities-and-towns-in-Canada-2038873"}

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
driver.set_window_position(-10000, 0)
dict_result = {}
for key, item in urls.items():
    driver.get(item)
    ref_list = []
    for i in range(2, 1000):
        x_cities = f'//*[@id="content"]/div/div[1]/article/div/div[1]/div/div/div[2]/div[2]/div[1]/ul/li[{i}]'
        try:
            ref = driver.find_element(By.XPATH, x_cities)
            ref_list.append(ref.get_attribute('data-target').replace('#', ''))
        except:
            break
    city_dict = {}
    for ref in ref_list:
        x_city = f'//*[@id="{ref}"]/h2/a'
        f_city = driver.find_element(By.XPATH, x_city)
        print(f_city.get_attribute("textContent"))
        towns = []
        for i in range(1, 1000):
            x_town = f'//*[@id="{ref}"]/ul/li[{i}]/div/a'
            try:
                f_town = driver.find_element(By.XPATH, x_town)
                towns.append(f_town.get_attribute("textContent"))
            except:
                break
        
        city_dict[f_city.get_attribute("textContent")] = towns
    dict_result[key] = city_dict
    
with open('result.json', 'w') as fp:
    json.dump(dict_result, fp)

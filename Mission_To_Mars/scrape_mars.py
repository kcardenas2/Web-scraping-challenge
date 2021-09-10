#Dependencies
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import pymongo
import requests
from flask import Flask, render_template, redirect
from webdriver_manager.chrome import ChromeDriverManager
from flask_pymongo import PyMongo

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless =False)
    dict={}

    url="https://redplanetscience.com/"
    browser.visit(url)
    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')
#Getting the lastest news title
    news_title=soup.find(class_='content_title').text
#getting the paragraph for title
    news_p=soup.find(class_='article_teaser_body').text
    featured_image_url= "https://spaceimages-mars.com/"
    browser.visit(featured_image_url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')
    path= soup.find('img', class_= "fancybox-image")['src']
    featured_image_url = featured_image_url + path
#MArs Table
    Mars_url= "https://galaxyfacts-mars.com/"
    browser.visit(Mars_url)
    mars_df =pd.read_html(Mars_url)
    mars_df = mars_df[0]
    mars_df.columns = mars_df.iloc[0]
    mars_df = mars_df.iloc[1:]
    mars_df
# Mars Hemisphere
    Mars_hemoshpere_url="https://marshemispheres.com/"
    browser.visit(Mars_hemoshpere_url)
    hemisphere_list =[]
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_ ='item')
    for hemisphere in results:
        browser.links.find_by_partial_text(hemisphere.h3.text).click()
        html= browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image_title = soup.h2.text
        image_url= Mars_hemoshpere_url + soup.find('img', class_="wide-image")['src']
        browser.visit(Mars_hemoshpere_url)
        dict = {'title': image_title, 'image_url': image_url}
        hemisphere_list.append(dict)

    dict['news_title']=news_title
    dict['news_p']= news_p
    dict['featured_image_url']= featured_image_url
    dict['mars_df']=mars_df
    dict['Mars_hemoshpere_url']=hemisphere_list

    # Close bRowser
    browser.quit()


    return dict

print(scrape())
#!/usr/bin/python
#!/usr/bin/python3
#!/usr/bin/env python
#!/usr/bin/env python3

# -*- coding: utf8 -*-
# aws gathering data   :- [Name, Price, Asin, Category, Link]
# date                 :- 30/03/2019
# author               :- Md Jabed Ali(jabed)

#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import Select
from time import gmtime, strftime
import time
import re
import os
import requests
from bs4 import BeautifulSoup
import csv
import itertools
from urllib.request import urlopen
from itertools import groupby
import multiprocessing
from fake_useragent import UserAgent
#from captcha-tst import *

#https://www.amazon.in/s/ref=sr_pg_2/259-2923346-9701236?me=A368CFGDO8H247&fst=as%3Aoff&rh=p_4%3A%%21iT+Jeans&page=1
#https://www.amazon.in/s/ref=sr_in_1_p_4_0?me=A368CFGDO8H247&fst=as%3Aoff&rh=p_4%3A%21iT+Jeans&ie=UTF8&qid=1553146952 
#pip install fake-useragent

# ip   : 144.202.82.63 , 144.202.57.92
# pass : Tx)181vhaB@q%BBW , +1YkNHPHd5y6a]_L

# http://webservices.amazon.com/onca/xml?Service=AWSECommerceService&AWSAccessKeyId=[]&AssociateTag=[]&Operation=ItemSearch&Keywords=[]&SearchIndex=[]&Timestamp=[]&Signature=[] ----- api url
# https://www.amazon.in/gp/search/other/ref=sr_in_1_-2?me=A368CFGDO8H247&rh=i%3Amerchant-items&pickerToList=brandtextbin&indexField=%23&ie=UTF8&qid=1552922225 ----- test url

ua = UserAgent()
headers = {'User-Agent': ua.random,
           #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
           #':authority': 'www.amazon.in',
           #':scheme': 'https',
           'X-Requested-With': 'XMLHttpRequest',
           'Upgrade-Insecure-Requests': '1',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Origin': 'https://www.amazon.in',
           #'Host': 'www.amazon.in',
           #'Authorization': 'Bearer ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKaGRYUm9YM1J2YTJWdUlqb2lNMkpoTnpGak9EaG1NMkl5T0RJMVpEQmlObU15WlRKaVltUmpPRGxsTkRjaUxDSmxlSEFpT2pFMU16azVOamt6TnpFc0ltbGhkQ0k2TVRVek56TTNOek0zTVN3aWFYTnpJam9pYW5WdVoyeGxjMk52ZFhSZllYQnBYMlY0ZEdWdWMybHZiaUlzSW1GMVpDSTZJbU5zYVdWdWRDSjkuajREcnY2TVJiLWdRTmk2ZzF5cjJHZTZaRFJLTi1hdnhwRTVxZkRyNVdWZw==',
           #'Referer': 'https://www.amazon.in/gp/search/other/ref=sr_sa_p_4?me=A368CFGDO8H247&rh=i%3Amerchant-items&pickerToList=brandtextbin&ie=UTF8&qid=1552571726'
           #'Cookie': 'ASPSESSIONIDQWBBDTCD=DNCKHHMBMEBFIHNPCJKDCKJB'
           #'Cookie' : 'csm-hit=tb:ZQ6S0DGY3NA6K1VAEG63+s-PEF8HXB6MZ9J6K652T10|1552582601349&t:1552582601349&adb:adblk_no'

}

headers3 = {'Host': 'www.amazon.in',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            #'Referer': 'https://www.amazon.in/gp/search/other/ref=sr_in_m_L?me=A368CFGDO8H247&rh=i%3Amerchant-items&pickerToList=brandtextbin&indexField=m&ie=UTF8&qid=1552586898',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': ''
}

#Remove duplicate from list
def my_function(x):
  return list(dict.fromkeys(x))

readsfile = open('brand-link.txt', errors='ignore')
line = readsfile.readlines()
lines = [i.strip(' \t\n\r') for i in line]

#outputFile = open('a.csv','a', newline='', encoding="utf8")
#outputWriter = csv.writer(outputFile) 

searches = ['%23','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
final = []
count = 0

#[for different page layout.
#a-last
#a-spacing-none
#div.s-item-container
#li.a-link-normal
#s-include-content-margin s-border-bottom]
#keywords = ['a-last']

for ix, tit in enumerate(itertools.islice(lines,0,None)):
#for ix,tit in enumerate(lines):
    count1 = count + ix + 1
    print (str(count1) + " Collect information. - " + time.strftime("%a %b %d %I:%M:%S %p %Y"))
    #os.system("taskkill /im chromedriver.exe")
    #os.system("taskkill /im chrome.exe")
    try:
        res = requests.get(tit, headers=headers)
    except:
        res = 'n/a'
    #soup = BeautifulSoup(res.text, 'html.parser')
    #browser = webdriver.Chrome()
    #browser.maximize_window()
    #browser.get(tit)
    #time.sleep()
    src = str(res.text).replace('amp;', '').replace('href="', '').replace('https://www.amazon.in/', '')     #for different layout
    soup = BeautifulSoup(src, 'html.parser')
    if 's-include-content-margin s-border-bottom' in soup:
        results0 = soup.find_all('div', {'class' : 's-include-content-margin s-border-bottom'})
        link = str(str(re.findall('class="a-link-normal"(.*?)>', str(src), re.DOTALL)) +  str(re.findall('data-asin="(.*?)"', str(src), re.DOTALL))).replace('\',', '~')
        name = str(str(re.findall('<span class="a-size-medium a-color-base a-text-normal">(.*?)<', str(src), re.DOTALL)) +  str(re.findall('height="160" alt="(.*?)"', str(src), re.DOTALL))).replace('\',', '~')
        price = (str(re.findall('price"><span class="a-offscreen">(.*?)"', str(src), re.DOTALL)) + str(re.findall('price s-price a-text-bold">(.*?)</a>', str(src), re.DOTALL))).replace('\',', '~')
        outputFile = open('a1.csv','a', newline='', encoding="utf8")
        outputWriter = csv.writer(outputFile)
        for a, b, c in zip(link.split('~'), name.split('~'), price.split('~')):
            d = [a + "~" + b + "~" + c]
            outputWriter.writerow([d])
            final.extend(d)
        outputFile.close()
    else:
        results1 = soup.find_all('div', {'class' : 's-item-container'})
        link = str(str(re.findall('class="a-link-normal"(.*?)>', str(src), re.DOTALL)) +  str(re.findall('data-asin="(.*?)"', str(src), re.DOTALL))).replace('\',', '~')
        name = str(str(re.findall('<span class="a-size-medium a-color-base a-text-normal">(.*?)<', str(src), re.DOTALL)) +  str(re.findall('height="160" alt="(.*?)"', str(src), re.DOTALL))).replace('\',', '~')
        price = (str(re.findall('price"><span class="a-offscreen">(.*?)"', str(src), re.DOTALL)) + str(re.findall('price s-price a-text-bold">(.*?)</a>', str(src), re.DOTALL))).replace('\',', '~')
        outputFile = open('a1.csv','a', newline='', encoding="utf8")
        outputWriter = csv.writer(outputFile)
        for a, b, c in zip(link.split('~'), name.split('~'), price.split('~')):
            d = [a + "~" + b + "~" + c]
            outputWriter.writerow([d])
            final.extend(d)
        outputFile.close()
    #if re.compile('|'.join(keywords),re.IGNORECASE).search(src):
    if any(y in src for y in ('="Next', 'a-last')):
        print ('Next page')
        counter = 1
        while True:
            counter += 1
            pg = '&page=' + str(counter)
            try:
                pgn = str(tit) + str(pg)
                #pgn = pgn.split('page=')[0] + str(pg)
                print (pgn)
                #buttons = browser.find_elements_by_xpath("//*[contains(text(), 'Next')]")
                #for btn in buttons:
                    #btn.click()
                #time.sleep(.)
                try:
                    res1 = requests.get(pgn, headers=headers)
                except:
                    res1 = 'n/a'
                src11 = str(res1.text).replace('amp;', '').replace('href="', '').replace('https://www.amazon.in/', '')   #for different layout
                link0 = str(str(re.findall('class="a-link-normal"(.*?)>', str(src11), re.DOTALL)) +  str(re.findall('data-asin="(.*?)"', str(src11), re.DOTALL))).replace('\',', '~')
                name0 = str(str(re.findall('<span class="a-size-medium a-color-base a-text-normal">(.*?)<', str(src11), re.DOTALL)) +  str(re.findall('height="160" alt="(.*?)"', str(src11), re.DOTALL))).replace('\',', '~')
                price0 = (str(re.findall('price"><span class="a-offscreen">(.*?)"', str(src11), re.DOTALL)) + str(re.findall('price s-price a-text-bold">(.*?)</a>', str(src11), re.DOTALL))).replace('\',', '~')
                outputFile = open('a1.csv','a', newline='', encoding="utf8")
                outputWriter = csv.writer(outputFile)
                for d, e, f in zip(link0.split('~'), name0.split('~'), price0.split('~')):
                    g = [d + "~" + e + "~" + f]
                    outputWriter.writerow([g])
                    final.extend(g)
                outputFile.close()
                #print(any(x in a for x in b))
                if any(z in src11 for z in ('pagnRA1', 'a-disabled a-last', 'Try checking your spelling or use more general terms')):
                    #print ('captcha')
                    break
                #src1.extend(src)
            except:
                pass
            #if 'pagnRA1' in res.text:
                #os.system("taskkill /im chromedriver.exe")
                #os.system("taskkill /im chrome.exe")
                #pass
                #break
    else:
        continue

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 18:22:53 2018

@author: Administrator
"""

#首页：http://cn.fifaaddict.com/fo4db?class=live&age=0-25
#所有球员的名字://tbody//tr/td[@class="info"]/div[@class="info-inner"]/a/text()
#所有球员的图片://tbody//tr/td[@class="info"]/div[@class="info-inner"]/img/@src
#球员名字按钮：class="player-name"
#//div[@class="attrwrap"]/ul//li  #进入球员详情页面后匹配球员所有的能力值


from lxml import etree
import requests
from selenium import webdriver
import time
import csv
from selenium.webdriver.common.by import By

#driver = webdriver.Chrome()
#driver.get('http://cn.fifaaddict.com/fo4db?class=live&age=0-25')
#
#time.sleep(5)

url = 'http://cn.fifaaddict.com/fo4db?class=live&age=0-25'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'}
res = requests.get(url,headers=headers)
res.encoding = 'utf-8'
html = res.text

parsehtml = etree.HTML(html)
photo_list = parsehtml.xpath('//tbody//tr/td[@class="info"]/div[@class="info-inner"]/img/@src')
#print(photo_list)

name_list = parsehtml.xpath('//tbody//tr/td[@class="info"]/div[@class="info-inner"]/a/text()')
#print(name_list)
#print(str(name_list[0]))


#x = 0
#for r in photo_list:
#    es = requests.get(str(r),headers=headers)
#    es.encoding = 'utf-8'
#    h = es.content
#    name = str(name_list[x])[0:-1]
#    with open(name+'.png','wb') as f:
#        f.write(h)
#    x += 1
    
#http://cn.fifaaddict.com/fo4db/piddlkkbbwz
#href="http://cn.fifaaddict.com/fo4db/piddlkkbbwz"
#http://cn.fifaaddict.com/fo4db/piddlkkbbwz

#//tbody/tr/td[@class="info"]/div[@class="info-inner"]/a/@href  #名字链接
#//tbody/tr/td[@class="info"]/div[@class="info-inner"]/a/text() #链接文本
#//div[@class="attrwrap"]/ul//li/span[@class="name"] #详情页面能力项名称
#//div[@class="attrwrap"]/ul//li/span[@class="value"] #详情页面能力项数值
#//i [@class="posbg rw"] #球员详情页面RW按钮

urlStart = 'http://cn.fifaaddict.com'
name_href_list = parsehtml.xpath('//tbody/tr/td[@class="info"]/div[@class="info-inner"]/a/@href')
#for name_href in name_href_list:
#    print(str(name_href).strip())

name_link_list = parsehtml.xpath('//tbody/tr/td[@class="info"]/div[@class="info-inner"]/a/text()')
#print('56行：',name_link_list)

driver = webdriver.Chrome()

y = 0
for name_link in name_link_list:
    time.sleep(2)
    name = str(name_link).strip()
    
    print('75行：',name)
    
    driver.get('http://cn.fifaaddict.com/fo4db?class=live&age=0-25')
#    driver.find_element_by_link_text(name).click()
    driver.find_element(By.PARTIAL_LINK_TEXT,name).click()
    
    time.sleep(1)
    
    print('80行：')
    res_star = requests.get(urlStart+str(name_href_list[y]).strip(),headers=headers)
    y += 1
    res_star.encoding = 'utf-8'
    html_star = res_star.text
    
    print('85行html_star为',html_star)
    starhtml = etree.HTML(html_star)
    time.sleep(1)
    ability_name_list = starhtml.xpath('//div[@class="perform"]/ul/li/span[@class="name"]')
    ability_value_list = starhtml.xpath('//div[@class="perform"]/ul/li/b[contains(@class,"value")]')
    print('90行：',ability_name_list)
    print('91行：',ability_value_list)
    
    with open('FIFA_Star.csv','a',newline='',encoding='gb18030') as f:
        writer = csv.writer(f)
        writer.writerow([name])
    for a_name,a_value in zip(ability_name_list,ability_value_list):
        print('95行')
        with open('FIFA_Star.csv','a',newline='',encoding='gb18030') as f:
            writer = csv.writer(f)
            writer.writerow([a_name.text,a_value.text])
            print(a_name.text,a_value.text)
            print('写入成功')
    with open('FIFA_Star.csv','a',newline='',encoding='gb18030') as f:
        writer = csv.writer(f)
        writer.writerow([])
        


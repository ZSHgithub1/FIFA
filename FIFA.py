# -*- coding: utf-8 -*-

from lxml import etree
import requests
from selenium import webdriver
import re
import csv

a_name = ['姓名','年龄','俱乐部','位置','国家','传中','射术','头球','短传','临空抽射','盘带','弧线','任意球','长传','控球','加速','速度','敏捷','反应','平衡','射门力量','弹跳','体能','强壮','远射','侵略性','拦截意识','跑位','视野','点球','沉着','盯人','断球','铲球','鱼跃','手型','开球','站位','反应']
with open('球星.csv','a',newline='',encoding='gb18030') as f:
            writer = csv.writer(f)
            writer.writerow(a_name)

url = 'https://sofifa.com/players?aeh=22/'
for pn in range(2):
    if pn == 1:
        url = 'https://sofifa.com/players?aeh=22&offset=60'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko'}
    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    html = res.text
    parseHtml = etree.HTML(html)
    star_link_list = parseHtml.xpath('//div [@class="col-name text-ellipsis rtl"]/a[2]/@href')
    #print(star_link_list)
    
    star_start_url = 'https://sofifa.com'
    index = 0
    for star_link in star_link_list:
        star_l = star_start_url+str(star_link)
    
    
        mbp = star_start_url + str(star_link_list[index])
        index += 1
        res_M = requests.get(mbp,headers=headers)
        res_M.encoding = 'utf-8'
        html_M = res_M.text
        #print(html_M)
        r = re.compile('<div class="meta">(.*?)<a.*?Age(.*?)\(',re.S)
        r_f = r.findall(html_M)
        #print(r_f)
        
        
        #头像://div[@class="card card-border player fixed-width"]/img/@data-src
        #姓名:name = r_f[0][0].strip()
        #年龄:age = r_f[0][1].strip()
        #球队://div[@class="teams"]/div/div[3]//ul/li/a/text()
        #位置://div[@class="meta"]/span[1]/text()
        #国籍://div[@class="teams"]/div/div[4]/ul/li[1]/a/text()
        #能力值第一行：//div[@class="mt-2 mb-2"]/div/div/ul/li
        #能力值第二行：//div[@class="card card-border player fixed-width"]/div[@class="mb-2"][2]//li
        
        name = r_f[0][0].strip()
        age = r_f[0][1].strip()
        parse_star = etree.HTML(html_M)
        club = parse_star.xpath('//div[@class="teams"]/div/div[3]//ul/li/a/text()')
        position = parse_star.xpath('//div[@class="meta"]/span[1]/text()')
        country = parse_star.xpath('//div[@class="meta"]/a/@title')
        nlz_one = parse_star.xpath('//div[@class="mt-2 mb-2"]/div/div/ul/li')
        nlz_two = parse_star.xpath('//div[@class="card card-border player fixed-width"]/div[@class="mb-2"][2]/div[1]/div/ul/li')
        nlz_three = parse_star.xpath('//div[@class="card card-border player fixed-width"]/div[@class="mb-2"][2]/div[2]//li')
        nlz_four = parse_star.xpath('//div[@class="card card-border player fixed-width"]/div[@class="mb-2"][2]/div[3]//li')
        
        print(name)
        print(age)
        print(club[0])
        print(position[0])
        print(country[0])
        
        photo_url = parse_star.xpath('//div[@class="card card-border player fixed-width"]/img/@data-src')
        photo_url = str(photo_url[0])
        res_photo = requests.get(photo_url,headers=headers)
        res_photo.encoding = 'utf-8'
        photo = res_photo.content
        with open(name+'.png','wb') as f:
            f.write(photo)
            print('图片下载成功')
        
        a_value = []
        a_value.append(name)
        a_value.append(age)
        a_value.append(club[0])
        a_value.append(position[0])
        a_value.append(country[0])
        
        for one in nlz_one:
            if len(one) == 3:
#                a_name.append(one[2].text)
                a_value.append(int(one[0].text)+int(one[1].text))
            else:
#                a_name.append(one[1].text)
                a_value.append(int(one[0].text))
                
        for two in nlz_two:
#            print(len(two))
            if len(two) == 3:
#                a_name.append(two[2].text)
                a_value.append(int(two[0].text)+int(two[1].text))
            elif len(two) == 2:
#                a_name.append(two[1].text)
                a_value.append(int(two[0].text))
            else:
                a_value.append(int(two[0].text))
#                a_name.append('Composure')
        for three in nlz_three:
            if len(three) == 3:
                a_value.append(int(three[0].text)+int(three[1].text))
            elif len(three) == 2:
                a_value.append(int(three[0].text))
            else:
                a_value.append(int(three[0].text))
                
        for four in nlz_four:
            if len(four) == 3:
                a_value.append(int(four[0].text)+int(four[1].text))
            elif len(four) == 2:
                a_value.append(int(four[0].text))
            else:
                a_value.append(int(four[0].text))
        
        print(a_name)
        print(a_value)

        with open('球星.csv','a',newline='',encoding='gb18030') as f:
            writer = csv.writer(f)
            writer.writerow(a_value)
#!/usr/bin/env python
#coding:utf-8
from selenium import webdriver
from pyvirtualdisplay import Display
 
display = Display(visible=0, size=(800,600))
display.start()

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
#options.add_argument('--headless') 
options.add_argument('Referer=https://www.tvmao.com')
driver = webdriver.Chrome(chrome_options=options)
driver.set_window_size(1366, 768)
driver.get("https://www.tvmao.com/program/CCTV-CCTV1-w1.html")
driver.implicitly_wait(15) 
#i = raw_input()

labels = driver.find_elements_by_class_name("am")
for x in labels:
    print x.text

labels = driver.find_elements_by_class_name("pm")
for x in labels:
    print x.text

labels = driver.find_elements_by_class_name("nt")
for x in labels:
    print x.text

labels = driver.find_elements_by_class_name("p_show")
for x in labels:
    print x.text

driver.close()
driver.quit()

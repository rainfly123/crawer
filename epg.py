#!/usr/bin/env python
#coding:utf-8

import sys  
reload(sys)
sys.setdefaultencoding("utf-8")
import datetime
import time
from pyvirtualdisplay import Display
from selenium import webdriver
import pickle

FILE = "/tmp/epg"

def load():
    try:
        f = open(FILE)
    except IOError:
        return 0

    which = pickle.load(f)
    f.close()
    return which

def dump(which):
    out = open(FILE, "w")
    pickle.dump(which, out)
    out.close()

def remove():
    os.remove(FILE)


if __name__ == "__main__":
    import mysql

    fromwhich = load()
    if fromwhich >= 12:
        sys.exit(0)

    all_channels = [
          {
           "gid" : "cctv1",
           "urls": [
               'https://www.tvmao.com/program/CCTV-CCTV1-w%d.html',
               ]
          },
          {
           "gid" : "cctv2",
           "urls": [
               'https://www.tvmao.com/program/CCTV-CCTV2-w%d.html',
               ]
          },

          {
           "gid" : "cctv3",
           "urls": [
               'https://www.tvmao.com/program/CCTV-CCTV3-w%d.html',
               ]
          },
          {
           "gid" : "cctv4",
           "urls": [
               'https://www.tvmao.com/program/CCTV-CCTV4-w%d.html',
               ]
          },
          {
           "gid" : "cctv5",
           "urls": [
               'https://www.tvmao.com/program/CCTV-CCTV5-w%d.html',
               ]
          },
          {
           "gid" : "cctv5p",
           "urls": [
               'https://www.tvmao.com/program/CCTV-CCTV5-PLUS-w%d.html',
               ]
          },
          {
           "gid" : "cctv6",
           "urls": [
               'https://www.tvmao.com/program/CCTV-CCTV6-w%d.html',
               ]
          },
          {
           "gid" : "cctv8",
           "urls": [
               'https://www.tvmao.com/program/CCTV-CCTV8-w%d.html',
               ]
          },
          {
           "gid" : "cctv9",
           "urls": [
               'https://www.tvmao.com/program/CCTV-CCTV9-w%d.html',
               ]
          },
          {
           "gid" : "cctv10",
           "urls": [
               'https://www.tvmao.com/program/CCTV-CCTV13-w%d.html',
               ]
          },

          {
           "gid" : "cctv13",
           "urls": [
               'https://www.tvmao.com/program/CCTV-CCTV13-w%d.html',
               ]
          },
          {
           "gid" : "gdws",
           "urls": [
                'https://www.tvmao.com/program_satellite/GDTV1-w%d.html',
               ]
          },
          ]

    display = Display(visible=0, size=(800,600))
    display.start()

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
    options.add_argument("--no-sandbox")
    #options.add_argument('--headless') 
    options.add_argument('Referer=https://www.tvmao.com')
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_window_size(1366, 768)



    now = datetime.datetime.now()
    dayofweek = now.weekday()

    for channel in all_channels[fromwhich:]:
        which = 2 #tomorrow
        store_path = "/data/" + channel['gid'] 
        gid = channel['gid'] 
        for url in channel['urls']:
            url = url%(dayofweek + which + 1)
            driver.get(url)
            driver.implicitly_wait(15) 
            now = datetime.datetime.now() 
            now += datetime.timedelta(which, 0, 0)
            nowstr = now.strftime("%Y-%m-%d ")
            labels = driver.find_elements_by_class_name("am")
            am = [x.text for x in labels]
            labels = driver.find_elements_by_class_name("pm")
            pm = [x.text for x in labels]
            labels = driver.find_elements_by_class_name("nt")
            nt = [x.text for x in labels]
            alltime = am + pm + nt
            labels = driver.find_elements_by_class_name("p_show")
            pname = [x.text for x in labels]
            allprograms = list()
            for x in alltime:
                allprograms.append({"time":nowstr + x, "program_name":pname[alltime.index(x)]})
            for x in allprograms:
                print gid, x["time"], x["program_name"]
                mysql.UpdateEPG(gid, x["program_name"], x["time"], store_path)
            fromwhich += 1
            dump(fromwhich)

    driver.close()
    driver.quit()
    display.stop()


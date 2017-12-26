import time 
import requests
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
import queue
import threading

def getsouphtml():
    start = time.time()
    browser = webdriver.Firefox()
    #使用selenium.webdriver模拟打开firefox以获取由js引擎加载的网页内容
    browser.maximize_window()  
    browser.get('http://xueqiu.com/#/cn')  
    browser.maximize_window()
    for i in range(1, 5):
        #模拟鼠标向下滚动  
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')  
        time.sleep(1.5)  
    
    for i in range(4):  
        # 找到加载更多按钮，总共点击4次
        browser.find_element(By.LINK_TEXT, "加载更多").click()  
        time.sleep(1.5)  
    
    soup = BeautifulSoup(browser.page_source,'lxml')
    #通过bs库获取加载后的整个网页的所有信息 
    browser.close() 
    stop = time.time()
    print('browser time %s'%(stop - start))
    #打印浏览器运行的时间
    return soup , start , stop

def get_list_url(article_queue):
    the_queue = queue.Queue()
    #设定一个queue对象
    eachitem = article_queue.find_all('div',attrs = {'class':'home__timeline__item'})
    #由find_all方法找出包含所有的文章url的一个list
    for i in eachitem:
        #循环获取list并添加到ullist中
        url = dict(i.h3.a.attrs)['href']
        article_url = 'https://xueqiu.com' + url
        the_queue.put(article_url)
    return the_queue


class Mythreading(threading.Thread):
    

    def __init__(self,aqueue):
        threading.Thread.__init__(self)
        self.aqueue = aqueue
        #定义线程类
    def run(self):
       while True:
            try:
                
                eachurl = self.aqueue.get()
                #从aqueue中提取文章url,并提取每个url中的具体内容
                add_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0'}
                eacharticle = requests.get(eachurl,headers = add_headers)
                eacharticle.encoding = 'utf-8'
                eacharticle = eacharticle.text
                detail = BeautifulSoup(eacharticle,'lxml')
                title = detail.find(attrs = {'class':'article__bd__title'})
                bodydetail = detail.find(attrs = {'class':'article__bd__detail'})
                #分别获取title和body
                #打印
                for i in title.stripped_strings:
                    print(i)
                print('\n')
                for k in bodydetail.stripped_strings:
                    print(k)
                print('\n\n')
                self.aqueue.task_done()
                #获取成功后将成功信号传递给aqueue
            except:
                
                print('Can not get this article!!!!!!!!!!!!!')
                self.aqueue.task_done()
             
'''
def soup_eachurl(urllist):
    num = 0
    #num用来统计爬出的文章数目
    for eachurl in urllist:
        #由循环获取list中的每个url，并提取每个url中的具体内容
        add_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0'}
        eacharticle = requests.get(eachurl,headers = add_headers)
        eacharticle.encoding = 'utf-8'
        eacharticle = eacharticle.text
        detail = BeautifulSoup(eacharticle,'lxml')
        title = detail.find(attrs = {'class':'article__bd__title'})
        bodydetail = detail.find(attrs = {'class':'article__bd__detail'})
        #分别获取title和body
        try:
            #打印
            num+=1
            print('第%s篇文章'%num)
            for i in title.stripped_strings:
                print(i)
            print('\n')
            for k in bodydetail.stripped_strings:
                print(k)
            print('\n\n')

        except:
            num-=1
            continue
    return num
'''
def main():
    article_list , start , stop = getsouphtml()
    aqueue = get_list_url(article_list)
    for i in range(10):
        athread = Mythreading(aqueue)
        athread.setDaemon(True)
        athread.start()
    
    aqueue.join()
    print('browser time %s'%(stop - start))
main()

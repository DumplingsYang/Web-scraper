import time 
import requests
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from multiprocessing import Pool , Process , Queue , Manager
import os


def write(q):
    '''
    创建write方法，用来将目标内容soup化，并put添加进q
    '''
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

    eachitem = soup.find_all('div',attrs = {'class':'home__timeline__item'})
    #由find_all方法找出包含所有的文章url的一个list
    for i in eachitem:
        #循环获取list并添加到ullist中
        url = dict(i.h3.a.attrs)['href']
        article_url = 'https://xueqiu.com' + url
        q.put(article_url)



def read(q):
    '''
    read方法通过get提取q中的内容，并通过soup打印出来
    '''
    while True:
        try:
            print('Process to print: %s' % os.getpid())
            #打印当前子进程的名称
            eachurl = q.get()
            #从q中提取文章url,并提取每个url中的具体内容
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
            q.task_done()
            #若执行成功，通过task_done方法将信号传给q
        except:
            print('Can not get this article!!!!!!!!!!!!!')
            q.task_done() 
            #若执行失败，也通过task_done方法将信号传给q，用来跳过


m = Manager()
#Manage方法用来管理当前正在进行的进程
q = m.Queue()
#配合Queue创建一个进程可以共享的queue
pw = Process(target=write, args=(q,))
#运行写入q进程
for i in range(4):

    #通过for循环创建4个子进程
    p = Process(target=read,args = (q,))
    p.daemon = True
    #设立守护，若主程序结束，则还在运行的子进程也退出
    p.start()
pw.start()
pw.join()
#join阻碍主进程，程序执行到这里起吗有一两个子进程在运行，确保不会broke pipe
q.join()
#确保所有子进程运行完毕，因为read方法中遍历了q中所有的元素，并task_done()，所以保证q全部执行完毕





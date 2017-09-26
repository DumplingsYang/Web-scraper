import re
from bs4 import BeautifulSoup
import requests
import traceback

def getHTMLtext(url):
	try:
		r=requests.get(url,timeout=30)
		r.raise_for_status()
		r.encoding=r.apparent_encoding
		return r.text
	except:
		print('')

def getStockList(ulist,Stockurl)
	html=getHTMLtext(Stockurl)
	soup=BeautifulSoup(html,'html.parser')
	a=soup.find_all('a')
	for i in a: 
		try:
			href=i.attrs['href']
			ulist.append(re.findall(r'[s][hz]\d{6}',href)[0])
		except:
			continue

def getStockinfo(ulist, Stockurl,fpath):
	for stock in ulist:
		url=Stockurl+stock+".html"
		html=getHTMLtext(url)
		try:
			if html="":
				continue
			infoDcit={}
			soup=BeautifulSoup(html,'html.parser')
			stockInfo=soup.find('div',attrs={'class':'stock-bes'})
			name=stockInfo.find_all(attrs={'class':'bets-name'})[0]
			infoDict.update({'股票名称':name.text.split()[0]})
			keyList=stockInfo.find_all('dt')
			valuelist=stockInfo.find_all('dd')
			for i in range(len(keyList)):
				key=keyList[i].text
				val=valuelist[i].text
				infoDcit[key]=val
			with open(fpath,'a',encoding='utf-8')as f:
				f.write(str(infoDcit)+'\n')
		except:
			traceback.print_exc()
			continue

def main():
	stock_list_url='http://quote.eastmoney.com/stocklist.html'
	stock_info_url='https://gupiao.baidu.com/stock/'
	outputfile='Users/yang/Desktop'
	ulist=[]
	getStockList(ulist,stock_list_url)
	getStockinfo(ulist,stock_info_url,outputfile)

main()

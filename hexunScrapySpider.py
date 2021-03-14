import requests
import demjson
import tablib
import time

def getHTMLDATA(url, kv):
	try:
		r = requests.get(url, headers = kv, timeout = 30)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return "ERROR"

def main():
	urla = "http://stockdata.stock.hexun.com/zrbg/data/zrbList.aspx?date=2018-12-31&count=20&pname=20&titType=null&page="
	pages = 208
	kv = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	data = []

	for page in range(1,pages+1):
		url = urla + str(page)
		demo = getHTMLDATA(url, kv)
		html = demo[13:-1]
		dataDict = demjson.decode(html)
		dataList = dataDict['list']
		for dictInList in dataList:
			del dictInList['StockNameLink']
			del dictInList['Hstock']
			del dictInList['Wstock']
			del dictInList['Tstock']
		data += dataList
		time.sleep(1)

	allData = []
	tableHeader = tuple(["序号","股票名称/代码","股东责任","总得分","等级","员工责任","供应商、客户和消费者权益责任","环境责任","社会责任"])
	
	for row in data:
		body = []
		for v in row.values():
			body.append(v)
		allData.append(tuple(body))
	
	allData = tablib.Dataset(*allData, headers=tableHeader)
	open('C:\\Users\\song\\Desktop\\2018-data.xlsx','wb').write(allData.xlsx)

main()

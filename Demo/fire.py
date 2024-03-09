from asyncio import events
from importlib.resources import path
from operator import truediv
from optparse import Values
import os
from turtle import color, goto
import PySimpleGUI as sg      
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import numpy as np
from selenium.webdriver.common.keys import Keys
from matplotlib import cm
from pprint import pprint
from datetime import datetime
import matplotlib.pyplot as plt
import googlemaps
import googletrans
import time
import datetime
import csv
import pandas as pd
import os
import time


usname=os.getlogin( )
usname="./weight-loss-master/"+usname+".csv"
list1 = []
list2 = []
listfin=[]
persona = []
gmaps = googlemaps.Client(key='AIzaSyDZHZuedToDI01GxJnXQWodNCkZEKbUnZM')
temparr = []
temparr2 = []
tmplsit=[]
translator = googletrans.Translator()
outputarr = []
def operation1():
	global temparr
	#getblocke = driver.find_element_by_xpath('//*[@type="button"]')
	#getblocke.click()
	k=1
	print("hi")
	list1.clear()
	tmplsit.clear()
	list2.clear()
	while 1:
		windows=driver.window_handles  #get all windows in your browser
		driver.switch_to.window(windows[-1])
		print("ichange1!")
		for i in driver.find_elements_by_xpath('//*[@class="gl fb e2 e3"]'):
			print("hji")
			list1.append(i.text)
		for i in driver.find_elements_by_xpath('//*[@class="ey fy ez ex"]'):
			print("hji")
			list1.append(i.text)
		#print(list1)
		if(len(list1)!=0):
			print(list1)
			break
	while 1:
		for i in driver.find_elements_by_xpath('//*[@class="ah am b6"]'): #class="ba c4 bb c5 ax"
			tmplsit.append(i.text)
		for i in driver.find_elements_by_xpath('//*[@class="ah am ed"]'): #class="ba c4 bb c5 ax"
			tmplsit.append(i.text)
		#print(tmplsit)
		if len(tmplsit)==0:
			continue
		else:
			list2.clear()
			for xx in range(len(tmplsit)):
				list2.append(tmplsit[xx])
			break


	#print(list1[0])
	#print(list2[0])

	

	outputarr.clear()
	for i in range(len(list2)):
		list2[i]=list2[i].encode('unicode_escape').decode('ascii')
		temparr=list1[0].encode('unicode_escape').decode('ascii')
		temparr2=list2[i]
		try:
			temparr=temparr[:temparr.index(" ")]
			temparr2=temparr2[:temparr2.index('\n')]
			try:
				temparr2=temparr2[:temparr2.index(" ")]
			except:
				temparr2=temparr2
		except:
			temparr=temparr
		try:
			temparr2=temparr2[:temparr2.index(" ")]
		except:
			temparr2=temparr2
		temparr=temparr+"_"+temparr2
		#print(temparr)
		outputarr.append(temparr.encode('ascii').decode('unicode_escape'))
		#print("%s ," %(temparr))
		#print(temparr.encode('ascii').decode('unicode_escape'))
	temp=[]
	outputmil=[]
	outputmilna=[]
	outputmilall=[]
	outputmilgg=[]
	outputmilnagg=[]
	namarr=[]
	scorearr=[]
	temp.clear()
	outputmil.clear()
	outputmilna.clear()
	outputmilall.clear()
	namarr.clear()
	scorearr.clear()
	outputmilgg.clear()
	outputmilnagg.clear()
	try:
		with open('scnew.csv', 'r') as file1:
					reader= csv.reader(file1)
					for row in reader:
						temp.append(row)

		max=100
		for j in range(len(temp)):
			for i in range(len(temp)):
				if(float(temp[i][1])<max):
					max=float(temp[i][1])
					tt=i
			if temp[tt][0] == "Constant":
				temp[tt][1]="999"
				max=998
			else:
				namarr.append(temp[tt][0])
				scorearr.append(float(temp[tt][1]))
				temp[tt][1]="999"
				max=998
				
	except:
		a=0
	colorl=[]
	colorlg=[]
	colorl.clear()
	colorlg.clear()
	idnum=-1
	for x in range(len(namarr)):
		if namarr[x]==outputarr[0]:
			colorl.append('#FFA500')
			colorlg.append('#00FF00')
		else: 
			colorl.append('black')
			colorlg.append('black')
	salesss = scorearr
	x_labelsss = namarr
	plt.clf()
	plt.rcParams['font.family']='Noto Sans CJK JP'
	plt.barh(x_labelsss,salesss,color=colorl)
	plt.savefig('all.png')
	plt.clf()
	plt.rcParams['font.family']='Noto Sans CJK JP'
	plt.barh(x_labelsss,salesss,color=colorlg)
	plt.savefig('allhe.png')
	for xx in range(len(outputarr)):
		for xxx in range(len(namarr)):
			if namarr[xxx]==outputarr[xx]:
				outputmilna.append(namarr[xxx-4])
				outputmilna.append(namarr[xxx-3])
				outputmilna.append(namarr[xxx-2])
				outputmilna.append(namarr[xxx-1])
				outputmilna.append(namarr[xxx])
				outputmil.append(scorearr[xxx-4])
				outputmil.append(scorearr[xxx-3])
				outputmil.append(scorearr[xxx-2])
				outputmil.append(scorearr[xxx-1])
				outputmil.append(scorearr[xxx])
				idnum=xxx
	if idnum==-1:
		with open(usname, 'a') as file:
				file.write("%s " % (temparr))
		sg.popup('You Ordered', outputarr)
		os.exit(0) 

	plt.clf()
	sales = outputmil
	x_labels = outputmilna
	plt.rcParams['font.family']='Noto Sans CJK JP'
	plt.barh(x_labels,sales,color=['black','black','black','black','#FFA500'])
	plt.savefig('danger.png')
	


	
	#if float(outputmil[4])>0:
		#out()
	print(namarr)
	print(scorearr)
	print(outputmil[4])
	if outputmil[4]>0:
		sg.theme('DarkAmber')
		layout = [[sg.Text('此食物容易造成肥胖(數值越大越容易造成肥胖)',font=("Helvetica", 25), text_color=('#FFA500'))],   
				[sg.Image('danger.png')],
						[sg.Text('1)重新選擇餐點 2)查看完整列表 3)送出餐點'),  sg.InputText()  ],
						[sg.Submit(), sg.Cancel(),]]
		window12 = sg.Window("Name", layout)
		event, values = window12.read() 
		window12.close()
		strr=str(values)
		if(strr[5]=="2"):
			layout = [[sg.Text('此食物容易造成肥胖(數值越大越容易造成肥胖)',font=("Helvetica", 25), text_color=('#FFA500'))],   
				[sg.Image('all.png')],
						[sg.Text('1)重新選擇餐點 2)送出餐點'),  sg.InputText()  ],
						[sg.Submit(), sg.Cancel(),]]
			window22 = sg.Window("Name", layout)
			event, values = window22.read() 
			window22.close()
		if(strr[5]=="3"):
			with open(usname, 'a') as file:
				file.write("%s " % (temparr))
			#print(temparr.encode('ascii').decode('unicode_escape'))
			sg.popup('You Ordered', outputarr)
		
		strr=str(values)
		print(strr[5])
		
		if(strr[5]=="1"):
			driver.find_element_by_xpath( '//*[@class="di ag ah am"]').click()
			driver.find_element_by_xpath('.//option[@value="0"]').click()
			driver.find_element_by_xpath( '//*[@class="be dd dh"]').click()
			operation1()
		if(strr[5]=="2"):
			with open(usname, 'a') as file:
				file.write("%s " % (temparr))
			#print(temparr.encode('ascii').decode('unicode_escape'))
			sg.popup('You Ordered', outputarr)
	else:
		layout = [[sg.Text('Smart Choice',font=("Helvetica", 25), text_color=('#00FF00'))],   
				[sg.Image('allhe.png')],
						[sg.Text('1)重新選擇餐點 2)送出餐點'),  sg.InputText()  ],
						[sg.Submit(), sg.Cancel(),]]
		window12 = sg.Window("Name", layout)
		event, values = window12.read() 
		window12.close()
		strr=str(values)
		if(strr[5]=="2"):
			with open(usname, 'a') as file:
				file.write("%s " % (temparr))
			#print(temparr.encode('ascii').decode('unicode_escape'))
			sg.popup('You Ordered', outputarr)
		

		
		if(strr[5]=="1"):
			driver.find_element_by_xpath( '//*[@class="di ag ah am"]').click()
			driver.find_element_by_xpath('.//option[@value="0"]').click()
			driver.find_element_by_xpath( '//*[@class="be dd dh"]').click()
			operation1()



	

	
	
	



	#print(opt)

	"""
	print("hi")
	ddelement= Select(driver.find_element_by_xpath('//*[@class="ba bx bb by bc ci ax br bs bt bn bo c9 eh ec tm hn ei tn"]'))
	ddelement.select_by_value('0')
	"""
	"""
	for i in range(len(list2)):
		list2[i]=list2[i].encode('unicode_escape').decode('ascii')
		temparr=list1[0].encode('unicode_escape').decode('ascii')
		temparr2=list2[i]
		try:
			temparr=temparr[:temparr.index(" ")]
			temparr2=temparr2[:temparr2.index('\n')]
			try:
				temparr2=temparr2[:temparr2.index(" ")]
			except:
				temparr2=temparr2
		except:
			temparr=temparr
		try:
			temparr2=temparr2[:temparr2.index(" ")]
		except:
			temparr2=temparr2
		temparr=temparr+"_"+temparr2
		#print(temparr)
		outputarr.append(temparr.encode('ascii').decode('unicode_escape'))
		#print("%s ," %(temparr))
		with open(usname, 'a+') as file:
			file.write("%s " % (temparr))
		#print(temparr.encode('ascii').decode('unicode_escape'))
	sg.popup('You Ordered', outputarr)
	"""
	#getblocke = driver.find_element_by_xpath('//*[@rel="nofollow"]')
	#getblocke.click()
try:
	with open('person.csv', 'r') as file1:
		#print()
		a=0
except:
    layout = [[sg.Text('Please Enter Your PersonalData')],      
                 [sg.Text('Please enter your name'), sg.InputText()],
                 [sg.Text('Please enter your Height(Cm)'), sg.InputText()],
                 [sg.Text('Please enter your Weight(Kg)'), sg.InputText()],
                 [sg.Text('Please enter your age'), sg.InputText()],
                 [sg.Text('Please enter your location'), sg.InputText()],
                 [sg.Submit(), sg.Cancel()]]      
    window = sg.Window('Body Control', layout) 
    event, values = window.read()    
    window.close()
    sg.popup('Submitted!!') 
    with open('person.csv', 'w') as file1:
        file1.write("%s\n" % (values[0]))
        file1.write("%s\n" % (values[1]))
        file1.write("%s\n" % (values[2]))
        file1.write("%s\n" % (values[3]))
        location1 = gmaps.geocode(values[4])
        jin=location1[0]['geometry']['location']['lat']
        wei=location1[0]['geometry']['location']['lng']
        file1.write("%s\n" % (jin))
        file1.write("%s\n" % (wei))
        file1.write("%s\n" % (values[4]))
with open('person.csv', 'r') as file1:
	reader= csv.reader(file1)
	for row in reader:
		persona.append(row)
	
	#print("Hello %s !\n" % (persona[0][0]))
	location = persona[6][0]
  # 建立 CSV 檔寫入器
  # 寫入另外幾列資料
lastday=[]
try:
	with open(usname, 'r') as file1:
		reader= csv.reader(file1)
		for row in reader:
			lastday.append(row)
	if str(lastday[len(lastday)-1][0])!=str(datetime.date.today()):
		with open(usname, 'a') as file:
			layout = [[sg.Text(datetime.date.today())],      
						[sg.Text('Please enter your Weight today'), sg.InputText()],
						[sg.Submit(), sg.Cancel()]]      
			window = sg.Window('Body Control', layout) 
			event, values = window.read()    
			window.close()	
			#print(datetime.date.today())
			file.writelines("%s,%s," % (datetime.date.today(),values[0]))
except:
	with open(usname, 'a') as file:
		file.write("Date,MorningWeight,YesterdayFactors\n")
		layout = [[sg.Text(datetime.date.today())],      
					[sg.Text('Please enter your Weight today'), sg.InputText()],
					[sg.Submit(), sg.Cancel()]]      
		window = sg.Window('Body Control', layout) 
		event, values = window.read()    
		window.close()	
		#print(datetime.date.today())
		file.writelines("%s,%s," % (datetime.date.today(),values[0]))
#print(lastday[len(lastday)-1][0])
	
  
while(1):
	# 設定基本參數
	desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
	#此處必須換成自己電腦的User-Agent
	desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

	# PhantomJS driver 路徑
	driver = webdriver.PhantomJS(executable_path = 'phantomjs', desired_capabilities=desired_capabilities)

	# 關閉通知提醒
	
	driver = webdriver.Chrome()

	#driver = webdriver.Firefox('geckodriver.exe')

	# 去到你想要的網頁
	driver.get("https://www.ubereats.com/tw")
	time.sleep(3)




	#---------- 開始網頁的控制 ----------
	#--- 輸入外送地址
	getblock = driver.find_element_by_xpath('//*[@placeholder="輸入外送地址"]')
	getblock.send_keys(location) # 輸入地址
	time.sleep(1)
	getblock.send_keys(Keys.ENTER) # 按下Enter
	operation1()
	break
	list1.clear()




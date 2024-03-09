import pandas as pd
import matplotlib.pyplot as plt
import csv
import PySimpleGUI as sg
from matplotlib.font_manager import FontProperties
import subprocess
import googlemaps
import os
threshold_weight_p = 0.03
threshold_weight_n = -0.03
usname=os.getlogin()
usname="./weight-loss-master/"+usname+".csv"
sg.theme('LightBrown3')

gmaps = googlemaps.Client(key='AIzaSyDZHZuedToDI01GxJnXQWodNCkZEKbUnZM')
try:
		with open('person.csv', 'r') as file1:
		#print()
			a=0
except:
		layout = [[sg.Text('Please Enter Your PersonalData')],      
					[sg.Text('Please enter your name'), sg.InputText()],
					[sg.Text('Please enter your Height(cm)'), sg.InputText()],
					[sg.Text('Please enter your Weight(kg)'), sg.InputText()],
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
layout = [  [sg.Text('You want?\n1. Show/Edit my personal data\n2. Analyze the influence\n3. Show the weight change\n4. Show diet records\n5. Show Steps records\n6. Ordering on UBEREAT!\n7. ExchangeData!\nx. END\n')],
            [sg.Text('Choice: '),
            sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

window = sg.Window('Window Title', layout, font=("宋體", 30), default_element_size=(50,10))
font = FontProperties(fname=r'NotoSansTC-Regular.otf')

arr = []

os.system("gnome-terminal -e 'bash -c \"python3 ./give_keyandport/rec/aa.py & exec bash\"'")
while 1:
	
	while True:
		event, values = window.read()  #獲取文本框輸入內容
		if event == sg.WIN_CLOSED or event == 'Cancel':
			break
		print('You entered:', values[0])
		
		if values[0] == 'x':
			break
		elif values[0] == '1':
			qqg=[]
			with open('person.csv', 'r') as file1:
				reader= csv.reader(file1)
				for row in reader:
					qqg.append(row)
			layout = [      
					[sg.Text('Name : %s' %(qqg[0][0]))],
					[sg.Text('Height(cm):%s'%(qqg[1][0]))],
					[sg.Text('Weight(kg):%s'%(qqg[2][0]))],
					[sg.Text('Age:%s'%(qqg[3][0]))],
					[sg.Text('Address: %s'%(qqg[6][0]))],
					[sg.Text('Comfirm Or Edit(C/E)?'), sg.InputText()],
					[sg.Submit(), sg.Cancel()]]      
			window2 = sg.Window('Body Control', layout) 
			event, values = window2.read()    
			window2.close()
			if values[0]=="E":
				layout = [[sg.Text('Please Enter Your PersonalData')],      
					[sg.Text('Please enter your name'), sg.InputText()],
					[sg.Text('Please enter your Height(cm)'), sg.InputText()],
					[sg.Text('Please enter your Weight(kg)'), sg.InputText()],
					[sg.Text('Please enter your age'), sg.InputText()],
					[sg.Text('Please enter your location'), sg.InputText()],
					[sg.Submit(), sg.Cancel()]]      
				window1 = sg.Window('Body Control', layout) 
				event, values = window1.read()    
				window1.close()
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
		elif values[0] == '2':
			os.chdir('./weight-loss-master')
			os.system('make')
			os.system('cp scores.txt ../')
			os.chdir('..')
			ff = open('scores.txt')
			if ff.readline() != 'FeatureName,Influence,Score\n':
				ff.close()
				with open('scores.txt', 'r+') as f:
					content = f.read()
					f.seek(0, 0)
					f.write('FeatureName,Influence,Score\n'+content)
					f.close()
			dff = pd.read_csv("scores.txt")
			dff.to_csv("scores.csv", encoding='utf-8', index=False)
			print("Gonna analyze the diet influence to your weight...")
			df = pd.read_csv('scores.csv', encoding='utf-8')
			result = df[["FeatureName", "Influence"]]
			result.set_index('FeatureName', inplace=True)
			chart = result.plot(kind='barh', figsize=(20, 15), fontsize=15)
			for label in chart.get_yticklabels():
				label.set_fontproperties(font)  # 設定x軸每一字型
			plt.title('體重影響', fontproperties=font, fontsize=20)
			plt.xlabel('影響指數(weight)', fontproperties=font, fontsize=20)
			plt.ylabel('特徵', fontproperties=font, fontsize=20)
			plt.legend(prop=font)
			plt.show()
		elif values[0] == '3':
			print("Gonna show your weight change...")
			df = pd.read_csv(usname, encoding='utf-8')
			result = df[["Date", "MorningWeight"]]
			result.set_index('Date', inplace=True)
			chart = result.plot(legend=True, figsize=(20, 15), fontsize=15)
			plt.title('Weight Change', fontsize=20)
			plt.xlabel('Date', fontsize=20)
			plt.ylabel('Weight(kg)', fontsize=20)
			plt.show()
		elif values[0] == '4':
			ff = open('scores.txt')
			if ff.readline() != 'FeatureName,Influence,Score\n':
				ff.close()
				with open('scores.txt', 'r+') as f:
					content = f.read()
					f.seek(0, 0)
					f.write('FeatureName,Influence,Score\n'+content)
					f.close()
			dff = pd.read_csv("scores.txt")
			dff.to_csv("scores.csv", encoding='utf-8', index=False)
			
			fname='scores.csv'
			rows_n = sum(1 for line in open(fname))
			rows_n -= 1  #Ignore the first row.
			
			fea_num = [0]*rows_n
			for i in range(rows_n):
				fea_num[i] = 0
				
			hea_num = [0]*rows_n
			for i in range(rows_n):
				hea_num[i] = 0
    		
			df = pd.read_csv('scores.csv', encoding='utf-8')
			inf = df["Influence"]
			fea = df["FeatureName"]
			
			dfff = pd.read_csv(usname, encoding='utf-8')
			factors = dfff["YesterdayFactors"]
			num_meals = 0
			for fac in factors:
				num_meals += len(fac.split())
			
			for i in range(rows_n):
				if inf[i] >= threshold_weight_p:           # Threshold of BEING FAT.
					for fac in factors:
						if fea[i] in fac.encode('ascii').decode('unicode_escape'):
							fea_num[i] += 1
				elif inf[i] <= threshold_weight_n:         # Threshold of HEALTHY food.
					for fac in factors:
						if fea[i] in fac.encode('ascii').decode('unicode_escape'):
							hea_num[i] += 1
			#for i in range(rows_n):
			#	print(i,"  fea: ",fea_num[i])
			#for i in range(rows_n):
			#	print(i,"  hea: ",hea_num[i])
			
			for i in range(rows_n):
				num_meals -= fea_num[i]
				num_meals -= hea_num[i]
			print("????")
			print(fea_num)
			print(hea_num)
			cnt = 0
			arr = []
			arr2 = []
			for i in range(rows_n):
				if fea_num[i] != 0:
					arr.append(fea[i])
					arr2.append(fea_num[i])
					cnt += 1
			for i in range(rows_n):
				if hea_num[i] != 0:
					arr.append(fea[i])
					arr2.append(hea_num[i])
			arr.append("Remaining meals")
			arr2.append(num_meals)
			
			ser1 = pd.Series(arr)
			ser2 = pd.Series(arr2)
			dataframe = pd.DataFrame({'1':ser1, '2':ser2})
			print(dataframe)
			
			plt.figure(figsize=(15,10))
			print(arr2)
			labels = dataframe["1"]
			separeted = []
			colors = []
			print(cnt)
			for i in range(len(arr2)):
				if i <= cnt-1:
					separeted.append(0.3)
					colors.append('red')
				elif i == len(arr2)-1:
					separeted.append(0)
					colors.append('khaki')
				else:
					separeted.append(0.2)
					colors.append('green')
			size = dataframe["2"]

			p, l_text, n_text = plt.pie(size,
					colors = colors,
					labels = labels,
					autopct = "%1.1f%%",
					explode = separeted,            # 設定分隔的區塊位置
					pctdistance = 0.6,
					textprops = {"fontsize" : 12},
					shadow=True)
			for l in l_text:
				l.set_fontproperties(font)
				l.set_size(15)
			for n in n_text:
				n.set_size(15)
			 
			plt.axis('equal')
			plt.title("Analysis of Diet Composition", {"fontsize" : 20})
			plt.legend(loc = "best", prop = font, fontsize = 15)

			plt.show()
			plt.close()
		elif values[0] == '5':
			subprocess.run(["python3", "sleep_steps.py"])
			print("\n")
		elif values[0] == '6':
			subprocess.run(["python3", "pan.py"])
			print("\n")
		
		
		elif values[0] == '7':
			os.system("gnome-terminal -e 'bash -c \"python3 ./give_keyandport/sub/bb.py & exec bash\"'")
			print("\n")
	window.close(); del window

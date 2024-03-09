import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties as font
import csv
import PySimpleGUI as sg
namarr=[]
scorear=[]
scorearr=[]
temp=[]
from matplotlib import font_manager
font_set = {f.name for f in font_manager.fontManager.ttflist}
for f in font_set:
    print(f)
with open("scnew.csv", 'r') as file1:
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
print(namarr)
print(scorearr)
temp.clear()
print(len(scorear))
for s in range(len(scorearr)):
    scorear.append(0)
print(scorear)
with open("scores.txt", 'r') as file1:
	reader= csv.reader(file1)
	for row in reader:
		temp.append(row)
print(temp[2][1])
for j in range(len(temp)):
    for i in range(len(namarr)):
        print(temp[j][0])
        print(namarr[i])
        if(temp[j][0]==namarr[i]):
            scorear[i]=float(temp[j][1])
            break
print(scorear)
menuhel=[]
menuheln=[]
muentemp=[]
menufat=[]
menufatn=[]
with open("scnew.csv", 'r') as file1:
	reader= csv.reader(file1)
	for row in reader:
		muentemp.append(row)
max=100
for j in range(len(muentemp)):
      if float(muentemp[j][1])<0 and muentemp[j][2]=="new" and muentemp[j][0]!="Constant":
            print(muentemp[i][2])
            menuhel.append(muentemp[j][1])
            menuheln.append(muentemp[j][0])
for j in range(len(muentemp)):
      if float(muentemp[j][1])>0 and muentemp[j][2]=="new" and muentemp[j][0]!="Constant":
            menufat.append(muentemp[j][1])
            menufatn.append(muentemp[j][0])
print("fhht:")
print(menuheln)
print("fat:")
print(menufatn)
left = np.array(namarr)
height1 = np.array(scorear)
height2 = np.array(scorearr)

labels = namarr
font1 = font(fname="NotoSansTC-Regular.otf")
plt.style.use('ggplot')
font = {
 'family' : 'Noto Sans CJK JP',
        'weight' : 'bold',
        'size'   : '10'}
plt.rc('font', **font)               # 步驟一（設定字型的更多屬性）
plt.rc('axes', unicode_minus=False)
#chart = result.plot(kind='barh', figsize=(20, 15), fontsize=15)
#bar1 = plt.bar(left, height1,color='blue', yerr=0.01, tick_label=labels)
bar1 = plt.bar(left, height1, color='#0055FF', yerr=0.01,alpha=1, tick_label=labels)
#選擇要在上面的棒狀圖 red   誤差6
bar2 = plt.bar(left, height2,  yerr=0.01, color='#FF8800', ec='#FF0000',  alpha=0.5,tick_label=labels)

plt.title('Title')
plt.legend((bar1[0], bar2[0]), ('Before', 'After'))
plt.show()





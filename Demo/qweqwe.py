import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import csv
df = px.data.tips()
dis=[]
menuhel=[]
menuheln=[]
muentemp=[]
menufat=[]
menufatn=[]
orgfatn=[]
orgthinn=[]
pat=[]
paf=[]
pa=[]
with open("scnew.csv", 'r') as file1:
	reader= csv.reader(file1)
	for row in reader:
		muentemp.append(row)
max=100
for j in range(len(muentemp)):
      if float(muentemp[j][1])<0 and muentemp[j][2]=="new" and muentemp[j][0]!="Constant":
            menuhel.append(muentemp[j][1])
            menuheln.append(str(muentemp[j][0]))
for j in range(len(muentemp)):
      if float(muentemp[j][1])>0 and muentemp[j][2]=="new" and muentemp[j][0]!="Constant":
            menufat.append(muentemp[j][1])
            menufatn.append(muentemp[j][0])
for j in range(len(muentemp)):
      if float(muentemp[j][1])>0 and muentemp[j][2]=="old" and muentemp[j][0]!="Constant":
            orgfatn.append(muentemp[j][0])
            
for j in range(len(muentemp)):
      if float(muentemp[j][1])<0 and muentemp[j][2]=="old" and muentemp[j][0]!="Constant":
            orgthinn.append(muentemp[j][0])

leb=["Orgin","New", "Fat(Org)", "Thin(Org)", "Fat(New)", "Thin(New)"]
par=["","","Orgin","Orgin","New","New"]
for s in range(len(orgthinn)):
    leb.append(orgthinn[s])
    par.append("Thin(Org)")
for s in range(len(orgfatn)):
    leb.append(orgfatn[s])
    par.append("Fat(Org)")
for s in range(len(menuheln)):
    leb.append(menuheln[s])
    par.append("Thin(New)")
for s in range(len(menufatn)):
    leb.append(menufatn[s])
    par.append("Fat(New)")
print(menuheln)
print("fat:")
print(menufatn)
pa.append("")
pa.append("")
for i in range(len(menuheln)):
    pat.append("Healthy")
    if i > 3:
        break
for i in range(len(menufatn)):
    paf.append('Unhealthy')
    if i > 3:
        break
dis.append("Healthy")
dis.append("Unhealthy")
for i in range(len(pat)):
    dis.append(menuheln[i])
for i in range(len(paf)):
    dis.append(menufatn[i])
pa=pa+pat+paf
print(pa)
print(dis)
fig = go.Figure(go.Sunburst(
    labels=leb,
    parents=par,

))
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0),
                  title_text='Meals')
fig.show()

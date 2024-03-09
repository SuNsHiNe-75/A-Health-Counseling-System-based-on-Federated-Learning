from asyncio import events
from operator import truediv
from optparse import Values
import os
from turtle import color
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
def out():
	sg.theme('DarkAmber')
	layout = [[sg.Text('此食物容易造成肥胖')],   
			[sg.Image('danger.png')],
					[sg.Text('1)重新選擇餐點 2)查看完整列表 3)送出餐點'),  sg.InputText()  ],
					[sg.Submit(), sg.Cancel(),]]
	window = sg.Window("Name", layout)
	event, values = window.read()    
	window.close()	
	strr=str(values)
	print(strr[5])
	
out()
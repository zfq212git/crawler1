# -*- coding: UTF-8 -*-

# requests is a python lib used for http level data communication
import requests
import re

#BeautifulSoup is a good html parser to help cawler to get wanted data in a easy way
from bs4 import BeautifulSoup

import urllib
import webbrowser

import xlrd
import xlwt
from openpyxl import load_workbook

import excel_processing


url_list = []
key_word_list = []

#note: if uisng r, return normal string; if using rb, return binary.  It will impact the following string processing.
#note: if there is Chinese (non-English) characters in data.txt, we need explicitly assign encoding = utf-8 here
#note: for each line, when we save it in the list, we'd better remove the line return cahracter - \n, otherwise it may cause trouble later
data_file = open("data.txt", "r", encoding = "UTF-8")

break_line = 0

#please check the format used in data.txt
for line in data_file:
	#print (line[0])
	if(break_line ==0 and line[0] == "*"):
		break_line = 1

	if (break_line == 0 and line[0] != "*"):
		url_list.append(line.strip("\n"))
	
	if (break_line == 1 and line[0] != "*"):
		key_word_list.append(line.strip("\n"))

data_file.close()


#try to write the crawlered data in a excel file.  We use openpyxl as 3rd party but did not use xlrd/xlwt, becasue only openpyxl
#can handle editing existing excel document
dataX=load_workbook("archive1.xlsx")
sheetFor3D=dataX.get_sheet_by_name('3D')
sheetForOther=dataX.get_sheet_by_name('other')
sheetX=dataX.get_sheet_by_name('Sheet3')

starting_row_number_3D = int(sheetX['A1'].value)
starting_row_number_Other = int(sheetX['B1'].value)

for url in url_list:
	#print (url)
	page = requests.get(url)
	soup = BeautifulSoup(page.text,"lxml")

	for key_word in key_word_list:
		#print(key_word)
		find = soup.find_all('a', text=re.compile(key_word))
		#print(find)	
		for link in find:		

			index0 = link.get('href')
			indexLen=int(len(index0))
			print(indexLen)
			index = index0[indexLen-10:indexLen-6] + '\n'

			print(index0)
			print(index)

			index_file = open('index.txt','r')
			index_list = index_file.read()
			if index not in index_list:
				index_file.close()
				if (key_word == '3D' or key_word == "三维"):
					#webbrowser.open_new_tab(link.get('href'))
					sheetFor3D['A'+str(starting_row_number_3D+1)] = key_word
					sheetFor3D['A'+str(starting_row_number_3D+2)] = index0
					starting_row_number_3D=starting_row_number_3D+3
				else:
					sheetForOther['A'+str(starting_row_number_Other+1)] = key_word
					sheetForOther['A'+str(starting_row_number_Other+2)] = index0
					starting_row_number_Other=starting_row_number_Other+3
				index_file = open('index.txt','a')
				index_file.write(index+'\n')
				index_file.close()			

	
sheetX['A1']=starting_row_number_3D
sheetX['B1']=starting_row_number_Other	
dataX.save("archive1.xlsx")


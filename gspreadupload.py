#General Imports
import time
import credentials
import csv

import gspread


username = '###'
password = '###'

from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(creds)


#Google Sheets Moderation


time.sleep(180)
with open("msglist.csv","rU") as f:
	reader = csv.reader(f)
	data = list(list(rec) for rec in csv.reader(f,delimiter=","))
	wks=gc.open("DataSheet").sheet1	

	for row in data:
		try:
			wks.insert_row(row,index=2)
		except:
			gc = gspread.authorize(creds)
			wks.insert_row(row,index=2)
		print(row)
		time.sleep(3)
with open("msglist.csv","w") as f:
	f.truncate()


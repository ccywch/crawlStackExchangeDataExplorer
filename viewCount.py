# -*- coding: utf-8 -*-
#Author: Chen Chunyang

import re
import time 
from selenium import webdriver
from selenium.webdriver import ActionChains
import os
import shutil
from operator import itemgetter
import collections
import MySQLdb

#As stackexchange explorer can only return 50k results, so we needs to record data piece by piece
def selectData(inputFile, outputFile):
	f = open(inputFile)
	lines = f.readlines()
	f.close()
	
	fw = open(outputFile, "w")
	for index, row in enumerate(lines):
		if index%50000 == 49999:
			fw.write(row.strip()+" ")
	fw.close()
	

#Use selenium to get data
def sendRequent(url, order):
	try:
		print order
		browser = webdriver.Chrome()
		browser.get(url)
		#time.sleep(5)
		fillin = browser.find_element_by_id("sql")
		#print "This is textarea: ",fillin.is_displayed()
		#print "here"
		fillin.send_keys(order)
		#ActionChains(browser).move_to_element(fillin).send_keys(order).perform()
		time.sleep(10)
		submit_button = browser.find_element_by_id('submit-query')
		submit_button.click()
		
		time.sleep(20)
		download = browser.find_element_by_id("resultSetsButton")
		#print download
		download.click()
		time.sleep(12)
		#print browser.current_url
		browser.quit()
	
	except Exception, e :
			print e		

#send requent according to the order			
def getData(inputFile, url, inputDir, outputDir, newLast):
	f = open(inputFile)
	dataPoint = f.read().split()
	f.close()
	
	fileName = ""
	for i in range(len(dataPoint)):
		if i == 0:
			order = "select ID, viewCount from posts where id<=" + dataPoint[i] +" and posttypeid=1"
		else:
			order = "select ID, viewCount from posts where id>" + dataPoint[i-1] + " and id<= " + dataPoint[i] +" and posttypeid=1"
		sendRequent(url, order)
		fileName = dataPoint[i]+".csv"
		moveFile(inputDir, outputDir, fileName)
		
	
	oldLast = int(dataPoint[-1])        #The last questionPost in our database
	#newLast = 31364402                  #The new questionPost in data exploerer
	for i in range((newLast-oldLast)/100000+1):
		order =  "select ID, viewCount from posts where id>" + str(oldLast+i*100000) + " and id<= " + str(oldLast+(i+1)*100000) +" and posttypeid=1"
		sendRequent(url, order)
		fileName = str(oldLast+(i+1)*100000) + ".csv"
		moveFile(inputDir, outputDir, fileName)
		

#Move files from default location to where you desire and rename by query
def moveFile(inputDir, outputDir, name):
	for file in os.listdir(inputDir):
		if file.find("QueryResults")>-1:	
			shutil.move(inputDir+file, outputDir+name)
		
		
#Combine crawled data into one file	
def combineData(inputDir, outputFile, date):
	postView = {}
	for file in os.listdir(inputDir):
		if file.find(".csv")>-1:
			f = open(inputDir+file)
			lines = f.readlines()
			f.close()
			#print file
			for index, row in enumerate(lines):
				if index == 0:
					continue
				row = row.strip().replace("\"", "")
				#if int(row.split(",")[0]) in postView:
				#	print file
				#	break
				postView[int(row.split(",")[0])] = row.split(",")[1] 
				
	print len(postView)
	
	'''
	postView_previous = {}
	title = ""
	
	f = open(outputFile)
	lines = f.readlines()
	f.close()
	
	for index, row in enumerate(lines):
		row = row.strip()
		if index == 0:
			title = row+","+date
		else:
			row = row.split(",")
			postView_previous[int(row[0])] = ",".join(row[1:])
	'''
	
	
	#Store data for the first time
	fw = open(outputFile, "w")
	#postView = sorted(postView.iteritems(), key=itemgetter(1), reverse=False)
	#postView_ordered = collections.OrderedDict(sorted(postView.items()))
	postView_ordered = sorted(postView)
	fw.write("ID,"+date+"\n")
	for key in postView_ordered:
		fw.write(str(key)+","+postView[key]+"\n")
	fw.close()
	
		
if __name__=='__main__':
	
	queryURL = "https://data.stackexchange.com/stackoverflow/query/new"
	
	date = "0919"
	newLast = 32545956
	
	samplePoint = "samplePoint.txt"
	dataOriginDir = "C:\\Users\\CHEN0966\\Downloads\\"
	dataDir = "D:\\PhD\\data\\stackoverflow\\viewCount\\rawData_"+date+"\\"
	dataCombination = "dataCombination_"+date+".csv"
	
	
	#Every time you run this program, please revise variable "date" and "newLast" in getData() accordingly
	try:
		#selectData("questionID.txt", samplePoint)
		#sendRequent(queryURL)
		#getData(samplePoint, queryURL, dataOriginDir, dataDir, newLast)
		combineData(dataDir, dataCombination, date)
		#moveFile(dataOriginDir, dataDir, "agcfg")
	except Exception, e :
		print e	
		raise

	
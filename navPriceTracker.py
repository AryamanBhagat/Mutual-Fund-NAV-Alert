import datetime
from datetime import date, timedelta
from typing import ValuesView 
from urllib.request import urlopen
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import smtplib, ssl

port = 465 #for SSL
sender_email = #enter the email id you want to send to here
password = #enter password
context = ssl.create_default_context()



pd.options.mode.chained_assignment = None  # default='warn'



def subtractDays(window, date):#
    return date - timedelta(days=window)



threshold_for_alert = -3 #percent should be negative value
window = 10  #window should be less than 90 because AMF doesnt allow you to get 
endDate = date.today()
startDate = subtractDays(window, endDate)
recievers = ["aryamanbhagat2000@gmail.com"] #make list of recivers here



fundHouseNames = ["20", "48"] #ICICI, IDFC
fundNames = [["ICICI Prudential US Bluechip Equity Fund - Direct Plan -  Growth"], ["IDFC Tax Advantage  (ELSS) Fund-Direct Plan-Growth "]]
subject = "Mutual Fund Price Drop Alert"


def getDateString(date):
    return date.strftime("%d")+"-"+date.strftime("%b")+"-"+date.strftime("%Y")


def getMutualFundHouseNavHistory(startDate, endDate, fundHouseName):
    #https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?mf=25&frmdt=01-Jan-2022&todt=29-Jan-2022
    url_mf = "https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?mf="
    url_startDate = "&frmdt="
    url_endDate = "&todt="
    url_complete = url_mf + fundHouseName + url_startDate + getDateString(date=startDate) + url_endDate + getDateString(date=endDate)
    file = urlopen(url_complete)
    output = str()
    for line in file:
        decoded_line = line.decode("utf-8")
        output = output + decoded_line
    return output


def removeNonCSVLines(file):
    lines = file.split('\n')
    output = str()
    for line in lines:
        if ";" in line:
            output = output + line + "\n"
    
    return output
        

def getMutualFundHouseDataframe(startDate, endDate, fundHouseName):
    file = getMutualFundHouseNavHistory(startDate, endDate, fundHouseName)
    file = removeNonCSVLines(file)
    data = StringIO(file)
    df = pd.read_csv(data, sep=';')
    #select on fundName
    #df_fundName = df.loc[df['Scheme Name'] == fundName]
    #order on Date
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df_fundName = df.sort_values(by = ['Scheme Name', 'Date'])
    return df_fundName

def calculateLargestDropPercentage(data):
    endPrice = data.iloc[-1]
    dataPercentage = data.apply(lambda a: ((endPrice-a)/a)*100)
    return dataPercentage.min()


def findPercentageMovementInMutualFunds(fundHouseNames, fundNames):
    percentageMovementList = []
    for i, fundHouse in enumerate(fundHouseNames):
        df = getMutualFundHouseDataframe(startDate, endDate, fundHouse)
        for fund in fundNames[i]:
            df_fund = df.loc[df['Scheme Name'] == fund]
            #caculate change
            df_change = df_fund['Net Asset Value']
            #startPrice = df_change.iloc[0]
            #endPrice = df_change.iloc[-1]
            #print(df_fund)
            #print(startPrice)
            #print(endPrice)
            change = calculateLargestDropPercentage(df_change)
            #add to list
            percentageMovementList.append((fund, change))
    return percentageMovementList
    


def sendAlert(percentageList):
    alert = False
    body = "The Mutual Funds you monitor have dropped below " + str(-1*threshold_for_alert) + "% in a moving window calculation with window size " + str(window) + ".\n Find the list of percentage drop* below\n\n"
    for tuple in percentageList:
        fund = tuple[0]
        percentage = tuple[1]
        body = body + str(tuple)
        if percentage < threshold_for_alert:
            alert = True
            body = body + "*"
        body = body + "\n"
    if alert:
        print("hello")
        message = 'Subject: {}\n\n{}'.format(subject, body)
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            for receiver in recievers:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver, message)
                server.quit()


#df = getMutualFundHouseDataframe(startDate, endDate, fundHouseNames[0])
#print(df)
#print(df.head(50))
percentageMovementList = findPercentageMovementInMutualFunds(fundHouseNames, fundNames)
#print(percentageMovementList)
sendAlert(percentageMovementList)
#df.info(verbose=True)
#df.plot(x = 'Date', y = 'Net Asset Value', kind = 'line')
#print(df)
#plt.show()







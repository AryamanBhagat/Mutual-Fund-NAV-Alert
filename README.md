# Mutual-Fund-NAV-Alert
This is a simple python script that you can setup to run at 11AM everyday, it will send an alert through email if the NAVs of mutual funds fall below a certain amount

# How it works
Everyday at 10AM www.amfindia.com generates a list of latest Net Asset Values of various mutual funds.

The python script will scrape all that data and see if any of the mutual funds have fallen below a certain threshold in the last few days.

The scipt then sends email alerts to all subscribers

# How can I get it to work
1.Clone this repository

2.Change the .bat file to represnt the locations of your python installations and repository locations. you may refer to https://towardsdatascience.com/automate-your-python-scripts-with-task-scheduler-661d0a40b279

3.Set up a task in the windows schduler. Keep in mind that AMF updates NAV values at 10AM everyday.

4.You can then play around with the various values in the python script. you will need to do the following.

  -create a gmail account
  
  -enter the details of the account in the python script
  
  -make a list of reciever addresses, add against the relevant variable in the python script
  
  -use the https://www.amfiindia.com/nav-history-download to find out the codes of your mutualFundHouses
  
 for example the following url generates all the NAV prices for the IDFC from 1st Jan 2022 to 6th Jan 2022
 https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?mf=48&frmdt=01-Jan-2022&todt=06-Jan-2022
 
 so we can see that the code for IDFC is 48
 
 # Why would I want something like this
 
 you want to buy mutual funds for cheap and dont want to check prices everyday.


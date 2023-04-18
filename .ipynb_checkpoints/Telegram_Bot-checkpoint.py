# -*- coding: utf-8 -*-

#link to get user id/ group id or any activity related to our bot
#https://api.telegram.org/bot5747611163:AAFqIPOxRGTXP25py8mNdXRL7mz-TfsouO8/getUpdates


import requests

#please generate your bot and update TelegramBotCredential and ReceiverTelegramID below :

TelegramBotCredential = '6113918545:AAEBK6cQUM3C_yfp_CCXX9TfvmYhDJXhRDU'
ReceiverTelegramID = '5242432731' #my personal id


def SendMessageToTelegram(Message):
    try:
        Url = "https://api.telegram.org/bot" + str(TelegramBotCredential) +  "/sendMessage?chat_id=" + str(ReceiverTelegramID)
        
        textdata ={ "text":Message}
        response = requests.request("POST",Url,params=textdata)
    except Exception as e:
        Message = str(e) + ": Exception occur in SendMessageToTelegram"
        print(Message)  
		
		
def SendTelegramFile(FileName):
    Documentfile={'document':open(FileName,'rb')}
    
    Fileurl = "https://api.telegram.org/bot" + str(TelegramBotCredential) +  "/sendDocument?chat_id=" + str(ReceiverTelegramID)
      
    response = requests.request("POST",Fileurl,files=Documentfile)
	

SendMessageToTelegram("HI")
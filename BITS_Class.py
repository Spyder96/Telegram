
import time 
from datetime import datetime 
import pyautogui
from pynput.keyboard import Controller
from pynput.keyboard import Key
import webbrowser as wb
import telegram
from dotenv import load_dotenv
import os
import YFinance as YF
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

CHAT_ID = 727464642

load_dotenv()
TelegramBotCredential = os.environ.get('BOT_TOKEN')
updater = Updater(TelegramBotCredential)
bot = telegram.Bot(token=TelegramBotCredential)





advNetwork =   'https://teams.microsoft.com/l/meetup-join/19%3ae557afd8241a4f46921e12acdf373443%40thread.tacv2/1681035716016?context=%7b%22Tid%22%3a%22e24ac094-efd8-4a6b-98d5-a129b32a8c9a%22%2c%22Oid%22%3a%22b86d8394-7d7f-455e-b7ea-7416d0412e1f%22%7d'
cloudComp =    'https://teams.microsoft.com/l/meetup-join/19%3a569baddaad0e402e9c5a429af87ca48c%40thread.tacv2/1681035828532?context=%7b%22Tid%22%3a%22e24ac094-efd8-4a6b-98d5-a129b32a8c9a%22%2c%22Oid%22%3a%22b86d8394-7d7f-455e-b7ea-7416d0412e1f%22%7d'
itInfra =      'https://teams.microsoft.com/l/meetup-join/19%3ae8643548da9349b39364f50d485c1a96%40thread.tacv2/1681035949968?context=%7b%22Tid%22%3a%22e24ac094-efd8-4a6b-98d5-a129b32a8c9a%22%2c%22Oid%22%3a%22b86d8394-7d7f-455e-b7ea-7416d0412e1f%22%7d'
webTech =      'https://teams.microsoft.com/l/meetup-join/19%3a52704304e0aa4bf596aaa276eac1c398%40thread.tacv2/1681036071776?context=%7b%22Tid%22%3a%22e24ac094-efd8-4a6b-98d5-a129b32a8c9a%22%2c%22Oid%22%3a%22b86d8394-7d7f-455e-b7ea-7416d0412e1f%22%7d'

lst=[
     [  itInfra, 855, 1035],
     [ cloudComp, 1055, 1230],
     [  advNetwork, 1355, 1530],
     [ webTech, 1555, 1735]
     ]


#input lecture stats in form of list ......
# ["Link", start_time, end_time ]
# give time in 24 hrs format...
keyboard= Controller()
i=0
time_left=0

is_class_started =False
sunday = True
while sunday:
    today = datetime.now().weekday()
    if today != 6:  # Sunday is represented by 6
        print("Today is not Sunday.")
        bot.send_message(chat_id=CHAT_ID, text=f"sleeping for {600} secs. Today is not Sunday.")
        time.sleep(600)
    else:
        print("Today is Sunday.")
        
        bot.send_message(chat_id=CHAT_ID, text=f"Entering lectures. Today is Sunday.")
        
        sunday = False

for lecture  in lst:
    while True:
    #Checking for end timing of the selected class and skipping if required
    #Program run after the end of selected class
        if ((datetime.now().hour*100) + datetime.now().minute) >= lecture[2]:
            i+=1
            break

        
        #Checking for end timing of the selected class and joining if time left
        #Program run during the selected class
        elif (datetime.now().hour*100 + datetime.now().minute >= lecture[1]) and (((datetime.now().hour*100) + datetime.now().minute) < lecture[2]):
        
            wb.open(lecture[0])
            is_class_started=True
            time.sleep(10)
            for i in range (7):
                pyautogui.press('tab')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(5)
            # Take a screenshot
            screenshot = pyautogui.screenshot()
            # Save the screenshot as a file
            screenshot.save('screenshot.png')
            bot.send_photo(chat_id=CHAT_ID, photo=open('screenshot.png', 'rb'), caption= "Class Joined")
             
        #Program run before the selected class timings     
        elif   (datetime.now().hour*100 + datetime.now().minute < lecture[1]):
            
            time_left=lecture[1]-(datetime.now().hour*100 + datetime.now().minute)
            if time_left > 10:
                bot.send_message(chat_id=CHAT_ID, text=f"sleeping for {time_left*10} secs. Next class to join {lecture}")
                time.sleep(time_left*10) 
            else :
                time.sleep(time_left*10)
            
        while is_class_started:
            time_left=lecture[2]-(datetime.now().hour*100 + datetime.now().minute)
            print(f"sleeping for {time_left*10} secs")
            if time_left > 10:
                time.sleep(600)       #class joined, sleeping for the class period
                
                # Take a screenshot
                screenshot = pyautogui.screenshot()
                # Save the screenshot as a file
                screenshot.save('screenshot.png')
                bot.send_photo(chat_id=CHAT_ID, photo=open('screenshot.png', 'rb'))
            else:
                time.sleep(time_left*30)
            
            if time_left <= 0:              #exiting
                is_class_started=False
                pyautogui.hotkey('ctrl','shift','h')
                time.sleep(3)
              #  pyautogui.hotkey('alt','f4')
                time.sleep(3)
                screenshot = pyautogui.screenshot()
                # Save the screenshot as a file
                screenshot.save('screenshot.png')
                bot.send_photo(chat_id=CHAT_ID, photo=open('screenshot.png', 'rb'), caption= "Class Left")
                break;

                

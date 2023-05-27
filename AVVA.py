#Import the necessary packages
import speech_recognition as sr #recognise speech
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import PyPDF2
import speedtest
import webbrowser  
from twilio.rest import Client  
import time
import os  
from PIL import Image
import subprocess
import pyautogui
import pyttsx3
from pywikihow import search_wikihow
import datetime
import winsound  
import wikipedia
import pywhatkit
import cv2
from requests import get
import weathercom
import json
import requests
import wolframalpha
import pyjokes
import smtplib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import psutil  #to check battery percentage

import sys
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QTimer,QTime,QDate;
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from gui import Ui_AVVA 
import random
import math

##text to speech
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
engine.setProperty('rate', 170)

###### helper functions. Use them when needed #######

def engine_speak(text):
    text = str(text)
    engine.say(text)
    print("avva  :", text)
    engine.runAndWait()

#To wish
def wish():
    engine_speak("Initializing Nancy ")
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        engine_speak(f"good morning ,Currently it is {time.ctime()}")
    elif hour>12 and hour<18:
        engine_speak(f"good afternoon,Currently it is {time.ctime()}")
    else:
        engine_speak(f"good evening it is {time.ctime()}")
    engine_speak("Now I am online")
    
#To send email
def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('sender@gmail.com', 'sender@1999')
    server.sendmail('sender@gmail.com', to, content)
    server.close()

#To tell day to user
def tellDay():                                       # This function is for telling the day of the week
    day = datetime.datetime.today().weekday() + 1    # this line tells us about the number
    Day_dict = {1: 'Monday', 2: 'Tuesday',           # that will help us in telling the day
                3: 'Wednesday', 4: 'Thursday',
                5: 'AVVA ', 6: 'Saturday',
                7: 'Sunday'}
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        engine_speak("The day is " + day_of_the_week)

# For weather Report
def weatherReport(city):
    weatherDetails = weathercom.getCityWeatherDetails(city)
    humidity = json.loads(weatherDetails)["vt1observation"]["humidity"]
    temp = json.loads(weatherDetails)["vt1observation"]["temperature"]
    phrase = json.loads(weatherDetails)["vt1observation"]["phrase"]
    return humidity, temp, phrase

#To set alarm
def alarm(Timing):
    altime=str(datetime.datetime.now().strptime(Timing,"%I:%M %p"))
    altime=altime[11:-3]
    Horeal=altime[:2]
    Horeal=int(Horeal)
    Mireal=altime[3:5]
    Mireal=int(Mireal)
    engine_speak(f"done,alarm is set for {Timing}")
    while True:
        if Horeal==datetime.datetime.now().hour:
            if Mireal==datetime.datetime.now().minute:
                print("alarm is running")
                winsound.PlaySound('abc',winsound.SND_LOOP)# by default sound
            elif Mireal<datetime.datetime.now().minute:
                break

#To get news headlines from Times of India
def get_news():
    url = 'https://timesofindia.indiatimes.com/home/headlines'
    news = requests.get(url).text
    news_dict = json.loads(news)
    articles = news_dict['articles']
    try:
        return articles
    except:
        return False

#To make a note
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    notepad = "C:\\WINDOWS\\system32\\notepad.exe"
    subprocess.Popen([notepad, file_name])

#To convert size
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   print("%s %s" % (s, size_name[i]))
   return "%s %s" % (s, size_name[i])

#To check system status
def system_stats():
    cpu_stats = str(psutil.cpu_percent())
    battery_percent = psutil.sensors_battery().percent
    memory_in_use = convert_size(psutil.virtual_memory().used)
    total_memory = convert_size(psutil.virtual_memory().total)
    final_res = f"Currently {cpu_stats} percent of CPU, {memory_in_use} of RAM out of total {total_memory}  is being used and battery level is at {battery_percent} percent"
    return final_res

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.respond()

    # To listen for audio and convert it to text in English:
    def record_audio(self,ask=""):
        r = sr.Recognizer()  # initialise a recogniser
        with sr.Microphone() as source:   # microphone as source
            print("Listening...")
            if ask:
                engine_speak(ask)
            audio = r.listen(source,phrase_time_limit=4)# listen for the audio via source
            try:
                print("Recognizing...")
                voice_data = r.recognize_google(audio,language='en-in')  # convert audio to text

            except sr.UnknownValueError: # error: recognizer does not understand
                engine_speak("Sorry! I didn\'t get that. Try typing the command!")
                voice_data = str(input("Command: "))

            except sr.RequestError:
                engine_speak('Sorry, the service is down') # error: recognizer is not connected

            print("user said:", voice_data.lower()) # print what user said
            voice_data=voice_data.lower()
            return voice_data

    # To listen for audio and convert it to text in Hindi:
    def TakeHindi(self,ask=""):
        r = sr.Recognizer()  # initialise a recogniser
        with sr.Microphone() as source:  # microphone as source
            print("Listening...")
            if ask:
                engine_speak(ask)
            audio = r.listen(source, phrase_time_limit=4)  # listen for the audio via source
            try:
                print("Recognizing...")
                voice_data = r.recognize_google(audio, language='hi')  # convert audio to text

            except sr.UnknownValueError:  # error: recognizer does not understand
                engine_speak("Sorry! I didn\'t get that. Try typing the command!")
                voice_data = str(input("Command: "))

            except sr.RequestError:
                engine_speak('Sorry, the service is down')  # error: recognizer is not connected

            print("user said:", voice_data.lower())  # print what user said
            voice_data = voice_data.lower()
            return voice_data

    #To Translate the line in hindi
    def Tran(self):
        engine_speak("Tell Me The Line!")
        line = self.TakeHindi()
        traslate = Translator()
        result = traslate.translate(line)
        Text = result.text
        engine_speak("The Translation of this line is :" + Text)

    #To read the book
    def Reader(self):
        engine_speak("Tell me Name of the book!")
        name = self.record_audio()

        if 'history' in name:
            os.startfile("History.pdf")
            book = open('History.pdf', 'rb')
            pdfreader = PyPDF2.PdfFileReader(book)
            pages = pdfreader.getNumPages()
            engine_speak(f"Number of pages in this books are {pages}")
            engine_speak("Enter the page number,from which page I have to start Reading ?")
            numPage = int(input("Enter the page number"))
            page = pdfreader.getPage(numPage)
            text = page.extractText()
            engine_speak("In which Language ,I have to Read?")
            lang = self.record_audio()
            if "hindi" in lang:
                engine_speak("Sorry...,My hindi is a little weak, so my sister will read book for you in hindi,hope you like her voice.")
                transl = Translator()
                textHin = transl.translate(text, 'hi')
                textm = textHin.text
                speech = gTTS(text = textm)
                try:
                    speech.save("book.mp3")
                    playsound("book.mp3")
                except:
                    speech.save("book.mp3")
                    playsound("book.mp3")
            else:
                engine_speak(text)

    #To check speed of internet
    def speedTest(self):
        engine_speak("Checking speed....")
        speed = speedtest.Speedtest()
        downloading = speed.download()
        correctDown = int(downloading / 800000)
        uploading = speed.upload()
        correctUpload = int(uploading / 800000)
        if "uploading" in self.voice_data:
            engine_speak(f"The Uploading speed is {correctUpload} mbp s")
        elif "downloading" in self.voice_data:
            engine_speak(f"The downloading speed is {correctDown} mbp s")
        else:
            engine_speak(f"The downloading speed is {correctDown}  and The Uploading speed is {correctUpload} mbp s")


    def respond(self):
        while True:
            self.voice_data=self.record_audio("Listening...")
            print("okay ,done")

            #Logic building for tasks

            # 1: Greeting and interaction

            GREETINGS = ["hello","AVVA ","ava","ever", "hi", "wake up", "time to work", "hey", "ok", "are you there"]
            GREETINGS_RES = ["always there for you", "i am ready", "your wish my command", "how can i help you?",
                             "i am online and ready "]
            if self.voice_data in GREETINGS:
                engine_speak(random.choice(GREETINGS_RES))
            elif "thank you" in self.voice_data:
                engine_speak("your welcome...")
            elif "how are you"in self.voice_data or "how are you doing"in self.voice_data :
                engine_speak("I'm very well, thanks for asking " )
            elif "name" in self.voice_data:
                engine_speak("My name is AVVA  \n and what's your good name?")
                n=self.record_audio().replace("my name is","")
                engine_speak(f"{n}....\nnice name")
            elif "who are you" in self.voice_data:
                 engine_speak("i am AVVA  \n Your desktop Assistant \n I am here to make your life easier \n You can command me to perform various tasks such as calculating sums,opening applications,play games,movie recommendation extra")

            # 2 : Weather
            if "today's weather" in self.voice_data:
                city = self.record_audio("which city")
                humidity, temp, phrase = weatherReport(city)
                engine_speak("currently in " + city + "  temperature is " + str(temp)
                + " degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase)
                print("currently in " + city + "  temperature is " + str(temp)
                + "degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase)

            # 3:Translator
            if "translator" in self.voice_data:
                self.Tran()

            # 4:IP address
            if "ip address" in self.voice_data:
                ip = get('https://api.ipify.org').text
                engine_speak(f"your IP address is {ip}")
            if "What is your name" in self.voice_data:
                engine_speak("my name is nancy")
            #5:To find current location using IP Address
            elif "where am i" in self.voice_data or "current location" in self.voice_data or "where we are" in self.voice_data:
                engine_speak("wait,let me check")
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    url='https://get.io/v1/ip/geo/'+ipAdd+'.json'
                    geo_requests=requests.get(url)
                    geo_data=geo_requests.json()
                    #print (geo_data)
                    city=geo_data['city']
                    region=geo_data['region']
                    country = geo_data['country']
                    engine_speak(f"You are currently in {city} city which is in {region} state and country {country}")
                except Exception as e:
                    engine_speak("Sorry , I coundn't fetch your current location. Please try again")

            # 6:Dictionary
    

            # 7:Remember
            if "remember that" in self.voice_data:
                rememberMsg=self.voice_data.replace("remember that","")
                engine_speak("You tell me to remind you that :"+rememberMsg)
                remember=open('data.txt','w')
                remember.write(rememberMsg)
                remember.close()
            elif "what do you remember" in self.voice_data:
                remember=open('data.txt','r')
                engine_speak("You tell me that : "+remember.read())
                
            # 8:News
            elif 'news' in self.voice_data:
                    news_res = get_news()
                    engine_speak('Source: The Times Of India')
                    engine_speak('Todays Headlines are..')
                    for index, articles in enumerate(news_res):
                        #pprint.pprint((articles['title']))
                        engine_speak(articles['title'])
                        if index == len(news_res) - 2:
                          break
                    engine_speak('These were the top headlines, Have a nice day !!..')

            # 9:Set alarm
            if "alarm" in self.voice_data:
                engine_speak("please tell me the time to set alarm. for example,set alarm to 5.30am")
                tt=self.record_audio() #set alarm to 5.30am
                tt=tt.replace("set alarm to ","")#5.30a.m
                tt=tt.replace(".","")#5.30 am
                tt=tt.upper()#5.30 AM
                alarm(tt)

            # 10:Movie recommendation
            if "movie" in self.voice_data:
                engine_speak("Yes of course...,first I have to find out what kind of movie do you like ")
                engine_speak("So tell me name of your favorite hollywood movie ")
                ###### helper functions. Use them when needed #######
                def get_title_from_index(index):
                    return df[df.index == index]["title"].values[0]

                def get_index_from_title(title):
                    return df[df.title == title]["index"].values[0]

                ##################################################

                ##Step 1: Read CSV File
                df = pd.read_csv("movie_dataset.csv")
                # print df.columns
                ##Step 2: Select Features

                features = ['keywords', 'cast', 'genres', 'director']
                ##Step 3: Create a column in DF which combines all selected features
                for feature in features:
                    df[feature] = df[feature].fillna('')

                def combine_features(row):
                    try:
                        return row['keywords'] + " " + row['cast'] + " " + row["genres"] + " " + row["director"]
                    except:
                        print("Error:", row)

                df["combined_features"] = df.apply(combine_features, axis=1)

                # print "Combined Features:", df["combined_features"].head()

                ##Step 4: Create count matrix from this new combined column
                cv = CountVectorizer()

                count_matrix = cv.fit_transform(df["combined_features"])

                ##Step 5: Compute the Cosine Similarity based on the count_matrix
                cosine_sim = cosine_similarity(count_matrix)

                movie_user_likes=self.record_audio().title()

                ## Step 6: Get index of this movie from its title
                movie_index = get_index_from_title(movie_user_likes )


                similar_movies = list(enumerate(cosine_sim[movie_index]))

                ## Step 7: Get a list of similar movies in descending order of similarity score
                sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)
                engine_speak("Here are some movies i recommend you to watch, I hope you like them")

                ## Step 8: Print titles of first 5 movies
                for element in sorted_similar_movies[1:6]:
                    engine_speak(get_title_from_index(element[0]))

            # 11: To check internet speed
            if "downloading speed" in self.voice_data :
                self.speedTest()
            elif "uploading speed" in self.voice_data:
                self.speedTest()
            elif "internet speed" in self.voice_data :
                self.speedTest()

            # 12:Audio Book
            if "read book" in self.voice_data:
                self.Reader()

            # 13:Wikipedia
            if 'search wikipedia for' in self.voice_data:
                engine_speak("searching wikipedia...")
                p = self.voice_data.replace('search wikipedia for', '')
                info = wikipedia.summary(p, 1)
                engine_speak(info)
            elif 'who is' in self.voice_data:
                person = self.voice_data.replace('who is', '')
                info = wikipedia.summary(person, 1)
                engine_speak(info)

            # 14:How to
            elif "how to " in self.voice_data:
                engine_speak("getting data fom the internet!")
                op=self.voice_data.replace("explain me","")
                max_result=1
                how_to_func=search_wikihow(op,max_result)
                assert len(how_to_func)==1
                engine_speak(how_to_func[0].summary)

            # 15:Webbrowser
            # in the open method we just to give the link
            # of the website and it automatically open
            # it in your default browser

            # 15.1: Search google
            if "search for" in self.voice_data and 'youtube' not in self.voice_data:
                search_term = self.voice_data.split("for")[-1]
                url = "https://google.com/search?q=" + search_term
                webbrowser.get().open(url)
                engine_speak("Here is what I found for" + search_term + "  on google")
            elif "open google" in self.voice_data:
                engine_speak("what should i search on google")
                cm=self.record_audio().lower()
                engine_speak("This is what I found on the web! ")
                pywhatkit.search(cm)
                try:
                    r=wikipedia.summary(cm,2)
                    engine_speak(r)
                except:
                    engine_speak("No speakable Data Available!")

            # 15.2:Open gmail
            if "open my mail" in self.voice_data or "gmail" in self.voice_data:
                url="https://mail.google.com/mail/u/0/#inbox"
                webbrowser.get().open(url)
                engine_speak("here you can check your gmail")
            elif "email" in self.voice_data:
                try:
                    engine_speak("what should i say?")
                    content=self.record_audio()
                    to="kashyaokeshav644@gmail.com"
                    sendEmail(to,content)
                    engine_speak("Email has been sent to keshav")
                except Exception as e:
                    print(e)
                    engine_speak("sorry , iam not able to sent this mail to keshav")

            # 15.3: Search youtube
            if "search on youtube" in self.voice_data:
                search_term =self.voice_data.replace('search on youtube', '')
                search_term = self.voice_data.split("for")[-1]
                url = "https://www.youtube.com/results?search_query=" + search_term
                webbrowser.get().open(url)
                engine_speak("Here is what I found for " + search_term + " on youtube")
            elif "open youtube" in self.voice_data:
                webbrowser.open("www.youtube.com")
            elif 'play song on youtube' in self.voice_data:
                song = self.voice_data.replace('play song on youtube', '')
                engine_speak('playing ' + song)
                pywhatkit.playonyt(song)

            # 15.4:To find location using map
            elif "open map" in self.voice_data or"find location" in self.voice_data:
                location=self.record_audio("what is the location?")
                url='https://google.nl/maps/place/'+location+'/&amp;'
                webbrowser.get().open(url)
                engine_speak('here is the location of'  +location)

            # 15.5:Search online for music
            if "online music" in self.voice_data:
                search_term = self.voice_data.replace("play some online music like ", "")
                # search_term = self.voice_data.replace("play some online song like ", "")
                url = "https://open.spotify.com/search/" + search_term
                webbrowser.get().open(url)
                engine_speak("You are listening to  " + search_term + " enjoy ")

            # 15.6:Make a note
            if "make a note" in self.voice_data:
                url = "https://keep.google.com/#home"
                webbrowser.get().open(url)
                engine_speak("Here you can make notes")

            # 15.7:Open calendar
            if "calendar" in self.voice_data:
                url = "https://calendar.google.com/calendar/u/0/r?pli=1"
                webbrowser.get().open(url)
                engine_speak("Here you can check calendar")

            # 15.8:Open any website
            # 15.8.1:open facebook
            elif "open facebook" in self.voice_data:
                engine_speak("opening facebook")
                webbrowser.open("www.facebook.com")

            # 15.8.2:Open stack overflow
            elif "open stack overflow" in self.voice_data:
                engine_speak("opening stack over flow")
                webbrowser.open("www.stackoverflow.com")

            # 15.8.3:Open geeksforgeeks
            if "open geeks for geeks" in self.voice_data:
                engine_speak("Opening GeeksforGeeks ")
                webbrowser.open("www.geeksforgeeks.com")

            # 15.8.4:Open instagram
            if "open instagram" in self.voice_data:
                url = "https://www.instagram.com/"
                webbrowser.get().open(url)
                engine_speak("opening instagram")

            # 15.8.5:Open twitter
            if "open twitter" in self.voice_data:
                url = "https://twitter.com/"
                webbrowser.get().open(url)
                engine_speak("opening twitter")

            # Open any website
            elif 'website' in self.voice_data:
                engine_speak("tell me the name of the website!")
                name=self.record_audio().replace(" ","")
                name = self.record_audio().replace("open", "")
                web='https://www.'+name+'.com'
                webbrowser.open(web)
                engine_speak("okay,done")

            # Weather of your current location
            if "what is the weather condition outside" in self.voice_data:
                url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
                webbrowser.get().open(url)
                engine_speak("Here is what I found for on google")

            #Operation on system

            #System status
            if "system" in self.voice_data:
                sys_info = system_stats()
                print(sys_info)
                engine_speak(sys_info)

            #  Control system volume
            if "volume up" in self.voice_data:
                    engine_speak("okay,done")
                    pyautogui.press("volumeup")
            elif "volume down" in self.voice_data:
                    engine_speak("okay,done")
                    pyautogui.press("volumedown")
            elif "mute" in self.voice_data:
                    engine_speak("okay,done")
                    pyautogui.press("volumemute")

            # Check battery percentage
            elif "battery" in self.voice_data or "power" in self.voice_data:
                    battery = psutil.sensors_battery()
                    percentage = battery.percent
                    engine_speak(f"our system have {percentage} percent battery")

            # 16.4:Hide files in current folder
            elif "hide all files" in self.voice_data or "hide this folder" in self.voice_data:
                os.system("attrib +h /s /d")
                engine_speak("All the files in this folder are now hidden")

            # 16.5:Make files visible in current folder
            elif "visible" in self.voice_data or "make files visible" in self.voice_data:
                os.system("attrib -h /s /d")
                engine_speak("All the files in this folder are now visible to everyone. I hope you are taking this decision in your own peace")

            #16.6:To open applications
            # 16.6.1: Open notepad
            if "open notepad" in self.voice_data:
                engine_speak("opening notepad")
                npath="C:\\WINDOWS\\system32\\notepad.exe"
                os.startfile(npath)

            #Write this down in notepad
            elif "write this down" in self.voice_data:
                engine_speak("What would you like me to write down?")
                note_text = self.record_audio()
                note(note_text)
                engine_speak("I've made a note of that")

            # 16.6.2:Open downloads
            elif "open downloads" in self.voice_data:
                engine_speak("opening downloads")
                dpath="C:\\Users\\Admin\\Downloads"
                os.startfile(dpath)

            # 16.6.3:Open command prompt
            elif "open command prompt" in self.voice_data:
                engine_speak("opening command prompt")
                os.system("start cmd")

            # 16.6.4:Microsoft word
            elif "microsoft word" in self.voice_data:
                engine_speak("Opening Microsoft Word")
                os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office')

            #16.6.5:Open code editor
            elif 'open code editor' in self.voice_data :
                engine_speak("opening code editor")
                codePath = "C:\\Users\DELL\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code"  # that's the code path.
                os.startfile(codePath)

            # 17:Screenshot
            if "take a screenshot" in self.voice_data or "take screenshot" in self.voice_data:
                engine_speak("By what name do you want to save the screenshot?")
                name = self.record_audio()
                engine_speak("Alright, taking the screenshot")
                img = pyautogui.screenshot()
                name = f"{name}.png"
                img.save(name)
                engine_speak("The screenshot has been succesfully captured")

            elif "show me the screenshot" in self.voice_data or "show screenshot" in self.voice_data:
                try:
                    engine_speak("By what name did you save the screenshot?")
                    name = self.record_audio()
                    img = Image.open('.png')
                    img.show(img)
                    engine_speak("Here it is ")
                    time.sleep(2)

                except IOError:
                    engine_speak("Sorry, I am unable to display the screenshot")

            #18:To open camera
            elif "open camera" in self.voice_data:
                cap=cv2.VideoCapture(0)
                while True:#infinite loop
                    ret,img=cap.read()
                    cv2.imshow('webcam',img)
                    if cv2.waitKey(1)==13:#assci value of enter
                        break
                cv2.destroyAllWindows()
                cap.release()

            # 19:Take photo from camera
          

            # 20:Play some offline music
            elif "play some offline music" in self.voice_data or "play some offline song" in self.voice_data:
                engine_speak("here you go with music")
                music_dir="C:\\Users\\DELL\\Music"
                songs=os.listdir(music_dir)
                rd=random.choice(songs)
                print(songs)
                os.startfile(os.path.join(music_dir, rd))

            # 21:Switch the window
            elif "switch the window" in self.voice_data or "switch window" in self.voice_data:
                engine_speak("Okay, Switching the window")
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(10)
                pyautogui.keyUp("alt")

            # 22:Close any application
            elif 'close notepad' in self.voice_data :
                engine_speak("okay,closing notepad")
                os.system("taskkill /f /im notepad.exe ")

            elif 'close chrome' in self.voice_data :
                 engine_speak("okay,closing chrome ")
                 os.system("taskkill /f /im chrome.exe ")

            # 23:Send message to phone number
            if "send message" in self.voice_data:
                engine_speak("what should i say")
                msg = self.record_audio()
                account_sid = 'ACd855bb7f9f3a8bc87527bb869ae62721'
                auth_token = '4851f4353322fef89c1bb026fce5d3c8'
                client = Client(account_sid, auth_token)
                message = client.messages \
                    .create(
                    body=msg,
                    from_='+12039516534',  # both numbers should be verified
                    to='+91 8219397544'
                )
                engine_speak("okay,done")

            # 24:Make call
            if "make call" in self.voice_data:
                account_sid = 'ACd855bb7f9f3a8bc87527bb869ae62721'
                auth_token = '4851f4353322fef89c1bb026fce5d3c8'
                client = Client(account_sid, auth_token)
                call = client.calls.create(
                    twiml='<Response><Say>this is the second testing message from AVVA </Say></Response>',
                    to='+918219397544',
                    from_='+12039516534',
                )
                engine_speak("okay,done")

            #25:Send whatsApp message
            if "whats app" in self.voice_data or "whatsapp" in self.voice_data:
                engine_speak("tell me the name of the person!")
                name=self.record_audio()
                if "type name" in name:
                    engine_speak("tell me the message!")
                    msg=self.record_audio()
                    engine_speak("tell me the time!" )
                    engine_speak("time in hour!")
                    hour=int(self.record_audio())
                    engine_speak("time in minutes!")
                    min= int(self.record_audio())
                    pywhatkit.sendwhatmsg('8219397544', msg, hour, min,20)
                    engine_speak("okay,sending whatsapp message! ")

                else:
                    try:
                        engine_speak("tell me the phone number!")
                        phone=str(self.record_audio())
                        ph='+91'+phone
                        engine_speak("tell me the message!")
                        msg = self.record_audio()
                        engine_speak("tell me the time!")
                        engine_speak("time in hour!")
                        hour = int(self.record_audio())
                        engine_speak("time in minutes!")
                        min = int(self.record_audio())

                        pywhatkit.sendwhatmsg(ph, msg, hour, min, 20)
                        engine_speak("okay,sending whatsapp message! ")

                    except pywhatkit.mainfunctions.CountryCodeException: # error: recognizer does not understand
                        engine_speak("Sorry! I didn\'t get that. please type the phone number!")
                        phone= str(input())
                        engine_speak("tell me the message!")
                        msg = self.record_audio()
                        engine_speak("tell me the time!")
                        engine_speak("time in hour!")
                        hour = int(self.record_audio())
                        engine_speak("time in minutes!")
                        min = int(self.record_audio())
                        pywhatkit.sendwhatmsg(phone, msg, hour, min, 20)
                        engine_speak("okay,sending whatsapp message! ")

            # 26:Stone paper scissors
            if "game" in self.voice_data:
                    self.voice_data = self.record_audio("choose among rock paper or scissor")
                    moves = ["rock", "paper", "scissor"]
                    cmove = random.choice(moves)
                    pmove = self.voice_data
                    engine_speak("The computer chose " + cmove)
                    engine_speak("You chose " + pmove)
                    if pmove == cmove:
                        engine_speak("the match is draw")
                    elif pmove == "rock" and cmove == "scissor":
                        engine_speak("you wins")
                    elif pmove == "rock" and cmove == "paper":
                        engine_speak("Computer wins")
                    elif pmove == "paper" and cmove == "rock":
                        engine_speak("you wins")
                    elif pmove == "paper" and cmove == "scissor":
                        engine_speak("Computer wins")
                    elif pmove == "scissor" and cmove == "paper":
                        engine_speak("you wins")
                    elif pmove == "scissor" and cmove == "rock":
                        engine_speak("Computer wins")

            #  27:Toss a coin
            if "toss a coin" in self.voice_data:
                    moves = ["head", "tails"]
                    cmove = random.choice(moves)
                    engine_speak("The computer chose " + cmove)

            # 28: Calculator
            elif "calculator" in self.voice_data:
               ou= self.record_audio()
               inp=ou.lower()
               app_id = 'H4PXTG-V87PJYR7X3'
               client = wolframalpha.Client(app_id)
               res = client.query(inp)
               answer = next(res.results).text
               engine_speak(f"answer is:{ answer} ")

            # 29:Time & day
            if "current time" in self.voice_data:
                            times = datetime.datetime.now().strftime('%I:%M %p')
                            engine_speak('Current time is ' + times)
            elif "day" in self.voice_data:
                tellDay()

            # Take the photo from camera
            elif "selfie" in self.voice_data :
                engine_speak("be ready, i am going to take your photo ")
                camera = cv2.VideoCapture(0)
                check,frame=camera.read()
                cv2.waitKey(100)
                cv2.destroyAllWindows()
                showPic = cv2.imwrite("Capture(2).jpg",frame)
                camera.release()

            #30:Time table
            if "show my time table" in self.voice_data:
                im = Image.open("time table.jpg")
                im.show()

            # 31:Joke
            elif 'joke' in self.voice_data:
                engine_speak(pyjokes.get_joke())
            elif 'party' in self.voice_data:
                engine_speak('sorry, I have a headache')
            elif 'are you single' in self.voice_data:
                engine_speak('I am in a relationship with wifi')

            # 32:To exit
            g=["you need a break","exit", "quit", "goodbye", "stop","rest"]
            if self.voice_data in g:
               engine_speak("thanks for using me ,i am going offline. It was nice working with you , have a good day")
               exit()



# Creating Instance Object for MainThread class
startExecution=MainThread()

#The QMainWindow class provides a main application window
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_AVVA ()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie=QtGui.QMovie("7LP8.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("gif3.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("small.gif")
        self.ui.label_5.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("gif1.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("images.jpeg")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("new.gif")
        self.ui.label_6.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("images.jpeg")
        self.ui.label_8.setMovie(self.ui.movie)
        self.ui.movie.start()
        wish()
        timer=QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()
    def showTime(self):
        current_time=QTime.currentTime()
        current_date=QDate.currentDate()
        label_time=current_time.toString('hh:mm:ss')
        label_date=current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)
    def __init__(self):
        super().__init__()
        self.ui=Ui_AVVA()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
app=QApplication(sys.argv)
avva=Main()
avva.show()
exit(app.exec_())




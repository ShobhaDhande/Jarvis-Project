import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import datetime
import pyjokes
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialisation of pyttsx3
engine = pyttsx3.init()

#Set the speaking rate of the jarvis..
engine.setProperty('rate', 120)
# contact list with name and email.
email_list = {'name of email holder':'email'}
credential = {}

def speak(audio):
    """
    This function is use to speak the query and results.
    """
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """
        A basic wish me fuction which will greet us as per the current time.
    """
    a = int(datetime.datetime.now().hour)
    if a>=0 and a<12:
        speak("Good Morning!")
    elif a>=12 and a<18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    

def weather_report(state):
    """
        This function will take name of place as an argument and speak the current weather of the place as per the open weather forcast.
        It will speak 'data is not available' if the place is not register in open weather.
    """
    key = "Enter your open weather api key here"
    url = "https://api.openweathermap.org/data/2.5/weather?"
    q = {
            "q":f"{state}",
            "appid":key,
            "units":"metric"
            }
    d = requests.get(url,params=q)
    if d.status_code == 200:
        data = d.json()
        speak(f"Temperature in {state} is {data['main']['temp']} degree celcius.")
        
    else:
        speak('Data is not available.')

def command():
    """
    This function will listen user command and then recognize the voice and convert the voice into text and then return a string.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        audio = recognizer.listen(source)
    print(audio)
    
    try:
        print("Recognizing......")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query
    except:
        speak("unable to recognise your voice please speak again..")
        return command()

def user_credential():
    """
    This  Function is use for user login or for saving the new user credentials.
    """
    speak("would you like to login or use it as guest..")
    query = command().lower()
    if "guest" in query:
        speak("You are using this device as a guest. You won't be able to use credential related features.")
    else:
        speak("Would you like to login or new user..")
        query = command().lower()
        if "new" in query:
            speak("Your name..")
            name = command().lower()
            speak("Email..")
            email = command()
            speak("Password..")
            password = command()
            email_list[name] = email
            credential[name] = password
        else:
            speak("Your name..")
            name = command().lower()
            speak("Password..")
            password = command()
            if name in credential.keys() and password in credential.values():
                    speak("login successfully..")


def send_email():
    """
    This function is used for sending mail.

    """
    msg = MIMEMultipart()
    msg["From"] = "shobhadhande11@gmail.com"
    speak("whom you want to send email ?")
    email_name = command().lower().strip()
    email = email_list[email_name]
    msg["To"] = email
    speak("Subject of your email..")
    sub = command()
    msg["Subject"] = sub
    speak("Body of your email....")
    body = command()
    msg.attach(MIMEText(body,'Plain'))
    s = smtplib.SMTP("smtp.gmail.com",587)
    s.starttls()
    s.login("shobhadhande11@gmail.com","Piemr#2019")
    text = msg.as_string()
    speak(f"sending email to {email_name}..")
    s.sendmail("shobhadhande11@gmail.com",email,text)
    s.quit()
    speak(f"Mail sent successfully to {email_name}")

if __name__ =="__main__":

    """
        This module can be used as jarvis or alexa. Which will take command from user and perform task accordingly.
        
    """
    question = {"what can you do":"I can serach your query on wikipedia, i can open Youtube, i can open google, i can tell you the current time,\
                i can send email for you if are a registered user, i can also open whatsapp web for you, i can make you laugh with few jocks,\
                    i can tell you the current temperature, i can write notes for you as well and few more things. ",
                "who are you":"I am your virtual assistant created by Shobha and Aditi"}
    print(question.keys())
    wishMe()
    # user_credential()
    speak("How can i help you sir!")
    while True:
        query = command().lower()
    
        if "wikipedia" in query:
            speak("Searching wikipedia....")
            query=query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=10)
            print(results)
            speak("According to wikipediya...")
            speak(results)

        elif "send email" in query:
            send_email()

        elif "open google" in query:
                speak("Opening Google")
                webbrowser.open("https://google.com")

        elif "open youtube" in query:
            speak("opening youtube")
            webbrowser.open("https://www.youtube.com/")

        elif "open whatsapp" in query:
            speak("opening whatsapp")
            webbrowser.open("https://web.whatsapp.com/")

        elif "the time" in query:
            Time = datetime.datetime.now().strftime("%H:%M:%S")
            
            speak(f"Time is {Time}")

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you?")

        elif 'fine' in query or "good" in query:
            speak("It's good to know that your fine")

        elif 'joke' in query:
                speak(pyjokes.get_joke())

        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.nl / maps / place/" + location + "")

        elif 'play music' in query or "play song" in query:
            speak("Here you go with music")
            music_dir = "Enter your playlist path here..."
            songs = os.listdir(music_dir)
            print(songs)   
            random = os.startfile(os.path.join(music_dir, songs[1]))


        elif "write a note" in query:
            speak("What should i write, sir")
            note = command()
            speak("What is the name for file")
            name = command()
            file = open(f'{name}.txt', 'w')
            file.write(note)
         
        elif "show note" in query:
            speak("Showing Notes")
            file = open(f"{name}.txt", "r")
            print(file.read())
            speak(file.read(6))
        
        elif "temperature" in query:
            speak('Please speak the place name.')
            weather_report(command())


        elif query in question.keys():
            print(query)
            print("*"*90)
            print(question[query])
            print("*"*90)
            speak(question[query])
 
        elif "thank you" in query:
            speak("okay! You can call me any time you need.")
            break
    
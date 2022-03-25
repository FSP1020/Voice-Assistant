import speech_recognition as sr
import time
import pyttsx3 
from num2words import num2words
from applemusic import AppleMusic
from bs4 import BeautifulSoup
import requests
import wikipedia
from word2number import w2n
from whiteCalculator import Calculator
import pyjokes


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Initialize
engine = pyttsx3.init() 


def get_response():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for background noise. One second")
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)
        print("Finished listening")

    IBM_USERNAME = "apikey"  
    IBM_PASSWORD = "dXap846U8DZUiY40WHU3HtQ8xuPMPPJBRlCN6PLJ4CLt"  # IBM Speech to Text apikey
    try:
        # print("IBM Speech to Text thinks you said " + r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD))
        result = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
        print(result)
    except sr.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
        speak("Please try again. I could not understand you.")
        ask_me()
    except sr.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))
    return result

def speak(result):
    print(result)

    # convert text to speech 
    engine.say(result) 
    engine.runAndWait()

def ask_me():
    end = False

    # Get first response.
    result = get_response()
    # result = input("Enter request... ")

    # What time is it?
    if "time" in result:
        t = time.asctime(time.localtime(time.time()))
        the_time = t.split()
        the_time = the_time[3]
        the_time = the_time.split(':')
        hour = int(the_time[0])
        minute = int(the_time[1])
        minute = num2words(minute)
        if hour > 12:
            hour -= 12
            minute += " PM. Have a good evening!"
        else:
            minute += " AM. Have a good day!"
        hour = num2words(hour)
        speak("The time is " + hour + " " + minute + ".")

    # Hello and introduction
    elif "hello" in result or "hi" in result:
        speak("Hello there human! What's your name?")

        result = get_response()
        # result = input("Enter request.. ")

        speak("Hello " + result + ".")
        speak("Can I help you with anything?")
        result = get_response()
        # result = input("Enter request.. ")
        if "yes" in result:
            speak("What can I help you with?")
            ask_me()
        else:
            speak("Okay, let me know if you need anything. Bye.")
            end = True

    # What is the weather?
    elif "weather" in result or "temperature" in result:
        city = "Galveston"
        city = city + " weather"
        location, info, temp = weather(city)
        speak("In " + location + ", it is " + info + " and " + temp + ".")
        speak("Have a great rest of your day!")

    # Play music
    elif "play" in result:
        speak("I am playing a song. Doo Daa. Doo daa.")

    # Tell a joke
    elif "joke" in result:
        joke = pyjokes.get_joke()
        speak(joke)

    # Search Wiki
    elif "wikipedia" in result:
        # search = input('What should we search for?  ')
        speak('What should we search for?')
        search = get_response()
        speak(wikipedia.summary(search, auto_suggest=False))

    # Calculator
    elif "calculate" in result:
        speak("What do you need to calculate?")
        c = Calculator()

        string = get_response()
        # string = input('What is your expression?  ')
        str_list = string.split()
        string = ""

        for element in str_list:
            # print(element)
            if element == "plus" or element == "+":
                element = "+"
            elif element == "times"  or element == "*" or element == "multiplied":
                element = "*"
            elif element == "minus"  or element == "-":
                element = "-"
            elif element == "divided"  or element == "/":
                element = "/"
            elif element == "by":
                element = ""
            else:
                element = w2n.word_to_num(element)
                element = str(element)
            string += element
        # print(str)

        speak(c.run(string))

    # Random Questions

    elif "who created you" in result or "who made you in result":
        speak("I was given life by the Great Sam Pomajevich.")

    elif "what is your name" in result or "what's your name" in result or "who are you" in result:
        speak("My name is Robo nice to meet you!")

    elif "I love you" in result:
        speak("Thank you, that's nice.")
    

    else:
        speak(result)


    # Anything else to ask?
    if not end:
        speak("Can I help you with anything else?")
        result = get_response()
        # result = input("enter request.. ")
        if "yes" in result:
            speak("What can I help you with?")
            ask_me()
        else:
            speak("Okay, let me know if you need anything. Bye.")

# Web scrape for weather.
def weather(city):
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    # print("Searching...\n")
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    print(location)
    print(time)
    print(info)
    weather = weather + " degrees Fahrenheit"
    print(weather + "\n")
    return location, info, weather

# Activate assistant
ask_me()

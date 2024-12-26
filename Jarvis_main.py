import datetime
import os
import pyttsx3
import speech_recognition
import requests
import openai  # Make sure you have installed the OpenAI Python package
from bs4 import BeautifulSoup
import pyautogui

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

# Function to speak text
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to take voice commands
def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)
    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query

# Function to get temperature for a given location using WeatherAPI
def get_temperature(location):
    api_key = "bc8c2e3c4007484695c64927240711"  # Replace with your actual WeatherAPI key
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=no"
    try:
        response = requests.get(url)
        data = response.json()
        if "error" not in data:
            temp = data["current"]["temp_c"]
            return f"The current temperature in {location} is {temp}°C."
        else:
            return "Location not found. Please try again."
    except Exception as e:
        print(f"Error: {e}")
        return "Unable to retrieve temperature due to an error."

# **ChatGPT API Integration**
OPENAI_API_KEY = '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'  # Replace with your actual OpenAI API key

# Function to get a response from ChatGPT
def get_chatgpt_response(question):
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("Request error:", e)
        return "Unable to reach ChatGPT API."

# Function to search with ChatGPT for definitions or explanations
def searchChatGPT(query):
    speak("Let me find that for you.")
    response = get_chatgpt_response(query)
    speak(response)
    print(response)

if __name__ == "__main__":
    while True:
        query = takeCommand().lower()
        if "hello" in query:
            from GreetMe import greetMe
            greetMe()

            while True:
                query = takeCommand().lower()
                if "bye" in query:
                    speak("Ok sir, you can call me anytime")
                    break
                elif "hello" in query:
                    speak("Hello sir, how are you?")
                elif "i am fine" in query:
                    speak("That's great, sir")
                elif "how are you" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("You are welcome, sir")

                elif "open" in query:
                    from Dictapp import openappweb
                    openappweb(query)
                elif "close" in query:
                    from Dictapp import closeappweb
                    closeappweb(query)

                elif "google" in query:
                    from SearchNow import searchGoogle
                    searchGoogle(query)
                elif "youtube" in query:
                    from SearchNow import searchYoutube
                    searchYoutube(query)
                elif "wikipedia" in query or "what" in query:
                    from SearchNow import searchWikipedia
                    searchWikipedia(query)
                elif "temperature" in query or "weather" in query:
                    speak("Please tell me the location")
                    location = takeCommand().lower()
                    if location != "none":
                        temp = get_temperature(location)
                        speak(temp)
                    else:
                        speak("Sorry, I didn't catch the location.")

                elif "time" in query:
                    strTime = datetime.datetime.now().strftime("%I:%M %p")
                    speak(f"Sir, the time is {strTime}")

                elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif "play" in query:
                    pyautogui.press("k")
                    speak("video played")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")

                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up, sir")
                    volumeup()
                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, sir")
                    volumedown()

                elif "set an alarm" in query:
                    print("input time example:- 10 and 10 and 10")
                    speak("Set the time")
                    a = input("Please tell the time :- ")
                    alarm(a)
                    speak("Done, sir")

                elif "search" in query or "define" in query or "explain" in query:
                    speak("What would you like me to find?")
                    topic = takeCommand().lower()
                    if topic != "none":
                        searchChatGPT(topic)
                    else:
                        speak("Sorry, I didn't catch that topic.")

                elif "exit" in query:
                    speak("Thank you, bye, sir")
                    exit()
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that", "")
                    rememberMessage = query.replace("jarvis", "")
                    speak("You told me to remember that" + rememberMessage)
                    with open("Remember.txt", "a") as remember:
                        remember.write(rememberMessage)
                elif "what do you remember" in query:
                    with open("Remember.txt", "r") as remember:
                        speak("You told me " + remember.read())
                elif "question" in query or "ask" in query:
                    speak("What is your question?")
                    question = takeCommand().lower()
                    if question != "none":
                        response = get_chatgpt_response(question)
                        speak(response)
                    else:
                        speak("Sorry, I didn't catch your question.")

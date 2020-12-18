# Description: A Virtual Assistant program that gets the current date and time, responds back with a random greeting

import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

# ignore any warning messages
warnings.filterwarnings('ignore')


# Record Audio and return it as a string

def recordAudio():
    # Record the Audio
    r = sr.Recognizer()

    # open the microphone and start recording
    with sr.Microphone() as source:
        print('Ramesh is ready! \U0001f600')
        audio = r.listen(source)

    # Use Google speech recognition
    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: ' + data)
    except sr.UnknownValueError:  # Check for Unknown Errors
        print('Google Speech Recognition could not understand the audio, unknown error')
    except sr.RequestError as e:
        print('Request results from Google Speech Recognition service error ' + e)

    return data


# A function to get a response

def assistantResponse(text):
    print(text)

    myobj = gTTS(text=text, lang='en', slow=False)
    myobj.save("assistant_response.mp3")
    os.system('cvlc assistant_response.mp3 --play-and-exit')

#A function for wake words

def wakeWords(text):
    WAKE_WORDS = ['hey ramesh','okay ramesh', 'hi ramesh','ramesh']

    text = text.lower()

    for var in WAKE_WORDS:
        if var in text:
            return True

    return False

# A function for Current date

def getDate():

    now = datetime.datetime.now()
    my_date = datetime.datetime.today()

    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']

    if dayNum in range(4,20) or range(24,32):
        out = 'Today is {} {} the {}th'.format(weekday,months[monthNum - 1],dayNum)

    elif dayNum == 21:
        out = 'Today is {} {} the {}st'.format(weekday, months[monthNum - 1], dayNum)

    elif dayNum == 22:
        out = 'Today is {} {} the {}nd'.format(weekday, months[monthNum - 1], dayNum)

    elif dayNum == 23:
        out = 'Today is {} {} the {}rd'.format(weekday, months[monthNum - 1], dayNum)

    elif dayNum == 1:
        out = 'Today is {} {} the First'.format(weekday, months[monthNum - 1])

    elif dayNum == 2:
        out = 'Today is {} {} the Second'.format(weekday, months[monthNum - 1])

    elif dayNum == 3:
        out = 'Today is {} {} the Third'.format(weekday, months[monthNum - 1])

    return out

# A function to return a random greeting response

def greeting(text):

    Greeting_Input = ['hi', 'hey', 'greetings', 'wassup', 'what is up', 'namaste', 'hello']

    Greeting_Response = ['howdy','whats good', 'hello', 'namaste']

    for word in text.split():
        if word.lower() in Greeting_Input:
            return random.choice(Greeting_Response) + '.'

    return ''

#A Function to get the first and last name from a text

def getPerson(text):

    wordList = text.split()

    for var in range(0,len(wordList)):
        if var+3 <= len(wordList) and wordList[var].lower() == 'who' and wordList[var+1].lower() == 'is':
            return wordList[var+2] + '' + wordList[var+3]

# A Function to get todays weekday
def getDay(text):

    from dateparser.search import search_dates
    day = search_dates(text)

    day1 = day[0][1].weekday()

    out1 = day[0][0]
    out2 = calendar.day_name[day1]

    return '{} is {}'.format(out1, out2)


while True:

    text = recordAudio()
    response = ''

    if(wakeWords(text) is True):

        #Check for greeting:
        response = response + greeting(text)

        #Check for date
        if('date' in text.lower()):
            getdate = getDate()
            response = response + '' + getdate

        #check for person
        if('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)
            response = response + '' + wiki

        #Check for day
        if('day' in text.lower()):
            day1 = getDay(text)
            response = response + '' + day1


        assistantResponse(response)

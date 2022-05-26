import json
from select import select 
import numpy as np
from tensorflow import keras
import re
import streamlit as s
from streamlit_chat import message
from streamlit_option_menu import option_menu
import random
import pickle
import string
import yfinance as yf
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from difflib import SequenceMatcher
with open('Intent.json') as file:
    data = json.load(file)
    select = option_menu(
        menu_title= "Othmane's ChatBot",
        options= ["About", "Start Chating"],
        icons=["house", "chat-dots-fill"],
        menu_icon= "line",
        default_index=0,
        orientation= "horizontal",
    )
if select == "About":
    s.title("About")
    s.subheader("Please read this description: ")
    txt = s.text_area('Othmane: ', '''
     Hi, my name is Othmane and I am happy to have you here. 
     This application is a user friendly AI Chatbot for entertainment purposes. You can enjoy a basic conversation about various topics.
     It is excellent at doing 3 main things: 
      1- Telling Jokes: You can ask the bot to tell you jokes or something funny.
      2- Playing riddles: If you like riddles, you are well served with this chatbot. You only need to ask for a riddle and do your best guessing the answer.
      3- Reporting live stock market data: For investment lovers, you can simply ask the chatbot for stock market data and it will provide you with what you are looking for including a buy/sell advice.
      This chatbot can also have basic conversation about daily life matters on a variety of topics, you can ask the chatbot information about itself, and enjoy an entertaining conversation. 
      Eventually, I hope you like it and have a joyful experience!.
     ''', height= 400, disabled= True)
    '''Project Github: [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/MagiOne07/Chatbot) My LinkedIn: [![Repo](https://badgen.net/badge/icon/linkedIn?icon=linkedIn&label)](https://www.linkedin.com/in/othmane-ayay-140687168/) My Instagram: [![Repo](https://badgen.net/badge/icon/Instagram?icon=Instagram&label)](https://www.instagram.com/othmane.ayay/?hl=en)'''
    s.markdown("<br>",unsafe_allow_html=True)
elif select == "Start Chating":
    def clean_text(txt):
            txt = txt.lower()
            txt = re.sub(r"i'm", "i am", txt)
            txt = re.sub(r"he's", "he is", txt)
            txt = re.sub(r"she's", "she is", txt)
            txt = re.sub(r"that's", "that is", txt)
            txt = re.sub(r"what's", "what is", txt)
            txt = re.sub(r"where's", "where is", txt)
            txt = re.sub(r"\'ll", " will", txt)
            txt = re.sub(r"\'ve", " have", txt)
            txt = re.sub(r"\'re", " are", txt)
            txt = re.sub(r"\'d", " would", txt)
            txt = re.sub(r"won't", "will not", txt)
            txt = re.sub(r"can't", "can not", txt)
            txt = re.sub(r"[^\w\s]", "", txt)
            return txt
    new_words = {
        'crushes': 10,
        'beats': 5,
        'beat': 5,
        'misses': -5,
        'misse': -5,
        'trouble': -10,
        'falls': -100,
        'fall': -100,
        'drops': -50,
        'drop': -50,
        'rise': 20,
        'rises': 20,
        'slip': -20,
        'slips': -20,
        'down':-20,
        'jump':20,
        'jumps':20
    }
    vader = SentimentIntensityAnalyzer()
    vader.lexicon.update(new_words)
    def get_random_string(length):
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(length))
            return result_str
    def chat():
        placeholder = s.empty()
        model = keras.models.load_model('chat_model.h5')

        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        with open('label_encoder.pickle', 'rb') as enc:
            lbl_encoder = pickle.load(enc)

        max_len = 20
        
        if "history" not in s.session_state:
            s.session_state.history = []
        
        if "status" not in s.session_state:
            s.session_state.status= False
        if "st" not in s.session_state:
            s.session_state.st = False  
        if "check" not in s.session_state:
            s.session_state.check = ['random']
        if "stock" not in s.session_state:
            s.session_state.stock = False 
        if len(s.session_state.history)>3:
            s.session_state.history = s.session_state.history[-3:]
        inp = s.text_input('User', key='text')
        inp = clean_text(inp)
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])
        answers = ['future', 'age', 'towel', 'seven', "potato", "comb", "needle", "g", "legs", "nothing", "name", "nine", "queue", "silence","egg", "car","jared", "piano","echo","map","r","water","home","shadow","redemption"]
        if inp:
            if s.session_state.status == True:
                if inp == "yes":
                    for i in data['intents']:
                        if i['tag'] == 'joke':
                            v=np.random.choice(i['responses']) + "\U0001F923 \U0001F923 \U0001F923 \n Do you want to hear another one? yes/no."
                    s.session_state.status=True
                else:
                    v='Aright'
                    s.session_state.status=False
                s.session_state.history.append({"message": inp, "is_user": True})
                s.session_state.history.append({"message": v, "is_user": False})
                with placeholder.container():
                    for chat in s.session_state.history:
                        message(**chat, key=get_random_string(8))
            elif s.session_state.st == True:
                if SequenceMatcher(a=s.session_state.check[-1],b=inp).ratio() >0.5:
                    v='Very Good, It is correct \U0001f600'
                    s.session_state.st = False
                else:
                    v='Not correct \U0001f60F the answer is: '+ s.session_state.check[-1] + ' if you want another one say riddle'
                    s.session_state.st = False
                s.session_state.history.append({"message": inp, "is_user": True})
                s.session_state.history.append({"message": v, "is_user": False})
                with placeholder.container():
                    for chat in s.session_state.history:
                        message(**chat, key=get_random_string(8))
            elif s.session_state.stock == True:
                if inp != "stop":
                    actual = yf.download(tickers=inp, period='1m',prepost=True)
                    actual=actual['Close']
                    actual = actual.to_numpy()
                    chart = yf.download(tickers=inp, period='30d',prepost=True)
                    headline = yf.Ticker(inp)
                    headline=headline.news
                    news=[]
                    for head in headline:
                        news.append(head['title'])
                    news= np.array([vader.polarity_scores(i)['compound'] for i in news]).mean()
                    if news>0.5:
                        news="strongly positive. My tip is to Buy."
                    elif news<-0.5:
                        news= "strongly negative. My tip is to Sell."
                    elif news >0:
                        news= "positive. You might want to Buy, but if I were you I would wait until more convincing news come out."
                    elif news<0:
                        news= "negative. You might want to Sell, but if I were you I would wait until more convincing news come out."
                    try:
                        actual = actual[0]
                        v = "The Price is:"+ str(actual) + " If you don't want to explore more stocks say stop."
                        s.session_state.history.append({"message": inp, "is_user": True})
                        s.session_state.history.append({"message": v, "is_user": False})
                        with placeholder.container():
                            for chat in s.session_state.history:
                                message(**chat, key=get_random_string(8))
                                if chat == s.session_state.history[len(s.session_state.history)-1]:
                                    a=s.line_chart(chart)
                                    b = s.write('The news sentiment of ' + inp  + ' are : ', news)
                                    del(a,b, news, chart, actual)
                    except:
                        v= "Please enter a correct symbol ticker or say stop to end. For exmaple, Apple is AAPL."
                        s.session_state.history.append({"message": inp, "is_user": True})
                        s.session_state.history.append({"message": v, "is_user": False})
                        with placeholder.container():
                            for chat in s.session_state.history:
                                message(**chat, key=get_random_string(8))
                else:
                    v= "Okay!"
                    s.session_state.history.append({"message": inp, "is_user": True})
                    s.session_state.history.append({"message": v, "is_user": False})
                    with placeholder.container():
                        for chat in s.session_state.history:
                            message(**chat, key=get_random_string(8))
                    s.session_state.stock = False
                        
            else:
                for i in data['intents']:
                        if i['tag'] == tag and tag=='joke':
                            v=np.random.choice(i['responses']) + " \U0001F923 \U0001F923 \U0001F923 \n Do you want to hear another one? yes/no."
                            s.session_state.status=True
                            s.session_state.history.append({"message": inp, "is_user": True})
                            s.session_state.history.append({"message": v, "is_user": False})
                            with placeholder.container():
                                for chat in s.session_state.history:
                                    message(**chat, key=get_random_string(8))
                        elif i['tag'] == tag and tag=='riddle':
                            v=np.random.choice(i['responses'])
                            for a in range(25):
                                if v == i['responses'][a]:
                                    s.session_state.check.append(answers[a])
                            s.session_state.st = True
                            s.session_state.history.append({"message": inp, "is_user": True})
                            s.session_state.history.append({"message": v, "is_user": False})
                            with placeholder.container():
                                for chat in s.session_state.history:
                                    message(**chat, key=get_random_string(8))
                        elif i['tag'] == tag and tag=='stock':
                            v = np.random.choice(i['responses']) 
                            s.session_state.stock = True
                            s.session_state.history.append({"message": inp, "is_user": True})
                            s.session_state.history.append({"message": v, "is_user": False})
                            with placeholder.container():
                                for chat in s.session_state.history:
                                    message(**chat, key=get_random_string(8))
                        elif i['tag'] == tag:
                            v=np.random.choice(i['responses'])
                            s.session_state.history.append({"message": inp, "is_user": True})
                            s.session_state.history.append({"message": v, "is_user": False})
                            with placeholder.container():
                                for chat in s.session_state.history:
                                    message(**chat, key=get_random_string(8))
        del(max_len, inp, v,tag ,result)
    s.write('ChatBot: I am Othmane your bot companion. We can enjoy a conversation, I can tell you jokes, play riddles and feed you with stock market data. Tell me what you want to do?')
    chat()
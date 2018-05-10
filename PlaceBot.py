# -*- coding: utf-8 -*-

import telepot
import telegram
import requests
import json
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

bot = telepot.Bot('488891276:AAEHJhT5HRoV1znvYnHjCp4pb8S2QSvOmKo')

def enviarLocalizacao():
    list_buttons = [
        [
            KeyboardButton(text='Enviar Localização', request_location = True)
        ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=list_buttons, resize_keyboard=True, one_time_keyboard=True)
    return reply_markup

def escolheEstabelecimento():
    list_buttons = [
       [
            KeyboardButton(text='Restaurante'),
            KeyboardButton(text='Hotel'),
            KeyboardButton(text='Mercado'),
            KeyboardButton(text='Pub')
       ]
    ]

    
    reply_markup = ReplyKeyboardMarkup(keyboard=list_buttons, resize_keyboard=True, one_time_keyboard=True)
    return reply_markup


def mandaLocais (userID, x, data):
    bot.sendMessage(userID,data['response']['groups'][0]['items'][x]['venue']['name'].encode(encoding='UTF-8',errors='strict'))
    if data['response']['groups'][0]['items'][x]['venue']['location']:
        if data['response']['groups'][0]['items'][x]['venue']['location']['formattedAddress']:
            for y in range(0, len(data['response']['groups'][0]['items'][x]['venue']['location']['formattedAddress'])):
                bot.sendMessage(userID,data['response']['groups'][0]['items'][x]['venue']['location']['formattedAddress'][y].encode(encoding='UTF-8',errors='strict'))
    bot.sendMessage(userID, '------')
                   
        
def localiza(message):
    
    tipoMsg, tipoChat, userID = telepot.glance(message)
    global categoria
    if tipoMsg == "text":
        if message['text'] == '/start':
            bot.sendMessage(userID, 'Bem vindo')
            reply_markup = escolheEstabelecimento()
            bot.sendMessage(userID, 'O que procura?', reply_markup=reply_markup)      
        else:
            if message['text'] == 'Restaurante':
                categoria = 'restaurant'
            if message['text'] == 'Hotel':
                categoria = 'hotel'
            if message['text'] == 'Mercado':
                categoria = 'supermarket'
            if message['text'] == 'Pub':
                categoria = 'pub'
                
            reply_markup = enviarLocalizacao()
            
            bot.sendMessage(userID, 'Enviar Localizaçao', reply_markup=reply_markup)
    if(tipoMsg == "location"):
        lat = message['location']['latitude']
        lon = message['location']['longitude']
        #Faz requisiçao na API
        latlon = str(lat)+','+str(lon)
        api_url = 'https://api.foursquare.com/v2/venues/explore'
        params = {'client_id': 'WJCBZKPRLMVOR51PALKM3JOUH2EKTW154YHXGGTKLGWLCH01',
                  'client_secret': 'CAKZAZQIPOKGPGZOCNTMMPLBAUBHDS4K5PBBHPCVYLGLMMO2',
                  'v': '20120609',
                  'll': latlon,
                  'radius': 25000,
                  'query': categoria,
                  'limit': 3}
        resp = requests.get(api_url, params)
        data = json.loads(resp.text)

        nome = []
        endereco = []
        if data['response']['groups'][0]['items']:
            for x in range(0, 3):
                mandaLocais(userID, x, data)          
        else:
            bot.sendMessage(userID, 'Nao há locais perto de você! Sinto muito.')     

bot.message_loop(localiza)
while True:
    pass

import json
import os
import discord
from config import settings

#os.chdir('/home/peoples/discord-bot')

def parse_city_json(json_file='russia.json'):
    content = {}
    p_obj = None
    try:
        js_obj = open(json_file, "r", encoding="utf-8")
        p_obj = json.load(js_obj)
    except Exception as err:
        print(err)
        return None
    finally:
        js_obj.close()   
    return [city['city'].lower() for city in p_obj]

def get_city(city):
    normilize_city = city.strip().lower()[1:]
    if is_correct_city_name(normilize_city):
        if get_city.previous_city != "" and normilize_city[0] != get_city.previous_city[-1]:
            return 'Город должен начинаться на "{0}"!'.format(get_city.previous_city[-1])

        if normilize_city not in cities_already_named:
            cities_already_named.add(normilize_city)
            last_latter_city = normilize_city[-1]
            proposed_names = list(filter(lambda x: x[0] == last_latter_city, cities))
            if proposed_names:
                for city in proposed_names:
                    if city not in cities_already_named:
                        cities_already_named.add(city)
                        get_city.previous_city = city
                        return city.capitalize()
            return 'Я не знаю города на эту букву. Ты выиграл'
        else:
            return 'Город уже был. Повторите попытку'
    else:
        return 'Некорректное название города. Повторите попытку'

get_city.previous_city = "" 

def is_correct_city_name(city):
    return city[-1].isalpha() and city[-1] not in ('ь', 'ъ')

def refresh():
    cities = parse_city_json()[:1000]
    cities_already_named = set()
    
cities = parse_city_json()[:1000]  # города которые знает бот
cities_already_named = set()  # города, которые уже называли

TOKEN = settings['token']

bot = discord.Client()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!'):
        if message.content == '!refresh':
            refresh()
        else:
            response = get_city(message.content)
            await message.channel.send(response)

bot.run(TOKEN)





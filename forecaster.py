# Code for the weather forecaster discord bot
import os
import discord
import requests
from dotenv import load_dotenv

#code for connecting the bot to discord
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord.')

@client.event
async def on_message(message):
    print(message)
    if message.author == client.user:
        return

    m_list = message.content.split(' ', 1)
    command = m_list[0]
    #checks if message is a valid command
    if(command != '/weather'):
        return
    #parses message
    args = m_list[1].rsplit(' ', 1)
    city = args[0]
    state = args[1]
    
    print('Forecasting weather for:')
    print('City: ', city)
    print('State: ', state)
    print('In progress...')

    #api request
    url = 'https://wttr.in/{},{}'.format(city, state)
    response = requests.get(url)  
    print('Forecasting complete.')
    print(response)

    #due to discord message character limits, just grabs the current weather
    #and appends the rest of the forecast via a url
    weather = response.text.split('─', 1)[0]
    forecast = '\nFor the rest of the forecast, please visit {}.'.format(url)
    responseMessage = '```' + weather + '```' + forecast
    #sends back response
    await message.channel.send(responseMessage)
    

client.run(token)
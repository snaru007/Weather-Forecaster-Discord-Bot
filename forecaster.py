# Code for the weather forecaster discord bot using openweathermap
import os
import discord
import requests
from dotenv import load_dotenv

#code for connecting the bot to discord and getting the weather api key
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
api_key = os.getenv('API_KEY')
base_url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + api_key + '&units=imperial&q='

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord.')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    m_list = message.content.split(' ', 1)
    command = m_list[0]
    #checks if message is a valid command
    if(command != '/weather'):
        return
    #parses message, checks for both space and comma delimiters
    args = m_list[1].split(',')
    argString = ''
    if(len(args) < 3):
        arg_string = m_list[1].replace(' ', ',')
    else:
        arg_string = m_list[1]

    args = arg_string.split(',')
    city = args[0].capitalize()
    state = args[1].upper()
    country = args[2].upper()

    print('Forecasting weather for ', arg_string, '...')

    #api request
    url = base_url + arg_string
    response = requests.get(url)  
    print('Forecasting complete.')
    #creates the embed response
    print('Generating embed...')

    #gets the current discord channel
    channel = message.channel

    #parses out current weather info
    json_res = response.json()
    if(json_res['cod'] != '404'):
        async with channel.typing():
            weather = json_res['main']
            #temp is in fahrenheit as specified in the base_url at the top in the units parameter
            current_temp = weather['temp']
            current_humidity = weather['humidity']
            description = json_res['weather'][0]['description']

            #formats weather info in discord embed
            embed = discord.Embed(title=f'Weather in {city}, {state}, {country}', color=message.guild.me.top_role.color, timestamp=message.created_at)
            embed.add_field(name='Description', value=f'**{description}**', inline=False)
            embed.add_field(name='Temperature (F)', value=f'**{current_temp}**', inline=False)
            embed.add_field(name='Humidity (%)', value=f'**{current_humidity}**', inline=False)

            embed.set_thumbnail(url=f'http://flags.ox3.in/svg/{country}/{state}.svg')
            embed.set_footer(text=f'Requested by {message.author.name}')
            print('Embed created.')
    #sends back the response message embed or a failure message
        await channel.send(embed=embed)
    else:
        await channel.send('Could not determine specified location.')


client.run(token)
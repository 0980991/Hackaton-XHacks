# bot.py
from asyncio.windows_events import NULL
import os

import discord
from dotenv import load_dotenv

import newsapi as na

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f'{self.guilds}')

    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.content == '!helloworld':
            await message.channel.send('Hello, world!')
        if message.content == '!qt':
            if message.reference != NULL:
                message = await message.channel.fetch_message(message.reference.message_id)
                await message.channel.send(self.ruinSentence(message.content))
        if message.content == '!whatsnew':
            news = self.getNews()
            for article in news:
                await message.channel.send(article)


    def getNews(self):
        key = os.getenv('DISCORD')
        newsapi = na.NewsApiClient(api_key=key)
        data = newsapi.get_everything(q='bbc-news', language='en', page_size=5)

        retlist = []
        articles = data['articles']
        for i, article in enumerate(articles):
            retlist.append(f'{i+1}\t{article["title"]}https://www.bbc.com/sport/live/olympics/52501715\n')
        
        return retlist

    def ruinSentence(self, string):
        string = string.capitalize()
        newstring = ""
        i = 0
        for char in string:
            i += 1
            if i % 3 == 0:
                continue
            if i % 5 == 0:
                newstring += char.lower()
            else:
                newstring += char.upper()

        return newstring
        
client = CustomClient()
client.run(TOKEN)

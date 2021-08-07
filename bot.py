# bot.py
from asyncio.windows_events import NULL
import os

import discord
from dotenv import load_dotenv

import newsapi as na

import UIFunctions as ui

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f'{self.guilds}')

    async def on_message(self, message):
        if message.content == '!whatsnew':
            articlelist = self.getNews()
            for article in articlelist:
                await message.channel.send(article)
        if message.author == client.user:
            return
        else:
            userprofile = self.handleUserId(message.author.id)
        if message.content == '!helloworld':
            await message.channel.send(f'Hello, world! {userprofile.id}')
        if message.content == '!qt':
            if message.reference != NULL:
                message = await message.channel.fetch_message(message.reference.message_id)
                await message.channel.send(self.ruinSentence(message.content))
        if message.content == '!whatsnew':
            articlelist = self.getNews()
            for article in articlelist:
                await message.channel.send(article)
        if message.content == '!dn':
            await message.channel.send('D33Z NUT5')

    def handleUserId(self, id):
        return db.loadUser(id)

    def getNews(self):
        key = os.getenv('NEWSAPI_KEY')
        newsapi = na.NewsApiClient(api_key=key)
        data = newsapi.get_everything(q='politics', language='en', page_size=5)

        retlist = []
        articles = data['articles']
        for i, article in enumerate(articles):
                retlist.append(ui.formatArticle(article, i))

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

# bot.py
from asyncio.windows_events import NULL
import os

import random

import discord
from dotenv import load_dotenv

import newsapi as na

import UIFunctions as ui

import userProfile
db = userProfile.userDatabase()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f'{self.guilds}')

    async def on_message(self, message):
        if message.author == client.user:
            return
        else:
            userprofile = self.handleUserId(message.author.id)

        if message.content == '!whatsnew':
            articlelist = self.getNews(userprofile.amountOfNews, userprofile.interests, userprofile)
            await message.channel.send("Your news has been mailed to your inbox")
            for article in articlelist:
                await message.author.send(article)

        if message.content == '!helloworld':
            await message.channel.send(f'Hello, world! {userprofile.id}')

        if message.content == '!qt':
            if message.reference != NULL:
                message = await message.channel.fetch_message(message.reference.message_id)
                await message.channel.send(self.ruinSentence(message.content))

        if message.content == '!options':
            await message.channel.send("**OPTION MENU**\n\t**1.** - Add / remove news categories\n\t**2.** - Alter mail size\n\t**3.** - Edit mail time interval\n\nEnter your option")
            msg = await client.wait_for('message')
            while msg.author != message.author:
                msg = await client.wait_for('message')
            if int(msg.content) in range(1,4):
                #await message.channel.send(msg.content)
                if int(msg.content) == 1:
                    await message.channel.send("**1.** - Add category\n**2.** - Remove category")
                    msg = await client.wait_for('message')
                    while msg.author != message.author and int(msg.content) in range(1,3):
                        msg = await client.wait_for('message')
                    if int(msg.content) == 1:
                        # Add category
                        if len(userprofile.interests) > 0:
                            await message.channel.send(f'Your categories: {userprofile.interests}')
                        await message.channel.send("What category would you like to add?")
                        msg = await client.wait_for('message')
                        while msg.author != message.author:
                            msg = await client.wait_for('message')
                        userprofile.addInterest(msg.content)
                        db.editUser(userprofile)
                        await message.channel.send("Category added!")

                    else:
                        # Remove category
                        if len(userprofile.interests) > 0:
                            await message.channel.send(f'Your categories: {userprofile.interests}')
                            await message.channel.send(f'Please enter which category you would like to remove')
                            msg = await client.wait_for('message')
                            while msg.author != message.author:
                                msg = await client.wait_for('message')
                            if msg.content in userprofile.interests:
                                userprofile.removeInterest(msg.content)
                                db.editUser(userprofile)
                                await message.channel.send(f'Category removed!')
                            else:
                                await message.channel.send(f'Category not found.')


                        else:
                            await message.channel.send(f'You have no categories')
                            return


                    

                    pass
                elif int(msg.content) == 2:
                    await message.channel.send("How many mails would you like to receive per delivery? (1-20)")
                    msg = await client.wait_for('message')
                    while msg.author != message.author and int(msg.content) in range(1,20):
                        msg = await client.wait_for('message')
                    userprofile.setAmountOfNews(int(msg.content))
                    db.editUser(userprofile)
                    await message.channel.send("News amount updated!")
                    return

                elif int(msg.content == 3):
                    await message.channel.send("FILLER TEXT")
                    pass

        if message.content == '!dn':
            await message.channel.send('D33Z NUT5')

    def handleUserId(self, id):
        return db.loadUser(id)

    def getNews(self, pagesize, interests, userprofile):
        key = os.getenv('NEWSAPI_KEY')
        newsapi = na.NewsApiClient(api_key=key)
        data = []
        for i in range(len(interests)):
            interest = interests[i%len(interests)]
            data.append(newsapi.get_everything(q=interest, language='en', page_size=userprofile.amountOfNews))

        retlist = []
        articles = data
        for i in range(userprofile.amountOfNews):
            retlist.append(ui.formatArticle(random.choice(articles)['articles'][i], i))

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

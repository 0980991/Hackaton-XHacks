# bot.py
from asyncio.windows_events import NULL
import os

import random

import discord
from dotenv import load_dotenv

import newsapi as na

import datetime as dt

import UIFunctions as ui

import userProfile

from discord.ext import tasks, commands

from discord.utils import get

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

        if message.content.startswith('!interval '):
            argument = message.content[10:]
            if userprofile.setInterval(argument):
                await message.channel.send("Preference updated!")
                db.editUser(userprofile)
            else:
                await message.channel.send("Invalid input.")

        if message.content.startswith('!mailsize '):
            argument = message.content[10:]
            if int(argument) > 0 and int(argument) <= 20:
                userprofile.setAmountOfNews(int(argument))
                db.editUser(userprofile)
                await message.channel.send("News amount updated!")
            else:
                await message.channel.send("Invalid input. (1-20)")


        if message.content.startswith('!addcategory '):
            argument = message.content[13:]
            userprofile.addInterest(argument)
            db.editUser(userprofile)
            await message.channel.send("Category added!")


        if message.content.startswith('!removecategory '):
            argument = message.content[16:]
            userprofile.removeInterest(argument)
            db.editUser(userprofile)
            await message.channel.send("Category removed!")

        if message.content == '!listcategories':
            await message.channel.send(f'{userprofile.interests}')

        if message.content == '!help' or message.content == '!helppaperboy':
            await message.channel.send(f'**COMMANDS AND GUIDE**```\n\n\t!whatsnew - *Sends a fresh dose of mail to you right away*\n\n\t!automail - *Enables / disables automatic time-interval mail packets*\n\n\t!mailsize [number] - *set the size of your mail packets*\n\n\t!interval [1h / 3h / 6h / 12h / 24h] - *Set the time-interval between automatic mail packets*\n\n\t!listcategories - *list your personal mail categories*\n\n\t!addcategory [category] - *Add a keyword of interest to your category list*\n\n\t!removecategory [category] - *Remove a category from your personal category list*\n\n\t!help - *List the commands to use this bot*\n\n\t!options - *Open up an interactive menu to edit personal settings*```')

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

                elif int(msg.content) == 2:
                    await message.channel.send("How many mails would you like to receive per delivery? (1-20)")
                    msg = await client.wait_for('message')
                    while msg.author != message.author and int(msg.content) in range(1,20):
                        msg = await client.wait_for('message')
                    userprofile.setAmountOfNews(int(msg.content))
                    db.editUser(userprofile)
                    await message.channel.send("News amount updated!")
                    return

                elif int(msg.content) == 3:
                    await message.channel.send("How often would you like to receive your mail? \nEvery: 1h, 3h, 6h, 12h, 24h")
                    msg = await client.wait_for('message')
                    if userprofile.setInterval(msg.content):
                        await message.channel.send("Preference updated!")
                        db.editUser(userprofile)
                    else:
                        await message.channel.send("Invalid input.")

        if message.content == '!automail':
            userprofile.receiveAutoMail = not userprofile.receiveAutoMail
            db.editUser(userprofile)
            await message.channel.send(f"Your automail preference has been set to {userprofile.receiveAutoMail}")
            return

        if message.content == '!dn':
            await message.channel.send('D33Z NUT5')

        if message.content == '!mass':
            await self.sendMassMail()

    @tasks.loop(seconds=3600.0)
    async def sendMassMail(self):
        currentHour = dt.datetime.now().hour
        print(currentHour % 12)
        users = db.getAllUsers()
        for user in users:
            userOnDiscord = await self.fetch_user(str(user.id))
            if user.receiveAutoMail == True:
                if user.interval == "3h":
                    if currentHour % 3 != 0:
                        continue
                elif user.interval == "6h":
                    if currentHour % 6 != 0:
                        continue
                elif user.interval == "12h":
                    if currentHour % 12 != 0:
                        continue
                elif user.interval == "24h":
                    if currentHour % 24 != 12:
                        continue
                articlelist = self.getNews(user.amountOfNews, user.interests, user)
                for article in articlelist:
                    await userOnDiscord.send(article)


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
client.sendMassMail.start()
client.run(TOKEN)
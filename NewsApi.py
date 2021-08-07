import requests
import newsapi as na
import datetime as dt
import UIFunctions as ui


class NewsAPI():
    def getNews(self):
        key = '4f4ed8ca60dd4d53bbf8714662fb1d0e'
        newsapi = na.NewsApiClient(api_key=key)
        data = newsapi.get_everything(q='politics', language='en', page_size=5)


        articles = data['articles']
        for i, article in enumerate(articles):
            ui.formatArticle(article, i)







hn = NewsAPI()
hn.getNews()











'''
class HNAPI():
    def getNews(self):

        url = "https://community-hacker-news-v1.p.rapidapi.com/user/jl.json"

        querystring = {"print":"pretty"}

        headers = {
            'x-rapidapi-key': "bb1bcad953msh4a1dfd43ff13b0ap1d9c24jsn4cebe941a3cc",
            'x-rapidapi-host': "community-hacker-news-v1.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        for index, story in enumerate(response):
            story = self.byteToDic(story)
            itemurl = f"https://community-hacker-news-v1.p.rapidapi.com/item/{story['id']}.json"


            querystring = {"print":"pretty"}

            headers = {
                'x-rapidapi-key': "bb1bcad953msh4a1dfd43ff13b0ap1d9c24jsn4cebe941a3cc",
                'x-rapidapi-host': "community-hacker-news-v1.p.rapidapi.com"
                }

            response = requests.request("GET", itemurl, headers=headers, params=querystring)

            print(response.text)

    def byteToDic(self, bytestring):
        return bytestring.decode('utf-8')

#HNAPI().getNews()
for i in HNAPI().byteToDic(b'{\n  "about" : "This is a test"}'):
    print(i)
'''
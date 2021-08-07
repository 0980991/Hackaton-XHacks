def formatArticle(article, i):
    retstring = f'{i+1}\t{article["title"]}\n\t\t{formatDescription(article["description"])}'
    retstring += f'\n\tLink: {article["url"]}'
<<<<<<< Updated upstream
    return retstring
=======
    print(retstring)
>>>>>>> Stashed changes

def formatDescription(description):
    retstring = ''
    for i in range(len(description)):
        retstring += description[i]
        if i != 0 and i % 60 == 0:
            retstring += '\n\t\t'

    return retstring
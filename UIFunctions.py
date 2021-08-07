def formatArticle(article, i):
    retstring = f'{i+1}\t{article["title"]}\n\t\t{formatDescription(article["description"])}'
    retstring += f'\n\tLink: {article["url"]}'

    return retstring


def formatDescription(description):
    retstring = ''
    for i in range(len(description)):
        retstring += description[i]
        if i != 0 and i % 100 == 0:
            retstring += '\n\t\t'

    return retstring
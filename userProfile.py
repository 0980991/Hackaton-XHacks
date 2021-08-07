import json
import os

class userProfile:
    # Only pass ID to create new user, pass everything to load one from json
    def __init__(self, id, interests=[], interval='24h', amountOfNews=5, receiveAutoMail=False):
        self.id = id
        self.interests = interests
        self.interval = interval
        self.amountOfNews = amountOfNews
        self.receiveAutoMail = receiveAutoMail

    def addInterest(self, interest):
        self.interests.append(interest)
        return

    def removeInterest(self, interest):
        if interest in self.interests:
            self.interests.remove(interest)
        return
    
    def setInterval(self, interval):
        intervals = ["1h", "3h", "6h", "12h", "24h"]
        if interval in intervals:
            self.interval = interval
            return True
        else:
            return False

    def setAmountOfNews(self, num):
        self.amountOfNews = num
        return

# Handle the creation and storage of users. Also save user's profiles to a JSON file
class userDatabase:
    def __init__(self):
        self.jsonFile = './userProfiles.json'
        if not os.path.isfile(self.jsonFile):
            json.dump({}, open(self.jsonFile, 'w'))
        self.jsonRead = json.loads(open(self.jsonFile, 'r').read())
        

    # Creates a new user with the default values and writes it to the JSON file
    def createUser(self, id):
        user = userProfile(id)
        self.writeUser(user)
        return user

    def getAllUsers(self):
        users = []
        for id in self.jsonRead.keys():
            users.append(self.getUser(id))
        return users

    def loadUser(self, id):
        if self.doesUserExist(id):
            return self.getUser(id)
        else:
            return self.createUser(id)

    # Simply writes the new user info to the existing JSON
    def editUser(self, user):
        self.writeUser(user) 
        return

    def doesUserExist(self, id):
        if str(id) in self.jsonRead.keys():
            return True
        return False

    def writeUser(self, user):
        self.jsonRead[str(user.id)] = {
            'id': user.id,
            'interests': user.interests,
            'interval': user.interval,
            'amountOfNews': user.amountOfNews,
            'receiveAutoMail': user.receiveAutoMail
        }
        with open(self.jsonFile, 'w') as outputFile:
            json.dump(self.jsonRead, outputFile)
            outputFile.close()
        return

    # Creates user profile based on json contents
    def getUser(self, userId):
        if str(userId) in self.jsonRead.keys():
            return userProfile(userId, self.jsonRead[str(userId)]["interests"], self.jsonRead[str(userId)]["interval"], self.jsonRead[str(userId)]["amountOfNews"], self.jsonRead[str(userId)]["receiveAutoMail"])



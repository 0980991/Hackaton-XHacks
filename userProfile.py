import json

class userProfile:
    # Only pass ID to create new user, pass everything to load one from json
    def __init__(self, id, interests=[], interval='24h', amountOfNews=5):
        self.id = id
        self.interests = interests
        self.interval = interval
        self.amountOfNews = amountOfNews

    def addInterest(self, interest):
        self.interests.append(interest)
        return

    def removeInterest(self, interest):
        if interest in self.interests:
            self.interests.remove(interest)
        return
    
    def setInterval(self, interval):
        intervals = ["1h", "3h", "6h", "12h", "24h", "48h", "72h", "168h"]
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
        self.json = json.loads(open(self.jsonFile, 'r'))

    # Creates a new user with the default values and writes it to the JSON file
    def createUser(self, id):
        user = userProfile(id)
        self.writeUser(user)
        return user

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
        if id in self.json:
            return True
        return False

    def writeUser(self, user):
        self.json[user.id] = {
            'id': user.id,
            'interests': user.interests,
            'interval': user.interval,
            'amountOfNews': user.amountOfNews
        }
        return

    # Creates user profile based on json contents
    def getUser(self, userId):
        if userId in self.json:
            return userProfile(userId, self.json["interests"], self.json["interval"], self.json["amountOfNews"])



class userProfile:
    def __init__(self, id):
        self.id = id
        self.interests = []
        self.interval = "24h"

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
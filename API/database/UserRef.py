from models import User
from models import UserAchievement
from models import Achievement

class UserRef:

    def UserRef(new_username, new_password):
        u = User(username = new_username, name = new_username, password = new_password,
                 xp = 0, points = 0, has_been_verified = False)
        u.save()

    def verifyAccount(current_username):
        current_username.has_been_verified = True
        current_username.save()

    def bottleFilled(current_username):
        current_username.points = current_username.points + 5
        current_username.save()

    def setName(current_username, changed_name):
        updating_user = User.objects.get(username = current_username)
        updating_user.name = changed_name
        updating_user.save()

    def getUsersName(current_username):
        name = User.objects.get(username = current_username).name
        return name

    def getPassword(current_username):
        password = User.objects.get(username = current_username).password
        return password
    
    def getUserLevel(current_username):
        xp = User.objects.get(username = current_username).xp
        level = 10*(math.log(1-((xp(1-(2**(1/10))))/5) ,2))
        level = int(level)
        return level

    def getUserXpLeft(current_username):
        xp = User.objects.get(username = current_username).xp
        level = 10*(math.log(1-((xp(1-(2**(1/10))))/5) ,2))
        level = int(level)
        xp_left = xp - ((5(1-(2**(level/10)))) / (1-(2**(1/10))))
        xp_left = int(xp_left) + 1
        return xp_left

    def getPoints(current_username):
        points = User.objects.get(username = current_username).password
        return points
    

    def updateAcheivements(current_username):
        bottles = User.objects.get(username = current_username).bottles
        listOfAchievements = UserAchievement.objects.all()
    
        #Fill up your first bottle
        if bottles >= 1:
            newUserAchievement = UserAchievement(User.objects.get(username = current_username),
                                                 Achievement.objects.get(challenge = "Fill up your first water bottle"))
            newUserAchievement.save




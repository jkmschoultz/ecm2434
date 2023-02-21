from models import User

class UserRef:

    def UserRef(new_username, new_password):
        u = User(username = new_username, name = new_username, password = new_password,
                 xp = 0, points = 0, has_been_verified = False)
        u.save()

    def setName(current_username, changed_name):
        updating_user = User.objects.get(username = current_username)
        updating_user.name = changed_name
        updating_user.save()

    def verifyAccount(current_username):
        current_username.has_been_verified = True
        current_username.save()

    def getUsersName(current_username):
        name = User.objects.get(username = current_username).name
        return name

    def getPassword(current_username):
        password = User.objects.get(username = current_username).password
        return password
    
    def getUserLevel(current_username):
        xp = User.objects.get(username = current_username).xp
        level = 5*(math.log(1-((xp(1-(2**(1/5))))/20) ,2))
        level = int(level)
        return level

    def getUserXpLeft(current_username):
        xp = User.objects.get(username = current_username).xp
        level = 5*(math.log(1-((xp(1-(2**(1/5))))/20) ,2))
        level = int(level)
        xp_left = xp - ((20(1-(2**(level/5)))) / (1-(2**(1/5))))
        return xp_left

    def getPoints(current_username):
        points = User.objects.get(username = current_username).password
        return points

    



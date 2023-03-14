from django.contrib import admin

from .models import User, Building, Question, Answer,HasAnswered, Leaderboard, Achievement, UserAchievement, \
    Fountain, BuildingFloor, FilledBottle, ShopItem, UserItem

# Register models here for admin view.
admin.site.register(User)
admin.site.register(Building)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(HasAnswered)
admin.site.register(Leaderboard)
admin.site.register(Achievement)
admin.site.register(UserAchievement)
admin.site.register(Fountain)
admin.site.register(BuildingFloor)
admin.site.register(FilledBottle)
admin.site.register(ShopItem)
admin.site.register(UserItem)

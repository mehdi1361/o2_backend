from django.contrib import admin
from o2_api.models import GameUser, Tournament, Game
# Register your models here.
@admin.register(GameUser)
class GameUserAdmin(admin.ModelAdmin):
    list_display = ["uuid", "phone_number"]

class GameAdmin(admin.TabularInline):
    model = Game

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["id", "tournament_name", "start_date", "end_date", "max_user"]
    inlines = [GameAdmin]




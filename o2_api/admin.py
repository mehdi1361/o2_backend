from django.contrib import admin
from o2_api.models import GameUser, Tournament, Game, Package,BuyPackage
# Register your models here.
@admin.register(GameUser)
class GameUserAdmin(admin.ModelAdmin):
    list_display = ["user","uuid", "phone_number","gem_quantity"]

class GameAdmin(admin.TabularInline):
    model = Game

class BuyPackageAdmin(admin.TabularInline):
    model = BuyPackage

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["id", "tournament_name", "start_date", "end_date", "max_user"]
    inlines = [GameAdmin]

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "gem_quantity", "description"]
    inlines = [BuyPackageAdmin]


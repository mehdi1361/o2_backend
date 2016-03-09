from django.contrib import admin
from o2_api.models import GameUser
# Register your models here.
@admin.register(GameUser)
class GameUserAdmin(admin.ModelAdmin):
	list_display = ["uuid","phone_number"]

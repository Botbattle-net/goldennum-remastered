from django.contrib import admin

from app.models import Room, User

# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'roomid', 'status')
    list_filter = ['roomid']
    search_fields = ['roomid']


admin.site.register(Room, RoomAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'room', 'status')
    list_filter = ['name', 'room']
    search_fields = ['name']


admin.site.register(User, UserAdmin)

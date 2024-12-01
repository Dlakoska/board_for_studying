from django.contrib import admin

from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email',]


@admin.register(Payment)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user', ]


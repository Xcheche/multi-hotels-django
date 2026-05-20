from django.contrib import admin
from .models import CustomUser, Profile


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email","full_name", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "full_name")
    ordering = ("-date_joined",)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "country", "city", "is_verified")
    search_fields = ("user__email", "full_name", "country", "city")
    list_filter = ("is_verified",)
    ordering = ("-date",)    

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)

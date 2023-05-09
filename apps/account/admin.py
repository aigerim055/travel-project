from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()

# class UserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'phone', 'is_active', 'is_staff']
    # list_editable = ['is_active', 'is_staff']

admin.site.register(User)
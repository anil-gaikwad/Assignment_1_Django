from .models import Account
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin 
# Register your models her

# Admin model
class AccountAdmin(UserAdmin):
    list_display=('email','firstname','lastname','is_active','date_joined','last_login')
    list_display_links=('email','firstname')
    readonly_fields=('last_login','date_joined')
    
    filter_horizontal=()
    list_filter=()
    fieldsets=()

admin.site.register(Account,AccountAdmin)

admin.site.register(Customer)
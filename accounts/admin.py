from django.contrib import admin
from accounts.models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'avatar', 'additional', 'phone', 'gender')
    list_filter = ('email', 'avatar', 'additional', 'phone', 'gender')
    search_fields = ('email', 'avatar', 'additional', 'phone', 'gender')
    fields = ('email', 'avatar', 'additional', 'phone', 'gender')
    readonly_fields = ['id']


admin.site.register(Account, AccountAdmin)

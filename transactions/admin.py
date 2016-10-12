
from django.contrib import admin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('balance',)

admin.site.register(Account, AccountAdmin)

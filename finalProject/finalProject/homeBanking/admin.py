from django.contrib import admin
from .models import User,Account,CreditCard,Transaction

admin.site.register(User)
admin.site.register(Account)
admin.site.register(CreditCard)
admin.site.register(Transaction)
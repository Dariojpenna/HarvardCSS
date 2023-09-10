from django.contrib import admin
from .models import User,Account,Card,Transaction,Service

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Card)
admin.site.register(Transaction)
admin.site.register(Service)

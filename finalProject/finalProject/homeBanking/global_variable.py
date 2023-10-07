from .models import Account
from django.contrib.auth.models import AbstractUser

def global_variable(request):
    if request.user.is_authenticated:
        account = Account.objects.get(owner=request.user)
        account_bank = account.bank
    else:
        account_bank = None

    return {'global_account': account_bank}
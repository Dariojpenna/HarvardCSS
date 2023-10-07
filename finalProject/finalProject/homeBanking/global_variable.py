from .models import Account

def global_variable(request):
    if request.user.is_authenticated:
        account = Account.objects.get(owner=request.user)
        account_bank = account.bank
    else:
        account_bank = None

    return {'global_account': account_bank}
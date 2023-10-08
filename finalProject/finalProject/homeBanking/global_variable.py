from .models import Account

def global_variable(request):
    if request.user.is_authenticated:
        print(request.user.id)
        try:
            account = Account.objects.get(id=request.user.id)
            account_bank = account.bank
        except:
            account_bank =None
    else:
        account_bank = None

    return {'global_account': account_bank}
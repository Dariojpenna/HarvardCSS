
import json
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .forms import UserForm
from .models import User, Transaction,Account
from django.db import IntegrityError
import random
from django.db.models import Q
from twilio.rest import Client
import random
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.paginator import Paginator

# Create your views here.



def index(request):
    
    if request.user.is_authenticated:
        account = Account.objects.get(owner=request.user)
        return render(request, "index.html",{
            "user":request.user,
            "account": account
        })
    
    return render(request, 'login.html')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        dni = request.POST['document']
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            if int(dni) == user.dni:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {
                "message": "The document does not match "
            })
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
        # Check if authentication successful
        
    else:
        return render(request, "login.html",{
                "message": "The method is a GET"
            })



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def switch(cbu):
    if cbu >= 1000000000000000000000 and cbu < 2000000000000000000000:
        bank="Aurora_Finance_Bank"
    elif cbu >= 2000000000000000000000 and cbu < 3000000000000000000000:
        bank="NexaBank"
    elif cbu >= 3000000000000000000000 and cbu < 4000000000000000000000:
        bank="Horizon_Trust_Bank"
    elif cbu >= 4000000000000000000000 and cbu < 5000000000000000000000:
        bank="Crescent_Financial_Bank"
    elif cbu >= 5000000000000000000000 and cbu < 6000000000000000000000:
        bank="Veridian_Bank"
    elif cbu >= 6000000000000000000000 and cbu < 7000000000000000000000:
        bank="Pinnacle_Finance_Bank"
    elif cbu >= 7000000000000000000000 and cbu < 8000000000000000000000:
        bank="Solstice_Savings_Bank"
    elif cbu >= 8000000000000000000000 and cbu < 9000000000000000000000:
        bank="Equinox_Capital_Bank"
    elif cbu >= 9000000000000000000000:
        bank="Voyager_Bancorp_Bank"


    return bank


def  register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dni = request.POST['document']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['country_code'] + request.POST['phone']
        password = request.POST['password'] 
        cbu =  random.randrange(10**21, 10**22)
        bank= switch(cbu)
        if password != request.POST['password-confirm']:
            return render(request, 'register.html',{
                'message':"Passwords must match."
            })

        try:
            user = User.objects.create_user(first_name=first_name,last_name=last_name,dni=dni,username=username,email=email,phone_number=phone, password=password)
            user.save()
            account= Account.objects.create(owner = user, cbu = cbu,bank=bank)
            account.save()
        except IntegrityError:
            return render(request, "network/aaasd.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))


    return render(request, 'register.html',{
        'form':UserForm
    })


def deposit(request):
    type = "Deposit"
    account = Account.objects.get(owner=request.user)
    deposits = Transaction.objects.filter(account_sender=account,type="Deposit").order_by("id").reverse()

    paginator = Paginator(deposits, 10)
    pageNumber = request.GET.get('page')
    depositsInPage = paginator.get_page(pageNumber)
    
    subject = 'New transaction detected'
    message = f'There was a deposit on your account'
    from_email = 'mydjangoapp88@gmail.com'
    recipient_list = [account.owner.email]

    send_mail(subject, message, from_email, recipient_list)

    if request.method == 'POST':
        transaction_amount = request.POST['amount']
        transaction = Transaction(transaction_amount=transaction_amount,type=type,account_sender=account,account_recipient=account)
        transaction.save()
        account.account_amount= account.account_amount + int(transaction_amount)
        account.save()

        return render(request, "index.html",{
            "message": "The deposit was made correctly",
            "user":request.user,
            "account": account,
            "deposits":deposits,
            "depositsInPage":depositsInPage,
        })
    else:
        return render(request, "deposit.html",{
            "deposits":deposits,
            "depositsInPage":depositsInPage,
        })    
    


def transfer(request):
    account_sender = Account.objects.get(owner=request.user)
    transactions= Transaction.objects.filter((Q(account_sender=account_sender) | Q(account_recipient=account_sender)) and Q(type="Transfer")).order_by("id").reverse()
    
    paginator = Paginator(transactions, 5)
    pageNumber = request.GET.get('page')
    transactionsInPage = paginator.get_page(pageNumber)

    if request.method == 'POST':
        transaction_amount = request.POST['amount']
        cbu_recipient = request.POST['cbu_recipient']
        try :
            account_recipient = Account.objects.get(cbu=cbu_recipient)
        except Exception :

            return HttpResponse(f"Error: The Account doesn't exist.")
        
        if account_sender ==  account_recipient:
            return render(request, "transfer.html",{
                "message": "You can't make a transfer to you own account",
                "transactions": transactions,
                "account": account_sender,
                "transactionsInPage":transactionsInPage,
            }) 
        
        elif  account_sender.account_amount >= int(transaction_amount) :
            type = "Transfer"
            transaction = Transaction(transaction_amount=transaction_amount,type=type,account_sender=account_sender,account_recipient=account_recipient)  
            transaction.save()

            account_recipient.account_amount= account_recipient.account_amount + int(transaction_amount)
            account_recipient.save()

            account_sender.account_amount = account_sender.account_amount - int(transaction_amount)
            account_sender.save()

            
            subject = 'New transaction detected'
            message = f'Transfer request has been made from your account'
            from_email = 'mydjangoapp88@gmail.com'
            recipient_list = [account_sender.owner.email]

            send_mail(subject, message, from_email, recipient_list)

    
        
            return render(request, "index.html",{
                "message": "The Transfer was made correctly",
                "user":request.user,
                "account": account_sender,
                "transactions": transactions,
                "transactionsInPage":transactionsInPage,
            })

        else:
            return render(request, "transfer.html",{
                "message": "You have not enought money in your account for make  this transaction",
                "transactions": transactions,
                "user":request.user,
                "account": account_sender,
                "transactionsInPage":transactionsInPage,
            })  
    else:
        return render(request, "transfer.html",{
            "transactions": transactions,
            "user":request.user,
            "account": account_sender,
            "transactionsInPage":transactionsInPage,
        }) 
    

codigo_generado = None

def code_generator(request):
    global codigo_generado
    code = random.randint(10000, 99999) 
    codigo_generado = code
    if request.method =='POST':

        client = Client(account_sid, auth_token)
        
        message = client.messages \
                        .create(
                            body= code,
                            from_='+17622494206',
                            to='+393519556264'
                        )

        print(message.sid)
    return JsonResponse({"mensaje": "Código generado con éxito."})


def code_checker(request):
    codigo = request.POST.get('codigo')
    if int(codigo) == codigo_generado:
        return JsonResponse({"message": "1"})
    else:
        return JsonResponse({"message": "2"})

def services(request):
    return render (request, "services.html")


def transfer_detail(request,transactionId):
    transfer = Transaction.objects.get(id=transactionId)
    return render(request, "transferDetail.html",{
        'transfer':transfer,
        "user":request.user,
    })

def profile(request):
    return render(request, 'profile.html',{
        "user":request.user,
    })


def editEmail(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        new_email = data.get('new_email')
        #user = User.objects.get(owner=request.user)

        user = request.user
        user.email = new_email
        user.save()
        response_data = {
            'message': "Successful Modification",
            'email': new_email
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def editPhone(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_phone_number = data.get('new_phone')

        print(new_phone_number)
        user = request.user
        user.phone_number = new_phone_number
        user.save()
        
        response_data = {
            'message': "Successful Modification",
            'phoneNumber': new_phone_number
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
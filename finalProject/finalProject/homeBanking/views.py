
from io import BytesIO
import json
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import UserForm
from .models import User, Transaction,Account,Card,Service,Notification
from django.db import IntegrityError
import random
from django.db.models import Q
from twilio.rest import Client
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from decimal import Decimal
from datetime import datetime
from django.http import FileResponse
from django.shortcuts import render
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import colors
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.units import inch


def index(request):
    #Check authentification
    if request.user.is_authenticated:
        try:
            account = Account.objects.get(id=request.user)
        except:    
            logout(request)
            return redirect('logout')
        transactions = Transaction.objects.order_by('-id')[:5]
        # Response with user authenticated
        return render(request, "index.html",{
            "user":request.user,
            "account": account,
            'transactions':transactions
        })
    # Response with user  not authenticated
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
                
            })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

    #Choose the bank randomly
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
    #Check Method
    if request.method == "POST":
        #Get Data 
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dni = request.POST['document']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['country_code'] + request.POST['phone']
        password = request.POST['password'] 
        cbu =  random.randrange(10**21, 10**22)
        bank= switch(cbu)
        #Password confirm and get user 
        if password != request.POST['password-confirm']:
            return render(request, 'register.html',{
                'message':"Passwords must match."
            })

        try:
            #Creat account
            user = User.objects.create_user(first_name=first_name,last_name=last_name,dni=dni,username=username,email=email,phone_number=phone, password=password)
            user.save()
            account= Account.objects.create(owner = user,
                                            cbu = cbu,
                                            bank=bank)
            account.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username or Document already exist."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))


    return render(request, 'register.html',{
        'form':UserForm
    })


def deposit(request):
    # Get data
    account = Account.objects.get(owner=request.user)
    deposits = Transaction.objects.filter(account_sender=account,type="Deposit").order_by("id").reverse()
    # Paginator
    paginator = Paginator(deposits, 10)
    pageNumber = request.GET.get('page')
    depositsInPage = paginator.get_page(pageNumber)
    transactions = Transaction.objects.order_by('-id')[:5]
    # Email data
    subject = 'New transaction detected'
    message = f'There was a deposit on your account'
    from_email = 'mydjangoapp88@gmail.com'
    recipient_list = [account.owner.email]

    if request.method == 'POST':
        # Create deposit
        type = "Deposit"
        transaction_amount = request.POST['amount']
        transaction = Transaction(transaction_amount=transaction_amount,type=type,account_sender=account,account_recipient=account)
        transaction.save()
        account.account_amount= account.account_amount + int(transaction_amount)
        account.save()
        #Send a email
        send_mail(subject, message, from_email, recipient_list)
        # Response
        return render(request, "index.html",{
            "message": "The deposit was made correctly",
            "user":request.user,
            "account": account,
            'transactions':transactions
        })
    else:
        #GET  Response
        return render(request, "deposit.html",{
            "deposits":deposits,
            "depositsInPage":depositsInPage,
        })    
    


def transfer(request):
    # Get data and set variables
    account_sender = Account.objects.get(owner=request.user)
    transactions1= Transaction.objects.filter(Q(account_sender=account_sender) | Q(account_recipient=account_sender)).order_by("id").reverse()
    transactions = transactions1.filter(Q(type="Debit") | Q(type='Transfer'))

    # Paginator 
    paginator = Paginator(transactions, 10)
    pageNumber = request.GET.get('page')
    transactionsInPage = paginator.get_page(pageNumber)
    transactions_index = Transaction.objects.order_by('-id')[:5]

    if request.method == 'POST':
        # Check for a validation account
        transaction_amount = request.POST['amount']
        cbu_recipient = request.POST['cbu_recipient']
        try :
            account_recipient = Account.objects.get(cbu=cbu_recipient)
        except Exception :

            return HttpResponse(f"Error: The Account doesn't exist.")
        
        # You cant transfer yourself
        if account_sender ==  account_recipient:
            return render(request, "transfer.html",{
                "message": "You can't make a transfer to you own account",
                "transactions": transactions,
                "account": account_sender,
                "transactionsInPage":transactionsInPage,
            }) 
        # Check if we have money
        elif  account_sender.account_amount >= int(transaction_amount) :
            #Create a Transaction
            type = "Transfer"
            transaction = Transaction(transaction_amount=transaction_amount,type=type,account_sender=account_sender,account_recipient=account_recipient)  
            transaction.save()

            account_recipient.account_amount= account_recipient.account_amount + int(transaction_amount)
            account_recipient.save()

            account_sender.account_amount = account_sender.account_amount - int(transaction_amount)
            account_sender.save()

            # Send a email alert to the owner email
            subject = 'New transaction detected'
            message = f'Transfer request has been made from your account'
            from_email = 'mydjangoapp88@gmail.com'
            recipient_list = [account_sender.owner.email]

            send_mail(subject, message, from_email, recipient_list)

    
        
            return render(request, "index.html",{
                "message": "The Transfer was made correctly",
                "user":request.user,
                "account": account_sender,
                'transactions':transactions_index

            })
        # If we don0t have money
        else:
            return render(request, "transfer.html",{
                "message": "You have not enought money in your account for make  this transaction",
                "transactions": transactions,
                "user":request.user,
                "account": account_sender,
                "transactionsInPage":transactionsInPage,
            })  
    else:
        #GET Response
        return render(request, "transfer.html",{
            "transactions": transactions,
            "user":request.user,
            "account": account_sender,
            "transactionsInPage":transactionsInPage,
        }) 
    
# Create a global variable for generate de code in a function, after that we can check it in another 
code_generated = None

def code_generator(request):
    # Stamp global code
    global code_generated
    code = random.randint(10000, 99999) 
    code_generated = code
    # Here we need a TWILIO account data
    if request.method =='POST':
        
        account_sid = 'ACc490100ed731e11e5232ab16b0716ab8'
        auth_token = 'a311122b9836dd10f7732846caa14d34'
        client = Client(account_sid, auth_token)
        # Create de mssge
        message = client.messages \
                        .create(
                            body= code,
                            from_='+17622494206',
                            to='+393519556264'
                        )

        print(message.sid)
    return JsonResponse({"message": "Code ganerated succefull."})


def code_checker(request):
    # Get code for verification
    code = request.POST.get('code')
    print(code)
    # Check code
    if int(code) == code_generated:
        return JsonResponse({"message": "1"})
    else:
        return JsonResponse({"message": "2"})

def services(request):
    # Get all service and order it
    services = request.user.service.all().order_by("-state","-id")
    courrent_date = datetime.now().date()
    # Make paginator
    paginator = Paginator(services, 5)
    pageNumber = request.GET.get('page')
    servicesInPage = paginator.get_page(pageNumber)
    # Response
    return render (request, "services.html",{
        'services': services,
        'courrent_date' : courrent_date,
        'servicesInPage':servicesInPage
    })


def transfer_detail(request,transactionId):
    # Get the transaction id
    transfer = Transaction.objects.get(id=transactionId)
    # Response
    return render(request, "transferDetail.html",{
        'transfer':transfer,
        "user":request.user,
    })

def profile(request):
    # Get User data
    account = Account.objects.get(owner=request.user);
    # Response
    return render(request, 'profile.html',{
        "user":request.user,
        'account':account,
    })


def editEmail(request):
    # Get request data
    if request.method == 'POST':
        data = json.loads(request.body)
        new_email = data.get('new_email')
    # Chanche email
        user = request.user
        user.email = new_email
        user.save()
        response_data = {
            'message': "Successful Modification",
            'email': new_email
        }
    # Response
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def editPhone(request):
    # Get request data
    if request.method == 'POST':
        data = json.loads(request.body)
        new_phone_number = data.get('new_phone')

    # Chance phone number
        user = request.user
        user.phone_number = new_phone_number
        user.save()
        
        response_data = {
            'message': "Successful Modification",
            'phoneNumber': new_phone_number
        }
    # Response
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

def addService(request):    
    
    if request.method == 'POST':
        # Get  Post Data
        courrent_date = datetime.now().date()
        expiration_date = datetime(courrent_date.year, courrent_date.month + 1, 10)
        service_id = request.POST['selected_user']
        service_account = Account.objects.get(owner=service_id)
        # Create a new Service
        newService = Service.objects.create( service_name = service_account.owner.username,
                                amount_service = Decimal(random.uniform(100, 200)),
                                expiration_date =  expiration_date,
                                service_account = service_account,
                                state = "Pending")
        
        newService.save()
        user=request.user
        user.service.add(newService)
        # POST Response
        return HttpResponseRedirect(reverse("services"))
    else:
        # GET Response
        user_enterprises = User.objects.filter(username__icontains='Enterprise')
        
        return render(request, 'addService.html',{
            'user_enterprises':user_enterprises
        })
    
def service_detail(request,id):
    #Get service data
    service = Service.objects.get(id=id)
    courrent_date = datetime.now().date()
    # Response
    return render(request, 'serviceDetail.html',{
        'service':service,
        'courrent_date' : courrent_date,
    })


def service_pay(request,id):
    if request.method == 'POST':
        if not Service.objects.filter(id=id).exists():
            services = request.user.service.all().order_by("-state","-id")
            courrent_date = datetime.now().date()
            # Make paginator
            paginator = Paginator(services, 5)
            pageNumber = request.GET.get('page')
            servicesInPage = paginator.get_page(pageNumber)
            # Response
            return render (request, "services.html",{
                'services': services,
                'courrent_date' : courrent_date,
                'servicesInPage':servicesInPage
            })
        else:    
            # Get data
            courrent_date = datetime.now().date()
            account_sender = Account.objects.get(owner = request.user)
            service = Service.objects.get(id=id)
            amount = service.amount_service
            # Check our money
            if   account_sender.account_amount > amount :
                    # Create transaction
                debit = Transaction.objects.create(account_sender= account_sender,
                                                    account_recipient = service.service_account,
                                                    transaction_amount = amount,
                                                    date = datetime.now(),
                                                    type = 'Debit')
                debit.save()
                    # Add transaction to Servive model
                service.service_transaction = debit
                service.save()

                    # Make a debit
                account_sender.account_amount = account_sender.account_amount - amount
                account_sender.save()
                    # Add money to services account
                service.service_account.account_amount =  service.service_account.account_amount + amount
                service.service_account.save()
                    # Chanche services state
                service.state = "Paid"
                service.paid_date = datetime.now()
                service.save()
                #Response with enought money
                return HttpResponseRedirect(reverse("services"))
            else:
                #Response without enought money
                return render(request, 'serviceDetail.html',{
                'service':service,
                'courrent_date' : courrent_date,
                "message": "You have not enough money",
            })




def voucher(request, id):
    # Get Objects
    transfer = get_object_or_404(Transaction, id=id)
    account = Account.objects.get(owner=request.user)
    
    # Create a pdf with reportlab and save it in BytesIO
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Styles 
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(name='CustomStyle', parent=styles['Normal'])
    custom_style.alignment = 1  # Alineación central
    custom_style.fontSize = 12  # Tamaño de fuente
    custom_style.fontName = 'Helvetica'  # Fuente
    
    # Date Format
    formatted_date = transfer.date.strftime('%Y-%m-%d %H:%M:%S')
    
    # Style to bank name
    bank_name_style = ParagraphStyle(name='BankNameStyle', parent=styles['Normal'])
    bank_name_style.alignment = 1  # Alineación central
    bank_name_style.fontSize = 30  # Tamaño de fuente aumentado
    bank_name_style.fontName = 'Helvetica-Bold'  # Fuente en negrita
    bank_name_style.textColor = colors.lightblue  # Color celeste


    story = []
    # Add content to pdf
    story.append(Paragraph(account.bank, bank_name_style))
    story.append(Paragraph('<br/><br/>', custom_style))
    story.append(Paragraph('<br/><br/>', custom_style))
    story.append(Paragraph('Transfer Voucher', custom_style))
    story.append(Paragraph('<br/><br/>', custom_style))
    story.append(Paragraph('Fecha: {}'.format(formatted_date), custom_style))
    story.append(Paragraph('To: ' + transfer.account_recipient.cbu, custom_style))
    story.append(Paragraph('Total Amount: $' + str(transfer.transaction_amount), custom_style))

    #Make a square
    c.setFillColor(colors.lightblue)
    c.rect(0.1*inch,0.1*inch,0.1*inch,0.1*inch, fill=1)
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    doc.build(story)

    # Configure buffer from start
    buffer.seek(0)

    # Create Response
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transfer_voucher.pdf"'

    return response

def account(request):
    # Get account data
    account = Account.objects.get(owner= request.user.id)
    transactions = Transaction.objects.filter(Q(account_sender=account) | Q(account_recipient=account)).order_by("id").reverse()

    # Create paginator for transactions
    paginator = Paginator(transactions, 10)
    pageNumber = request.GET.get('page')
    transactionsInPage = paginator.get_page(pageNumber)
    # Response
    return render (request,'account.html',{
        'account':account,
        'transactionsInPage':transactionsInPage
    })

def cards(request):
    if not Card.objects.filter(owner=request.user).exists():
        return render(request, 'cards.html')
    else:
        card = Card.objects.get(owner=request.user)
        account = Account.objects.get(owner = request.user)
        bank = account.bank
        return render(request, 'cards.html',{
            'card':card,
            'bank':bank
        })

def add_card(request):
    account = Account.objects.get(owner = request.user)
    bank = account.bank
    #Create a credit card
    if request.method == 'POST':
        if not Card.objects.filter(owner=request.user).exists():
            courrent_date = datetime.now().date()
            expiration_date = courrent_date.replace(year=courrent_date.year + 1, month=12, day=1)
            new_Card = Card.objects.create(owner = request.user,
                                        cvv= random.randint(100, 999),
                                        card_number = randonCardNumber(),
                                        expiration_date=expiration_date,
                                        type = 'Credit'
                                        )
            new_Card.save()

            return render(request,'cards.html',{
                'card': new_Card,
                'bank':bank
            })
        else:
            card = Card.objects.get(owner=request.user)
            return render(request,'cards.html',{
                'card': card,
                'bank':bank,
                'message': 'You can only have one Credit Car '
            })


def randonCardNumber():
    number = ""
    for _ in range(4):
        digit = random.randint(1000, 9999)
        number += str(digit)
    return number

def delete_card(request,id):
    if request.method == 'POST':
        if not Card.objects.filter(owner=request.user).exists():
            return render(request, 'cards.html',{
                'message': 'Your dont have a Credit Card '
            })
        else:
            card = Card.objects.get(id = id)
            card.delete()
            
            return render(request, 'cards.html',{
                'message': 'Your card was removed successfully '
            })
            

def notifications (request):
    #Get all user notification
    notifications = Notification.objects.filter(recipient=request.user)
    # Paginator
    paginator = Paginator(notifications, 8)
    pageNumber = request.GET.get('page')
    notificationsInPage = paginator.get_page(pageNumber)
    #Change status to read
    for notification in notifications:
        notification.read = True
        notification.save()

    return render(request,'notifications.html',{
        'notificationsInPage':notificationsInPage
    })

def get_unread_notifications(request):
    #get arrived notifications
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(recipient=request.user, read=False)
        count = unread_notifications.count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})
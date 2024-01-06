
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
""" from background_task import background """
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import timedelta


def validate_creditCard(value):
    if len(str(value)) != 3:
        raise ValidationError('The lenght of the cvv number is 3.')

def validate_dni(value):
    if len(str(value)) != 8:
        raise ValidationError('The lenght of the dni number is 8.')
    
class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='homebanking_users')
    user_permissions = models.ManyToManyField(Permission, related_name='homebanking_users')
    first_name = models.CharField(max_length=50);
    last_name = models.CharField(max_length=50);
    username = models.CharField(max_length=50,unique=True,);
    email = models.EmailField(max_length=50,unique=True,);
    phone_number = models.CharField(max_length=50,default="",verbose_name='Phone Number')
    dni = models.IntegerField(validators=[validate_dni], default=0,unique=True,);
    
    def __str__(self):
        return f"{self.first_name}: {self.password} {self.last_name}  {self.username} {self.email} {self.phone_number} {self.service}";


class Account(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="owner_account")
    cbu = models.CharField(default=0, max_length=25);
    account_amount = models.DecimalField(max_digits=10, decimal_places=3,default=0);
    choices = [
        ('Aurora_Finance_Bank', 'Aurora_Finance_Bank'),
        ('NexaBank', 'NexaBank'),
        ('Horizon_Trust_Bank', 'Horizon_Trust_Bank'),
        ('Crescent_Financial_Bank', 'Crescent_Financial_Bank'),
        ('Veridian_Bank', 'Veridian_Bank'),
        ('Pinnacle_Finance_Bank', 'Pinnacle_Finance_Bank'),
        ('Solstice_Savings_Bank', 'Solstice_Savings_Bank'),
        ('Equinox_Capital_Bank', 'Equinox_Capital_Bank'),
        ('Voyager_Bancorp_Bank', 'Voyager_Bancorp_Bank'),
    ]
    bank = models.CharField(max_length=100,choices=choices,default="")
    
    def __str__(self):
        return f"{self.cbu}: {self.account_amount} {self.owner.first_name} {self.bank}";

class Transaction(models.Model):
    account_sender = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="sender_account",default=None)
    account_recipient = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="recipent_account",default=None)
    transaction_amount = models.DecimalField(decimal_places=3,max_digits=10)
    date = models.DateTimeField(auto_now=True)
    notification_sent = models.BooleanField(default=False)
    choices = [
        ('Debit', 'Debit'),
        ('Transfer', 'Transfer'),
        ('Deposit', 'Deposit'),
    ]
    type = models.CharField( choices=choices,max_length=30)

    def get_sender_representation(self):
        return f"{self.account_sender.owner.first_name} {self.account_sender.owner.last_name}"

    def __str__(self):
        return f"{self.transaction_amount}: {self.date}, {self.type}"

class Service(models.Model):
    user = models.ManyToManyField(User,related_name="service",blank=True)
    amount_service = models.DecimalField(decimal_places=3,max_digits=10,blank=True,null=True)
    service_name = models.CharField(max_length=30)
    paid_date = models.DateField(default=None,blank=True,null=True)
    expiration_date = models.DateField(default=None)
    service_account =models.ForeignKey(Account, on_delete=models.CASCADE,related_name="service_account",default=None)
    choices = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid')
    ]
    state = models.CharField(choices=choices,max_length=30,default="Pending")
    service_transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, related_name='service_transaction', null=True, blank=True)
    def __str__(self):
        return f" {self.service_name}: {self.amount_service} {self.expiration_date} {self.service_account} {self.state} {self.paid_date} "
    

class Card(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="owner_creditCard")
    cvv = models.IntegerField (validators=[validate_creditCard])
    card_number = models.IntegerField(default=0)
    expiration_date = models.DateField(default=timezone.now)
    choices = [
        ('Credit', 'Credit'),
    ]
    type = models.CharField(max_length=100,choices=choices)
    
    def __str__(self):
        return f"{self.owner}: {self.cvv}, {self.type} {self.expiration_date} {self.card_number}"
    
class Notification(models.Model):
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField()  # Message content
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications') # The receiver of the notification
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.content} to {self.recipient.username} {self.read} "


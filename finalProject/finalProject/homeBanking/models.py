from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


from django.db import models

from django.contrib.auth.models import AbstractUser,Group, Permission
from django.db import models
from django.core.exceptions import ValidationError



def validate_creditCard(value):
    if len(str(value)) != 3:
        raise ValidationError('The lenght of the cvv number is 3.')
     
def validate_dni(value):
    if len(str(value)) != 8:
        raise ValidationError('The lenght of the cvv number is 8.')
    
class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='homebanking_users')
    user_permissions = models.ManyToManyField(Permission, related_name='homebanking_users')
    first_name = models.CharField(max_length=50);
    last_name = models.CharField(max_length=50);
    username = models.CharField(max_length=50,unique=True,);
    email = models.EmailField(max_length=50);
    phone_number = models.CharField(max_length=50,default="",verbose_name='Phone Number')
    dni = models.IntegerField(validators=[validate_dni], default=0);

    def __str__(self):
        return f"{self.first_name}: {self.password} {self.last_name}  {self.username} {self.email} {self.phone_number} ";



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
        return f"{self.cbu}: {self.account_amount}, {self.type}";

class CreditCard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="owner_creditCard")
    cvv = models.IntegerField (validators=[validate_creditCard])
    card_number = models.IntegerField(default=0)
    expiration_date = models.DateTimeField(default=timezone.now)
    choices = [
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    ]
    type = models.CharField(max_length=100,choices=choices)
    
    def __str__(self):
        return f"{self.owner}: {self.cvv}, {self.type}"
    
class Transaction(models.Model):
    account_sender = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="sender_account",default=None)
    account_recipient = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="recipent_account",default=None)
    transaction_amount = models.DecimalField(decimal_places=3,max_digits=10)
    date = models.DateTimeField(auto_now=True)#cambiar por dateTimeField
    choices = [
        ('Debit', 'Debit'),
        ('Transfer', 'Transfer'),
        ('Deposit', 'Deposit'),
    ]
    type = models.CharField( choices=choices,max_length=30)

    def __str__(self):
        return f"{self.transaction_amount}: {self.date}, {self.type}"
    
class Service(models.Model):
    service_amount = models.DecimalField(decimal_places=3,max_digits=10)
    service = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.service_amount}: {self.service}"
    
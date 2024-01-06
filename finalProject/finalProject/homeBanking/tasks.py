""" from background_task import background
from django.utils import timezone
from datetime import timedelta
from .models import Service, Transaction, Notification

@background(schedule=60)
def check_services_and_transactions():

    for service in Service.objects.filter(state='Pending'):
        if timezone.now().date() + timedelta(days=3) >= service.expiration_date:
            for user in service.user.all():
                Notification.objects.create(
                    content=f"Your service {service.service_name} is about to expire.",
                    recipient=user
                )
    
    for transaction in Transaction.objects.filter(notification_sent=False):
        Notification.objects.create(
            
            content=f"You received money from {transaction.get_sender_representation()}",
            recipient=transaction.account_recipient.owner
        )
        
        transaction.notification_sent = True
        transaction.save()
 """
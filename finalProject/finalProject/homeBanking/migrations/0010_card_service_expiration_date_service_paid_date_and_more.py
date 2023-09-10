# Generated by Django 4.1 on 2023-09-03 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import homeBanking.models


class Migration(migrations.Migration):

    dependencies = [
        ('homeBanking', '0009_account_bank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cvv', models.IntegerField(validators=[homeBanking.models.validate_creditCard])),
                ('card_number', models.IntegerField(default=0)),
                ('expiration_date', models.DateField(default=django.utils.timezone.now)),
                ('type', models.CharField(choices=[('Debit', 'Debit'), ('Credit', 'Credit')], max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_creditCard', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='expiration_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='service',
            name='paid_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='service',
            name='state',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=30),
        ),
        migrations.AddField(
            model_name='service',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='payer', to='homeBanking.account'),
        ),
        migrations.DeleteModel(
            name='CreditCard',
        ),
    ]

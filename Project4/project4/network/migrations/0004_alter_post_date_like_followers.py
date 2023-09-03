# Generated by Django 4.1 on 2023-05-24 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_post_like_alter_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postLike', to='network.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userLike', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userFollowed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userFollowed', to=settings.AUTH_USER_MODEL)),
                ('userWhoFollows', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userWhoFollows', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

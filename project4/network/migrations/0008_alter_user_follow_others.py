# Generated by Django 4.1.5 on 2023-01-29 15:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_user_img_url_alter_user_follow_others'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='follow_others',
            field=models.ManyToManyField(blank=True, null=True, related_name='follow_me', to=settings.AUTH_USER_MODEL),
        ),
    ]